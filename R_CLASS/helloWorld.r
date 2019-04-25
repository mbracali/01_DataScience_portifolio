# 24/04/2019
# Criacao de vetores para o exercico da aula de R

vetLogico <- c(T,T,F,F)
vetInt <- c(1L,2L,3L,4L)
vetNum <- c(1.0,2.0,3.0,4.0)
vetText <- c("1","2","3","4")
vetIma <- c(1i,2i,3i,4i)


# Cria uma lista com 5 elementos, utilizando os
# vetores criados anteriormente

lista <- list(vetLogico, vetInt, vetNum, vetText, vetIma)


# Cria matrix 4 x 4 com 16 numeros pares

matrix = matrix(c(2L,4L,6L,8L,10L,12L,14L,16L,18L,20L,22L,24L,26L,28L,30L,32L), nrow = 4)


# Cria dataFrame com os vetores criados anteriormente

df = data.frame("Logicos" = vetLogico, 
                "Inteiros" = vetInt,
                "Numericos" = vetNum,
                "Texto" = vetText,
                "Imaginarios" = vetIma)

row.names(df) <- c("L1","L2","L3","L4")
