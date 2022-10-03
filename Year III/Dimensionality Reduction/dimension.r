setwd("C:/Users/eleoc/Desktop/WORK/Y3S1")

# Libraries

library(corrplot)
library(gginference)
library(dplyr)
library(ggplot2)
library(factoextra)
library(stats)
library(FactoMineR)

rm(list=ls())
rm()

# Import data

users = read.csv('Dimensionality Reduction\\users.db.csv')

# Create a correlation plot of all variables except for dates

users_num <- mutate_all(users, function(x) as.numeric(as.character(x)))
users_num$date.crea <- NULL
users_num$last.connex <- NULL
users_num$last.up.photo <- NULL
users_num$last.pr.update <- NULL
corrplot(cor(users_num),method = 'number')

# Compute date difference between last connection and last picture upload

users$date_diff1 <- as.Date(as.character(users$last.connex), format="%Y-%m-%d")-
  as.Date(as.character(users$last.up.photo), format="%Y-%m-%d")

users$date_diff1_num <- as.numeric(users$date_diff1, units="days")

# Logging the score

users$score_logged <- log(users$score)

# Correlation parameter photo.keke and gender

summary(lm(score_logged ~ photo.keke * gender, data = users))

keke <- select(users,15,19)

keke <- keke %>%
  group_by(photo.keke) %>%
  mutate(mean = mean(score_logged)) %>%
  mutate(sd = sd(score_logged)/2)

superior_keke <- unique(select(keke,1,3,4))

ggplot(superior_keke) +
  geom_bar(aes(x=photo.keke, y=mean), stat="identity", fill="skyblue", alpha=0.7) +
  geom_errorbar(aes(x=photo.keke, ymin=mean-sd, ymax=mean+sd), 
                width=0.4, colour="orange", alpha=0.9, size=1.3) + 
  labs(title = "Mean and standard deviation of score based on whether you're a keke or not")

keke2 <- select(users,10,15,19)

keke2 <- keke2 %>%
  group_by(photo.keke,gender) %>%
  mutate(mean = mean(score_logged)) %>%
  mutate(sd = sd(score_logged)/2)

superior_keke2 <- keke2 %>%
  filter(!duplicated(mean))

superior_keke2 <- select(superior_keke2,1,2,4,5)

ggplot(data=superior_keke2, aes(fill = as.factor(gender),x=photo.keke, y=mean)) +
  geom_bar(position = "dodge" ,stat="identity") +
  geom_errorbar( aes(x=photo.keke, ymin=mean-sd, ymax=mean+sd),position=position_dodge(width=0.9), colour="orange", alpha=0.9, size=0.8) + 
  labs(title = "Mean and standard deviation of score based on kekeness and gender")

# PCA

PCA <- prcomp(users_num, scale = TRUE)
PCA$rotation

fviz_pca_ind(PCA,col.ind = "cos2",gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),repel = TRUE)

fviz_pca_var(PCA, col.var="contrib")+scale_color_gradient2(low="#00AFBB", mid="#E7B800",high="#FC4E07", midpoint=96) +
  theme_minimal()

screeplot(PCA)


users_choice <- select(users_num,2,3,4,5,7,8)

HCPC(users_choice)

HCPC <- HCPC(users_choice)
plot(HCPC, choice = '3D.map')

PCA <- prcomp(users_choice, scale = TRUE)
PCA$rotation

fviz_pca_ind(PCA,col.ind = "cos2",gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),repel = TRUE)

fviz_pca_var(PCA, col.var="contrib")+scale_color_gradient2(low="#00AFBB", mid="#E7B800",high="#FC4E07", midpoint=96) +
  theme_minimal()

screeplot(PCA)

# Correlation test

cor.test(users_num$score, users_num$n.matches, method = "pearson")
