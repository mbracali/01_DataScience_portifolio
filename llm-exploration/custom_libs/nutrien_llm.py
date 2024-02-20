import sys, os, urllib
from llama_cpp import Llama # para instalar = pip install llama-cpp-python
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage


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


class OpenaiLlm:
    """Classe responsavel por retornar respostas da OpenAi

    Returns:
        Str: Tem como objetivo retornar uma resposta de um prompt
    """

    def __init__(self,
                open_ai_key = """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""",
                fine_tunning_folder = "fine_tunning",
                assist_log = 0):

        # [ATRIB] Variavel que guarda a preferencia sobre o log de execucao
        self.assist_log = assist_log

        # [ATRIB] Variavel que guarda a chave de API da OpenAI
        self.open_ai_key = open_ai_key

        # [ATRIB] Variavel que guarda a pasta com os textos para fine tunning
        self.fine_tunning_folder = fine_tunning_folder

        # Mecanicas exclusivas para o funcionamento do LLM da OpenAI
        # outras classes com outros modelos implementam so os outros
        # passos acima.

        # [SIS] Seta a variavel de ambiente com a chave da OpenAI
        os.environ['OPENAI_API_KEY'] = self.open_ai_key

        # [GPT] Carrega os textos de fine tune do modelo
        self.documents = SimpleDirectoryReader('fine_tunning').load_data()

        # [GPT] Carrega os documentos de fine tunning ao indice do modelo
        self.index = VectorStoreIndex.from_documents(self.documents)

        # [GPT] Persiste o indice de fine tune do modelo
        self.index.storage_context.persist()

        # [GPT] Carrega o contexto de conversacao com a LLM
        self.storage_context = StorageContext.from_defaults(persist_dir="./storage")

        # [GPT] Carrega o indice de conversacao com a LLM
        self.index = load_index_from_storage(self.storage_context)

        # [GPT] Cria objeto que lida com o prompt do usuario
        self.query_engine = self.index.as_query_engine()

        # [LOG] Se o log estiver ligado executa os seguintes
        if self.assist_log:
            print(self.index)
            print(len(self.index))


    def get_answer(self, prompt):
        """Resolve a pergunta feita pelo usuario e devolve a resposta

        Args:
            prompt (string): Aqui e esperado uma pergunta completa sem filtros feita pelo usuario
            assist_log (int, optional): Flag que indica se queremos um log de processamento. 
            Padrao em 0.
        """

        # [GPT] Essa linha ja se conecta com a API da OpenAI e resolve o prompt enviado pelo usuario
        response = self.query_engine.query(prompt)

        # [LOG] Se o log estiver ligado executa os seguintes
        # (Ver construtor da classe para opcao de log)
        if self.assist_log:
            print(len(response))

        return response


class Llama2:
    """Classe responsavel por retornar respostas do modelo LLama2

    Returns:
        Str: Tem como objetivo retornar uma resposta de um prompt
    """

    def __init__(self,
                model = """./models/llama-2-7b-chat.Q5_K_M.gguf""",
                model_download = False,
                fine_tunning_folder = "fine_tunning",
                assist_log = 0):

        # Caso o modelo nao esteja baixaddo, essa flag forca o download do modelo
        if model_download:
            # Repositorie of models on: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
            url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf?download=true"
            downloader = urllib.URLopener()
            downloader.retrieve(url, model)

        # [ATRIB] Variavel que guarda a preferencia sobre o log de execucao
        self.assist_log = assist_log

        # [ATRIB] Variavel que guarda qual modelo vai ser usado
        self.model = model

        # [ATRIB] Variavel que guarda a pasta com os textos para fine tunning
        self.fine_tunning_folder = fine_tunning_folder
        # Download via hugging faces

        # Carrega o modelo LLAMA2
        with suppress_stdout_stderr():
            self.llm = Llama(model)


    def get_answer(self, prompt):
        """Resolve a pergunta feita pelo usuario e devolve a resposta

        Args:
            prompt (string): Aqui e esperado uma pergunta completa sem filtros feita pelo usuario
            assist_log (int, optional): Flag que indica se queremos um log de processamento. 
            Padrao em 0.
        """

        # [GPT] Essa linha carrega o modelo e
        with suppress_stdout_stderr():
            response = self.llm(prompt,
                                max_tokens=1000)

        # [LOG] Se o log estiver ligado executa os seguintes
        # (Ver construtor da classe para opcao de log)
        if self.assist_log:
            print(len(response))

        return response["choices"][0]["text"]


class Vicuna:
    """Classe responsavel por retornar respostas do modelo LLama2

    Returns:
        Str: Tem como objetivo retornar uma resposta de um prompt
    """

    def __init__(self,
                model = """./models/llama-2-7b-chat.Q5_K_M.gguf""",
                model_download = False,
                fine_tunning_folder = "fine_tunning",
                assist_log = 0):

        # Caso o modelo nao esteja baixaddo, essa flag forca o download do modelo
        if model_download:
            # Repositorie of models on: https://huggingface.co/TheBloke/stable-vicuna-13B-GGUF
            url = "https://huggingface.co/TheBloke/vicuna-13B-v1.5-GGUF/resolve/main/vicuna-13b-v1.5.Q5_K_S.gguf?download=true"
            downloader = urllib.URLopener()
            downloader.retrieve(url, model)

        # [ATRIB] Variavel que guarda a preferencia sobre o log de execucao
        self.assist_log = assist_log

        # [ATRIB] Variavel que guarda qual modelo vai ser usado
        self.model = model

        # [ATRIB] Variavel que guarda a pasta com os textos para fine tunning
        self.fine_tunning_folder = fine_tunning_folder
        # Download via hugging faces

        # Carrega o modelo LLAMA2
        with suppress_stdout_stderr():
            self.llm = Llama(model)


    def get_answer(self, prompt):
        """Resolve a pergunta feita pelo usuario e devolve a resposta

        Args:
            prompt (string): Aqui e esperado uma pergunta completa sem filtros feita pelo usuario
            assist_log (int, optional): Flag que indica se queremos um log de processamento. 
            Padrao em 0.
        """

        # [GPT] Essa linha carrega o modelo e
        with suppress_stdout_stderr():
            response = self.llm(prompt,
                                max_tokens=1000)

        # [LOG] Se o log estiver ligado executa os seguintes
        # (Ver construtor da classe para opcao de log)
        if self.assist_log:
            print(len(response))

        #return response["choices"][0]["text"]
        return response


class Llama2_testing:
    """Classe responsavel por retornar respostas do modelo LLama2

    Returns:
        Str: Tem como objetivo retornar uma resposta de um prompt
    """

    def __init__(self,
                model = """./models/llama-2-7b-chat.Q5_K_M.gguf""",
                model_download = False,
                fine_tunning_folder = "fine_tunning",
                assist_log = 0):

        # Caso o modelo nao esteja baixaddo, essa flag forca o download do modelo
        if model_download:
            # Repositorie of models on: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
            url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf?download=true"
            downloader = urllib.URLopener()
            downloader.retrieve(url, model)

        # [ATRIB] Variavel que guarda a preferencia sobre o log de execucao
        self.assist_log = assist_log

        # [ATRIB] Variavel que guarda qual modelo vai ser usado
        self.model = model

        # [ATRIB] Variavel que guarda a pasta com os textos para fine tunning
        self.fine_tunning_folder = fine_tunning_folder
        # Download via hugging faces

        # Carrega o modelo LLAMA2
        with suppress_stdout_stderr():
            self.llm = Llama(model, n_ctx=2048)


        # [GPT] Carrega os textos de fine tune do modelo
        self.documents = SimpleDirectoryReader('fine_tunning').load_data()

        # [GPT] Carrega os documentos de fine tunning ao indice do modelo
        self.index = VectorStoreIndex.from_documents(self.documents)

        # [GPT] Persiste o indice de fine tune do modelo
        self.index.storage_context.persist()

        # [GPT] Carrega o contexto de conversacao com a LLM
        self.storage_context = StorageContext.from_defaults(persist_dir="./storage")

        # [GPT] Carrega o indice de conversacao com a LLM
        self.index = load_index_from_storage(self.storage_context)

        # [GPT] Cria objeto que lida com o prompt do usuario
        self.query_engine = self.index.as_query_engine()



    def get_answer(self, prompt):
        """Resolve a pergunta feita pelo usuario e devolve a resposta

        Args:
            prompt (string): Aqui e esperado uma pergunta completa sem filtros feita pelo usuario
            assist_log (int, optional): Flag que indica se queremos um log de processamento. 
            Padrao em 0.
        """

        # [GPT] Essa linha carrega o modelo e
        with suppress_stdout_stderr():
            response = self.llm("Responda apenas em portugues: \n" + prompt,
                                max_tokens=0, )
            
            response = self.query_engine.query(prompt)

        # [LOG] Se o log estiver ligado executa os seguintes
        # (Ver construtor da classe para opcao de log)
        if self.assist_log:
            print(len(response))

        return response["choices"][0]["text"]