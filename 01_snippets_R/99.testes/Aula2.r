# 08/05/2019 - Aula de sequencias 

# Criando sequencias simples
1:9
80:32
4:-2
3:3
1:0

# Ver as os metodos de seq via HELP
?seq.int
?seq_along
?seq_len

# Criando vetores via repeticao
rep(0,times = 40)
rep(c(0,1,2), times = 10)
rep(c(0,1,2), each = 10)

# Criar uma variavel my_seq com 30 valores entre 5 e 10
my_seq = rep(seq(5, 10), times=5)

# Help da funcao :
?':'

# Diferenca entre
pi:10 # Cria sequencia de valores PI ate 10
10:pi # Cria sequencia de 10 ate PI

# Tamanho de my_seq
length(my_seq)

# Sequencia que acompanhe o tamanho de my_seq
seq_along(my_seq)



# Valores especiais

# Criar variaveis com tipos especiais
v_NA = NA
v_NULL = NULL
v_NAN = NaN
v_PLUS_INFINITE = +Inf
V_MINUS_INFINITE = -Inf

# Criar vetor com as variaveis criadas
lista = list(v_NA, v_NULL, v_NAN, v_PLUS_INFINITE, V_MINUS_INFINITE)
vet_vars = c(v_NA, v_NULL, v_NAN, v_PLUS_INFINITE, V_MINUS_INFINITE)
vet_bool = c(is.na(v_NA), is.nan(v_NAN), is.null(v_NULL), is.infinite(v_PLUS_INFINITE))


# Filtrando dados das estruturas

# Filtro em mtcars
mtcars
mtcars[2,5]
mtcars[2:4,5]
mtcars[2:4,5:7]
mtcars[2:4,c(1,2,3)]
mtcars[2:4,c("mpg","wt")]

# Encontrar todas as colunas dos registros sejam maior ou iual a 15
mtcars[mtcars$mpg > 15,]


# Datas e horas

# Experimentos
dia_texto <-"28/09/2017 T 18:51:30"
dia_date  <-as.Date(dia_texto,format="%d/%m/%Y T %H:%M:%S",tz="America/Sao_Paulo")
dia.time1 <-as.POSIXct(dia_texto,format="%d/%m/%Y T %H:%M:%S",tz="America/Sao_Paulo")
dia.time2 <-as.POSIXlt(dia_texto,format="%d/%m/%Y T %H:%M:%S",tz="America/Sao_Paulo")

# Prints
dia_date
dia.time1
dia.time2
unclass(dia_date)
unclass(dia.time1)
unclass(dia.time2)

# Prints especificos
dia.time1$year
dia.time2$year

# Instalando o lubridate
install.packages("lubridate")
library(lubridate)

# Utilizando o lubridate
ymd("20110604")
mdy("06-04-2011")
dmy("04/06/2011")
ymd_hms("2018-04-23T19:02:13")
dmy_hms("23/04/2018 19:03:14")

# Criando durations
d260_seconds = duration(260, units = 'seconds')
d260_minutes = duration(260, units = 'minutes')
d60_minutes = duration(60, units = 'minutes')
d260_minutes/60

d1_day = duration(1, units = 'days')
d60_minutes - d1_day

d12_days = duration("12days 5hours 10mins")
d12_days

# Desafio Black Friday
nov_1 = dmy("01112018")
nov_2 = dmy("01112018") + wday(nov_1)

((day(nov_1) -7) + wday(nov_1) + 5



