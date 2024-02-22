# Imports de libs padrao
import os
import sys

# Imports de libs especificos para manipulacao de dados
import numpy as np
import pandas as pd
import torch

# Import das libs para execucao de LLM's
from langchain.llms import LlamaCpp

# Import das libs para RAG
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# Import de libs utils da Nutrien
from custom_libs.ds_utils import hardware_info



class suppress_stdout_stderr(object):
    """Essa classe tem como objetivo suprimir os logs de execucao
    da classe cpp

    Args:
        object: Qualquer objeto que herde cpp
    """

    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup    = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup ( sys.stderr.fileno() )

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2 ( self.errnull_file.fileno(), self.old_stderr_fileno_undup )

        sys.stdout = self.outnull_file        
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):        
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2 ( self.old_stderr_fileno, self.old_stderr_fileno_undup )

        os.close ( self.old_stdout_fileno )
        os.close ( self.old_stderr_fileno )

        self.outnull_file.close()
        self.errnull_file.close()

class LLM_With_Rag:
    """Essa classe roda uma LLM com RAG.
    Para utilizar a tecnica RAG e ncessario criar um banco de dados
    em memoria com os embedings dos documentos que quermos que a LLM
    leia, tenha em mente que esse banco so precisa ser criado somente
    a primeira vez que o processo roda ou entao quando um novo arquivo
    e adicionado a biblioteca de arquivos.

    Utilize a flag 'create_storage_db' para especificar quando criar
    essa base de dados em memoria.

    O embedding criado e o padrao do HuggingFaces (pode melhorar)

    A base de dados escolhida para armazenar os embeddings e o FAISS
    (muitas oportunidades de melhoria de DB e tipo de armazenamento)
    """

    def __init__(self,
                 model_name = "llama-2-7b-chat.Q5_K_M.gguf",
                 storage_path = "./00_storage",
                 models_path = "./01_models",
                 rag_data_path = "./02_transcript_data",
                 results_path = "./03_results",
                 create_storage_db = True,
                 device = "cpu", # Aceita cpu, gpu e auto para gpu se possivel
                 save_results = False,
                 assist_log = False,
                 llm_verbose = True,):

        # [ATRIB] Variavel que guarda qual e o modelo que vai ser utilziado
        self.model_name = model_name

        # [ATRIB] Variavel com a localizacao onde guardamos o banco de embeddings
        self.storage_path = storage_path

        # [ATRIB] Variavel com a localizacao onde guardamos os modelos LLMs
        self.models_path = models_path

        # [ATRIB] Variavel com a localizacao onde guardamos os dados que o LLM vai ler como contexto
        self.rag_data_path = rag_data_path

        # [ATRIB] Variavel com a localizacao de eventuais resultados
        self.results_path = results_path

        # [ATRIB] [FAISS] Variavel por indicar se o banco de arquivos deve ser
        # recriado ou nao. Essa variavel e muito importante caso nao queiramos
        # recriar o bando vetorizado para o RAG. Caso o banco ja exista e nao
        # precise ser atualizado nao e recomendado que o recrie, basta utiliza-lo.
        self.create_storage_db = create_storage_db

        # [ATRIB] Tenta forcar o tipo de device que vamos utilizar dentro do
        # processamento (GPU ou CPU)
        # Recomenda-se GPU apenas no LINUX (MAC NAO E LINUX)
        self.device = device

        # [ATRIB] Variavel com a opcao de salvar os prompts e suas respostas
        self.save_results = save_results

        # [ATRIB] Variavel que guarda a preferencia sobre o log de execucao
        self.assist_log = assist_log

        if self.assist_log:

            # Caso o log esteja ativo da captura o hardware
            # que esta rodando a aplicacao

            # Cria o objeto da classe de info de hardware
            hi = hardware_info()

            # Captura e exibe as informacoes em saida de terminal
            hi.get_info()

        # Inicializa objeto de retriever e vectorstorage
        self.retriever = None
        self.vectorstore = None

        # Grava o parametro verbose de inicializacao do modelo
        self.llm_verbose = llm_verbose


    def __create_db(self,):
        """Caso a execucao precise criar uma base de dados com os
        documentos para a tecnica de RAG.

        Veja que aqui e muito importante que todos os documentos
        que queremos contexto para a RAG estejam na pasta de 
        transcripts em formato .txt.

        (Como sugestao de melhoria para o futuro da lib, podemos 
        pensar em implementar uma leitura de arquivos PDF tambem)

        Returns:
            bool: Returna True ou False de acordo com o status de
            criacao do banco local de arquivos
        """

        # Variavel de retorno inicialziada como falsa por padrao
        # e so e atualziada caso tenhamos sucesso na criacao da
        # base de dados FAISS com os arquivos para RAG
        sucess = False

        try:
            # Cria objeto de leitura
            loader = DirectoryLoader(self.rag_data_path, glob="*.txt")

            # Cria objeto com os arquivos de leitura
            documents = loader.load()

            # Caso o log esteja ligado mostra os documentos carregados
            if self.assist_log:
                print(f"""Total de documentos encontrados: {len(documents)} """)
                print("Indexando...")

            # Divide os arquivos txt em chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)

            # Carrega modelo de embedding
            embedding_function = HuggingFaceEmbeddings(model_kwargs={'device': self.device})
            embedding_function.embed_query(texts[0].page_content)

            # Cria e persiste um base FAISS
            vector_database = FAISS.from_documents(texts, embedding_function)

            # Tenta persistir a base de vetores
            vector_database.save_local(self.storage_path)

            # Caso o log esteja ligado avisa sobre a persistencia do vetor
            if self.assist_log:
                print("Base de dados criada em: ", self.storage_path)
                return True


            # Caso todos os passos tenham sido completados com sucesso grava sucesso
            # na variavel de retorno
            sucess = True
        
        except Exception as e:

            print(f""" --- Error reading documents or creating local DB ---
                  (EN)
                  Check your pip to understand if you have all langchain
                  and llama CPP are installed correctly.
                  
                  On Windows systems is particulary complicated to install
                  beautifulsoap4 and install llama-cpp-python, you may have
                  to run CMAKE or install microsoft visual studio stuff
                  
                  (PT-BR)
                  Verifique atraves do seu PIP se voce tem todos os imports
                  de langchain e llama CPP instalados corretamente.
                  
                  No Windows temos problemas bem latentes e particulares
                  para instalar o beuatifullsouap4 e o llama-cpp-python,
                  voce provavelmente vai precisar rodar o CMAKE ou instalar
                  as bibliotecas adicionas do microsoft visual studio

                  The raised error is:
                  O erro encontrado e:
                  {e}
                  """)

        return sucess


    def __get_db(self,):
        """Traz para memoria e deixa disponivel para a LLM ler
        os arquivos indexados dentro do banco de dados local

        Returns:
            _type_: _description_
        """

        try:
            # Carrega o modelo de embeddings
            embeddings = HuggingFaceEmbeddings()

            # Carrega a base FAISS
            self.vectorstore = FAISS.load_local(self.storage_path, embeddings)

            if self.assist_log:
                # Caso log esteja ligado avisa sobre o carregamento com sucesso
                print("VectorStore carregado a partir de:"+ self.storage_path)
                # print(f"""Vector storage: {self.vectorstore}""") for debug

            # Retorna objeto de vetores previamente carregado no disco
            return self.vectorstore

        except Exception as e:

            print(f""" --- Error reading documents or DB store ---
                  (EN)
                  Check your pip to understand if you have all langchain
                  and llama CPP are installed correctly.
                  
                  On Windows systems is particulary complicated to install
                  beautifulsoap4 and install llama-cpp-python, you may have
                  to run CMAKE or install microsoft visual studio stuff
                  
                  (PT-BR)
                  Verifique atraves do seu PIP se voce tem todos os imports
                  de langchain e llama CPP instalados corretamente.
                  
                  No Windows temos problemas bem latentes e particulares
                  para instalar o beuatifullsouap4 e o llama-cpp-python,
                  voce provavelmente vai precisar rodar o CMAKE ou instalar
                  as bibliotecas adicionas do microsoft visual studio

                  The raised error is:
                  O erro encontrado e:
                  {e}
                  """)

            return False


    def __generate_model(self,):
        """Gera resposta utilizando o modelo escolhido e o contexto
        RAG apresentado

        Returns:
            str: Retorna um prompt em stream de uma pergunta feita 
            ao modelo
        """

        try:
            self.llm = LlamaCpp(
                #model_path = "./01_models/llama-2-7b-chat.Q5_K_M.gguf"
                model_path = f"""{self.models_path}/{self.model_name}""", 
                n_gpu_layers=1,
                n_batch=2048,
                n_ctx=2048,
                f16_kv=True,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                verbose=self.llm_verbose,
                )

            if self.device != "cpu":
                # Variavel de utilizacao de GPU ou nao
                self.device = "cuda" if torch.cuda.is_available() else "cpu"

            # Avisa sobre o modelo para o log
            if self.assist_log: 
                print("Modelo carregado e instanciado com sucesso")

            return True

        except Exception as e:
            # Estamos capturando excessoes genericas de proposito
            #nosso objetivo e que as excessoes estourem mesmo.

            print(e)

            return False


    def start_model(self, new_db = True):
        """Responsavel por inicializar o modelo de dados

        Args:
            new_db (bool, optional): Cria banco de dados de documentos caso True. Padrao True.
        """

        # Avisa o log sobre inicio do processo
        if self.assist_log: 
            print("Ligando os motores...")

        # Constroi o banco de dados vetorizado
        if new_db:
            self.__create_db()

        # Gera objeto da vector store
        self.__get_db()

        # Cria modelo da LLM escolhida
        self.__generate_model()

        # Devolve o banco em um objeto retriever
        # retriever = self.vectorstore.as_retriver()

        if self.assist_log:
            print("Warmup do motor finalizado")

        return self.vectorstore


    def answer_me(self,question):
        """Metodo responsavel por responder perguntas"""

        prompt_template= """
        ### [INST] 
        Instructions: Answer in portuguese, and take the following context in mind:

        {context}

        ### Question to answer:
        {question} 

        [/INST]
        """

        # Abstraction of Prompt
        prompt = ChatPromptTemplate.from_template(prompt_template)
        #output_parser = StrOutputParser()

        # Criando a cadeia LLM
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)

        # Cadeia de resposta RAG
        rag_chain = ( 
        {"context": self.vectorstore.as_retriever(), "question": RunnablePassthrough()}
            | llm_chain
        )
        print("====================================")
        print(question)
        rag_chain.invoke(question)
        print("\n====================================\n")

        #return rag_chain
