
# Matrizes
# Ciando vetores para os exercicios da aula 3 de programacao R
a <- c(333909, 19900204, 869, 545125, 6632)
b <- a * 2
c <- b/3
d <- c + a^2
e <- sqrt(d)
ai = rev(a)

# Criar matriz 
M1 <- matrix(c(a,b,c,d,e,ai),nrow = 6,ncol=5,byrow = TRUE)
M2 <- matrix(c(a,b,c,d,e,ai),nrow = 5,ncol=6,byrow = FALSE)
M3 <- M1*0.1

# Verificando a tabela attitude
attitude
class(attitude)
dim(attitude)

# Convertendo attitude em matriz
M4 <- as.matrix(attitude[-6:-30, 1:6], nrow = 5, n_col = 6)
M4

# Multiplicando matrizes
M5 <- M1 * M3 # Multiplicando elementos
M6 <- M3 * M1 # Multiplicando elementos
M7 <- M1 %*% M4 # Multiplicando matrizes
M8 <- M4 %*% M1 # Multiplicando matrizes

M5 == M6
M7 == M8

# Transposicao de matrizes 
M8 %*% t(M1) # Multiplicacao de matrizes por matriz transposta


# Amostras e simulacoes
runif(n = 3,min=1,max=100)
dunif(x=8, min = 1, max = 10)

# Comandos amostrais com sample
set.seed(1)
amostra = c("T", "R", "I", "A", "N", "G", "U", "L", "O", "S")
sample(x=amostra, replace = FALSE)
sample(x=amostra, replace = TRUE)
sample(x=amostra, size = 5)
sample(x=amostra, size = 10, replace = TRUE, prob = c(1,1,5,1,1,1,1,1,1,5))

# Explorando dataset
airquality # Ver o dataset
dim(airquality) # Pegar a dimensao
summary(airquality) # Resumo do dataframe
head(airquality, 10) # Pegar as 10 primeiras linhas
airquality[runif(n = 10,min=1,max=nrow(airquality)),] # Amostra de 10 linhas aleatorias


# Criando grafico aleatorio para simulacoes
library(plotly)

set.seed(20)
amostra <- sample(x = 100, min = 1, max 100)

Bzero <- 0.5 
B1 <- 2.0

x <- rnorm(mean(amostra), sd(amostra))
erro <- rnorm(mean(amostra), sd(amostra))
valor <- Bzero + (B1 * x) + erro


plot_ly(x = x, y=valor, type = "scatter")

# Teste do professor
set.seed(20)
amostra <- sample(x = 100, min = 1, max 100)

Bzero <- 0.5 
B1 <- 2.0

x <- rnorm(n = 100, mean = 0, sd = 1)
erro <- rnorm(n = 100, mean = 0, sd = 2)
y <- Bzero + (B1 * x) + erro


plot_ly(x = x, y=y, type = "scatter")
