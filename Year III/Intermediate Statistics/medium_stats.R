# Setting working directory

setwd("C:/Users/eleoc/Desktop/WORK/Y3S1")

# Loading libraries

library(plyr)
library(dplyr)
library(ggplot2)
library(bbplot)
library(ggrepel)
library(forcats)
library(scales)
library(xtable)
library(MASS)
library(caret)
library(leaps)
library(klaR)
library(graphics)
library(questionr)
library(finalfit)
library(moonBook)
library(survival)
library(ranger)
library(ggfortify)
library(survminer)

# Cleaner

rm(list=ls())
rm()

# Importing data

quest1 = read.csv('Intermediate Statistics\\data\\effec1.quest.compil.csv')
quest2 = read.csv('Intermediate Statistics\\data\\effec2.quest.compil.csv')
quest3 = read.csv('Intermediate Statistics\\data\\effec3.quest.compil.csv')
usage1 = read.csv('Intermediate Statistics\\data\\usages.effec1.csv')
usage2 = read.csv('Intermediate Statistics\\data\\usages.effec2.csv')
usage3 = read.csv('Intermediate Statistics\\data\\usages.effec3.csv')

# Adding a column specifying from which file the data comes for quest

quest1$quest1 = 1
quest2$quest2 = 1
quest3$quest3 = 1

# Same for usage

usage1$usage1 = 1
usage2$usage2 = 1
usage3$usage3 = 1

# Merging the data sets together

quest_subtotal <- rbind.fill(quest1,quest2)
quest_total <- rbind.fill(quest_subtotal,quest3)
usage_subtotal <- rbind.fill(usage1,usage2)
usage_total <- rbind.fill(usage_subtotal,usage3)
complete_dataset <- rbind.fill(quest_total,usage_total)

# Merging the duplicate IDs

cleaned_dataset <- complete_dataset %>%
  arrange(Student_ID, desc(Student_ID)) %>%
  group_by(Student_ID) %>%
  summarise_all(funs(first(.[!is.na(.)]))) %>%
  ungroup()

# Getting familiar with the data

colnames(cleaned_dataset)
max(cleaned_dataset$last.video,na.rm=TRUE)
sum(duplicated(cleaned_dataset$Student_ID))

# Isolating the various behaviors

level_completers <- filter(cleaned_dataset,Exam.bin == 1)
level_disengaging_learners <- filter(cleaned_dataset, (Exam.bin == 0 | is.na(Exam.bin) == TRUE) & (Assignment.bin == 1 | Quizz.1.bin == 1 | Quizz.2.bin == 1 | Quizz.3.bin == 1 | Quizz.4.bin == 1 | Quizz.5.bin == 1))
level_auditing_learners <- filter(cleaned_dataset, (Exam.bin == 0 | is.na(Exam.bin) == TRUE) & (Assignment.bin == 0 | is.na(Assignment.bin) == TRUE) & (Quizz.1.bin == 0 | is.na(Quizz.1.bin) == TRUE) & (Quizz.2.bin == 0 | is.na(Quizz.2.bin) == TRUE) & (Quizz.3.bin == 0 | is.na(Quizz.3.bin) == TRUE) & (Quizz.4.bin == 0 | is.na(Quizz.4.bin) == TRUE) & (Quizz.5.bin == 0 | is.na(Quizz.5.bin) == TRUE) & last.video >= 3.5)
level_bystanders <- filter(cleaned_dataset, (Exam.bin == 0 | is.na(Exam.bin) == TRUE) & (Assignment.bin == 0 | is.na(Assignment.bin) == TRUE) & (Quizz.1.bin == 0 | is.na(Quizz.1.bin) == TRUE) & (Quizz.2.bin == 0 | is.na(Quizz.2.bin) == TRUE) & (Quizz.3.bin == 0 | is.na(Quizz.3.bin) == TRUE) & (Quizz.4.bin == 0 | is.na(Quizz.4.bin) == TRUE) & (Quizz.5.bin == 0 | is.na(Quizz.5.bin) == TRUE) & (last.video <= 3.5 | is.na(last.video) == TRUE))

# Pie chart of the proportion of each type of learner

levels_count <- c(nrow(level_completers),nrow(level_disengaging_learners),nrow(level_auditing_learners),nrow(level_bystanders))
levels <- data.frame(group=c('Completers','Disengaging Learners','Auditing Learners','Bystanders'),value=levels_count)

pie <- ggplot(levels, aes(x = "", y = value, fill = group)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y") +
  geom_label_repel(aes(label = percent(value / sum(value))), size=5, show.legend = F, position='identity') +
  guides(fill = guide_legend(title = "Learner Behavior"))

pie

# T-Test for Gender and videos

cleaned_dataset$videos <- rowSums(cleaned_dataset[63:97],na.rm=T)

cleaned_dataset <- cleaned_dataset %>%
  group_by(Gender) %>%
  mutate(videos_by_gender = mean(videos))

lm(videos ~ Gender, data = cleaned_dataset) %>%
  xtable()

# ANOVA for Country_HDI.fin and videos

cleaned_dataset <- cleaned_dataset %>%
  group_by(Country_HDI.fin) %>%
  mutate(videos_by_HDI = mean(videos))

cleaned_dataset_for_HDI <- cleaned_dataset[!is.na(cleaned_dataset$Country_HDI.fin),]

summary(aov(videos ~ Country_HDI.fin, data = cleaned_dataset_for_HDI)) %>%
  xtable()

# Making an ANOVA table

anova(lm(videos ~ Gender + Country_HDI.fin + CSP, data = cleaned_dataset)) %>%
  xtable()

# Dealing with age

cleaned_dataset$birth.year <- as.numeric(cleaned_dataset$birth.year)
cleaned_dataset$age = 2014 - cleaned_dataset$birth.year

cleaned_dataset <- cleaned_dataset %>%
  mutate(age = case_when(age < 0 ~ NA_real_, age > 100 ~ NA_real_, TRUE ~ age))

cleaned_dataset <- cleaned_dataset %>%
  mutate(age_class = cut(age,breaks = c(20,30,40,50,60,70,80,90,100)))

# Tukey HSD

TukeyHSD(aov(videos ~ Gender + Country_HDI.fin + CSP + age_class, data = cleaned_dataset))

# Model update

anova(lm(videos ~ Gender + Country_HDI.fin + CSP + Gender*Country_HDI.fin, data = cleaned_dataset)) %>%
  xtable()

# Step wise regression using MASS

nona.data <- na.omit(dplyr::select(cleaned_dataset,2,7,33,126))

model1 <- lm(videos ~ Gender + Country_HDI.fin + CSP, data = nona.data)
step.model1 <- stepAIC(model1, direction = "both", trace = FALSE)

summary(step.model1)

# Step wise regression using caret

train.control <- trainControl(method = "cv", number = 10)

step.model2 <- train(videos ~ Gender + Country_HDI.fin + CSP, data = nona.data, method = "lmStepAIC", trControl = train.control, trace = FALSE)

summary(step.model2$finalModel)

# Step wise model accuracy

train.control <- trainControl(method = "boot", number = 100)
train(videos ~ Gender + Country_HDI.fin + CSP, data = nona.data, method = "nb", trControl = train.control)

# Chi-test and mosaic plots

chisq.test(nona.data$Gender,nona.data$Country_HDI.fin)
chisq.test(nona.data$Gender,nona.data$CSP)
chisq.test(nona.data$CSP,nona.data$Country_HDI.fin)

mosaicplot(~ Gender + Country_HDI.fin, data = nona.data, shade = TRUE, las=2, main = "Gender and Country HDI")
mosaicplot(~ Gender + CSP, data = nona.data, shade = TRUE, las=2, main = "Gender and Socioeconomic Status")
mosaicplot(~ CSP + Country_HDI.fin, data = nona.data, shade = TRUE, las=2, main = "Socioeconomic Status and Country HDI")

# Tukey HSD

turkey <- TukeyHSD(aov(videos ~ Gender + Country_HDI.fin + CSP, data = cleaned_dataset))
as.data.frame(turkey[3]) %>%
  xtable()

# Logistic regression

glm = glm(Exam.bin ~ Gender + Country_HDI.fin, data = cleaned_dataset, family=binomial)

glm %>%
  coef() %>%
  exp()

# Odds ratio and plot

odds.ratio(glm) %>%
  xtable()

or_plot(cleaned_dataset, explanatory = c("Gender","Country_HDI.fin"), dependent = "Exam.bin", glmfit = glm)

ORplot(glm,type=1,show.CI=TRUE)

# Poisson

glmPoisson = glm(videos ~ Gender + Country_HDI.fin, data = cleaned_dataset, family=poisson)

# QQ Plot

qqnorm(cleaned_dataset$videos, pch = 1, frame = FALSE)
qqline(cleaned_dataset$videos, col = "steelblue", lwd = 2)

# Fixing Country HDI

cleaned_dataset$Country_HDI.fin <- as.factor(cleaned_dataset$Country_HDI.fin)

# Survival analysis

cleaned_dataset <- cleaned_dataset %>%
  mutate(videos_percent = (videos / 35) * 100) %>%
  mutate(deciles = round_any(videos_percent,10,f=ceiling)) %>%
  mutate(status = case_when(deciles == 100 ~ 0, TRUE ~ 1))

survival_fit <- survfit(Surv(deciles,status) ~ Diploma, data = cleaned_dataset)

ggsurvplot(survival_fit)
