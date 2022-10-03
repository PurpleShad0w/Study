setwd("C:/Users/eleoc/Desktop/WORK/Y3S1")

# Loading libraries

library(dplyr)
library(lubridate)
library(ggplot2)
library(hrbrthemes)
library(viridis)
library(gender)
library(naniar)
library(missForest)

# Cleaner

rm(list=ls())
rm()

# Importing data

theses <- read.csv('Data Wrangling\\theses_v2.csv')

### Defense date ###
# Separating days, months and years

theses <- theses[!is.na(theses$Date.de.soutenance),]
theses$Date.de.soutenance <- as.Date(theses$Date.de.soutenance,format='%d-%m-%Y')
theses <- theses %>%
  mutate(Month = month(Date.de.soutenance)) %>%
  mutate(Day = day(Date.de.soutenance))

# Obtaining the monthly amount of theses

monthly <- theses %>%
  filter(!(Month == 1 & Day == 1)) %>%
  count(Month,Year)

# Removing the useless years

monthly <- monthly %>%
  filter(Year >= 2013 & Year != 2020)

# Computing the yearly percentages

monthly <- monthly %>%
  group_by(Year) %>% 
  mutate(percent = n/sum(n)*100)

# Obtaining the means and standard deviations of those percentages

monthly <- monthly %>%
  group_by(Month) %>%
  mutate(mean = mean(percent)) %>%
  mutate(sd = sd(percent))

# Collecting the data in a simpler matrix

superior_monthly <- unique(select(monthly,1,5,6))

# Plotting this data

graph <- ggplot(superior_monthly) +
  geom_bar(aes(x=Month, y=mean), stat="identity", fill="skyblue", alpha=0.7) +
  geom_errorbar(aes(x=Month, ymin=mean-sd, ymax=mean+sd), width=0.4, colour="orange", alpha=0.9, size=1.3)+
  theme_ipsum()

graph

### Languages ###
# Renaming the languages column

theses <- theses %>%
  rename(langage = Langue.de.la.these)

# Counting the languages

langages <- theses %>%
  count(langage,Year) %>%
  mutate(langage = case_when(langage == 'fr' ~ 'french', langage == 'en' ~ 'english', langage == 'fren' | langage == 'enfr' ~ 'bilingual', TRUE ~ 'others')) %>%
  group_by(langage,Year) %>%
  summarise(n = sum(n))

# Removing the useless years

langages <- langages %>%
  filter(Year >= 1988 & Year <= 2018)

# Plotting the data

graph2 <- ggplot(langages, aes(x=Year, y=n, fill=factor(langage, levels = c('french','bilingual','others','english')))) + 
  geom_area(position = position_stack(reverse = TRUE)) +
  labs(fill='Language') +
  scale_fill_viridis_d() +
  theme_ipsum()

graph2

### Genders ###

authors <- data.frame(as.character(theses$Auteur),theses$Year)

authors <- authors %>%
  rename(name = as.character.theses.Auteur.) %>%
  rename(year = theses.Year)

authors %>%
  rowwise() %>%
  mutate(gender = gender(name, method = 'kanterwitz'))

genders <- apply(authors$name, FUN = genderize, MARGIN = 1)

gender('maxime(',method = 'genderize')
dim(authors$name)

### Testing area ###


