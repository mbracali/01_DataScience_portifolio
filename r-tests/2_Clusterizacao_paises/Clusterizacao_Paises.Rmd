---
title: "Analise paises"
author: "Marcelo Bracali"
output: html_document
---

## Analise: Paises

O objetivo desse markdown é realizar uma analise em cima de uma base de paises e classificar os paises em grupos de acordo com a semelhança nas váriaves fornecidas. 
Essa base tem detalhado o desempenho de diversos paises em várias provas de resistência, cada uma das provas é representada por uma coluna.

Para tal o primeiro passo é importar a base e verificar o formato das variaveis:

```{r}
paises <- read.csv("C:/2019_workspace/2_PROJETOS/8_PORTIFOLIOS/Base Paises/DADOS_Papercsv_1.csv", row.names=1, sep=";")
str(paises) #Verificando o formato das variáveis
summary(paises) #Estatísticas descritivas
```

A titulo observatório, vamos ver a distribuição dos dados em cada uma das provas:

```{r}
par (mfrow=c(3,3))
hist(paises$p100ms)
hist(paises$p200ms)
hist(paises$p400ms)
hist(paises$p800mm)
hist(paises$p1500mm)
hist(paises$p3000mm)
hist(paises$pmaratm)
```


Ainda, é importante entender a correlação dos dados entre eles mesmos.
```{r}
matcor <- cor(paises)
print(matcor, digits = 2)

#install.packages("corrplot")
library(corrplot)

corrplot::corrplot(matcor, method="circle", order="hclust")

panel.cor <- function(x, y, digits=2, prefix ="", cex.cor,
    ...)  {
    usr <- par("usr")
    on.exit(par(usr))
    par(usr = c(0, 1, 0, 1))
    r <- cor(x, y , use = "pairwise.complete.obs")
    txt <- format(c(r, 0.123456789), digits = digits) [1]
    txt <- paste(prefix, txt, sep = "")
    if (missing(cex.cor))
        cex <- 0.8/strwidth(txt)
# abs(r) é para que na saída as correlações ficam proporcionais
    text(0.5, 0.5, txt, cex = cex * abs(r))
}

```




## Criando cluster de performance

Para a criação de clusters vamos utilizar uma técnica para deixar os dados escalaveis:
```{r}
Padr_paises <- scale(paises) # Aplica a técnica de SCALE
summary(Padr_paises) # Exibe estatisticas dos dados com a técnica ja aplicada
```


Com os dados escalados vamos utilizar o Elbow Method para definir a quantidade de clusters
```{r}
wss <- (nrow(Padr_paises )-1)*sum(apply(Padr_paises ,2,var))
for (i in 2:15) wss[i] <- sum(kmeans(Padr_paises ,iter.max=100,
                                     centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares") 
```


Dada a curva, vamos seguir com 5 clusters para a criação de grupos. Agora vamos criar os grupos e entender sua representação de forma gráfica:

```{r}
#install.packages("tclust")
library(tclust)
clus_teste <- tkmeans(Padr_paises , k = 5, alpha = 0.01)
plot(clus_teste)
```


O R também fornece por padrão o algoritimo kmeans, vamos utiliza-lo também para verificar em qual cluster cada pais se encontra e ainda por final entender quantos paises estão dentro de cada cluster:

```{r}
#attach(Padr_paises)
set.seed(333)
output_cluster<-kmeans(Padr_paises,5,iter=100)
output_cluster
segmento<-output_cluster$cluster
table (segmento)
```

Com a clusterização feita, gostaria de mostrar uma forma um pouco mais visivel de enxergar os grupos

```{r}
#install.packages("cluster")
library(cluster)
clusplot(Padr_paises, output_cluster$cluster, color=TRUE, shade=TRUE,
         labels=2, lines=0 , cex=0.75)
```



Nesse ponto já temos todos os paises devidamente agrupados com seus "semelhantes". Desse ponto em diante poderiamos definir uma série de próximos passos mas essa analise se limita a clusterização.










