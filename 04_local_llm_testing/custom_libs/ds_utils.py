class hardware_info():
    """
    Essa classe foi cirada com o proprosito de retornar as informacoes
    relevantes do sistema operacional onde o python esta instalado.
    """


    def get_size(self, bytes, suffix="B"):
        """
        Faz a escala de bits no formato correto
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """

        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    def get_info(self):
        """Recupera os dados de cada um dos parametros de sistema em variaveis separadas
        e retorna para op usuario"""

        import os
        import platform
        import datetime
        import psutil

        import GPUtil

        # Recupera o dia e hora de hoje
        rep_date = datetime.datetime.now()

        # Recupera versao do Python
        py_ver = platform.python_version()

        # Recupera dados de sistema operacional
        os_system = platform.system() # Recupera o nome da plataforma (Windows, linux ou MacOsX)
        os_name = os.name # Recupera nome do sistema (Windows 10, OSX Sierra, Ubuntu...)
        os_platform = platform.release() # Recupera a plataforma e numero de release (v1.2, v10, 12-45-12...)

        # Recupera dados de arquitetura
        sys_machin = platform.machine() # Recupera a arquitetura da maquina (X86, PPC, ARM...)
        sys_archquitetura = platform.architecture()# Recupera a arquitetura da maquina (64 bits, 32 bits...)

        # Recupera dados de CPU
        cpu_cores_total = psutil.cpu_count(logical=False) # Quantidade de cores totais
        cpu_cores_fisic = psutil.cpu_count(logical=True) # Quantidade de cores fisicos
        cpufreq = psutil.cpu_freq() # Recupera a utilizacao da CPU no momento
        cpu_freq_max = f"""Max Frequency: {cpufreq.max:.2f}Mhz""" # Frequencia maxima
        cpu_freq_min = f"""Min Frequency: {cpufreq.min:.2f}Mhz """ # Frequencia minima
        cpu_freq_now = f"""Current Frequency: {cpufreq.current:.2f}Mhz """ # Frequencia no momento

        # Recupera dados de memoria RAM
        svmem = psutil.virtual_memory() # Recupera dados de RAM no momento
        ram_total = self.get_size(svmem.total) # Quantidade de RAM total
        ram_avaliable = self.get_size(svmem.available) # Quantidade de RAM disponivel
        ram_usada = self.get_size(svmem.used) # Quantidade de RAM usada
        ram_percent = svmem.percent # Quantidade em percentual de RAM usada

        # Recupera dados de disco
        partitions = psutil.disk_partitions() # Recupera todas as particoes do disco
        partition1 = "DISK1 - Device: " + partitions[0].device # Recupera particao 1
        partition2 = "DISK1 - Device: " + partitions[1].device # Recupera particao 2
        partition3 = "DISK1 - Device: " + partitions[2].device # Recupera particao 3
        hd_total = self.get_size(psutil.disk_usage(os.getcwd()).total) # Recupera o tamanho do disco onde o python roda
        hd_free = self.get_size(psutil.disk_usage(os.getcwd()).free) # Recupera o espaco livre em disco de onde o python roda
        
        # Recupera dados de GPU
        gpus = GPUtil.getGPUs()
        gpu_avaliable = GPUtil.getFirstAvailable()

        # Formata o relatorio de exibicao
        # Preferivelmente exibido em um Jupyter notebook

        print(f"""|{rep_date}| Hardware report:
        
    ==============================================
     Software:
      Python ver:............{py_ver}
      OS system:.............{os_system}
      OS name:...............{os_name}
      OS plataform:..........{os_platform}
      Machine sys:...........{sys_machin}
      Machine architecture...{sys_archquitetura}

    ==============================================
     CPU:
      Total cores:...........{cpu_cores_total}
      Logical cores:.........{cpu_cores_fisic}
      CPU max frequency:.....{cpu_freq_max}
      CPU min frequency:.....{cpu_freq_min}
      CPU frequency now:.....{cpu_freq_now}

    ==============================================
     RAM:
      Total RAM:.............{ram_total}
      RAM avaliable:.........{ram_avaliable}
      RAM used:..............{ram_usada}
      RAM%:..................{ram_percent}
      
    ==============================================
     Storage:
      Partition 1:............{partition1}
      Partition 2:............{partition2}
      Partition 3:............{partition3}
      Python avaliable HDD:...{hd_total}
      Python free HDD:........{hd_free}

    ==============================================
     GPU:
      GPU:....................{gpus}
      GPU Avaliable:..........{gpu_avaliable}

    ==============================================
    """)
