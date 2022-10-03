# Setting working directory

setwd("C:/Users/eleoc/Desktop/WORK/Y3S1")

# Loading libraries

library(dplyr)
library(networkD3)
library(circlize)
library(tidyr)
library(corrplot)

# Cleaner

rm(list=ls())
rm()

# Importing data

audit = read.csv('Social Network Analysis\\Auditions.db.comp.csv')

# Creating subsets

audit_sub1 = filter(audit, year == 2017 & status == 'interne')
audit_sub2 = filter(audit, year == 2017 & status == 'externe')
audit_sub3 = filter(audit, year == 2018 & status == 'interne')
audit_sub4 = filter(audit, year == 2018 & status == 'externe')
audit_sub5 = filter(audit, year == 2019 & status == 'interne')
audit_sub6 = filter(audit, year == 2019 & status == 'externe')
audit_sub7 = filter(audit, year == 2020 & status == 'interne')
audit_sub8 = filter(audit, year == 2020 & status == 'externe')

#Subset and beyond

audit_sub1_edge <- audit_sub1 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub2_edge <- audit_sub2 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub3_edge <- audit_sub3 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub4_edge <- audit_sub4 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub5_edge <- audit_sub5 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub6_edge <- audit_sub6 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub7_edge <- audit_sub7 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

audit_sub8_edge <- audit_sub8 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

# Creating networks

simpleNetwork(audit_sub1_edge)
simpleNetwork(audit_sub2_edge)
simpleNetwork(audit_sub3_edge)
simpleNetwork(audit_sub4_edge)
simpleNetwork(audit_sub5_edge)
simpleNetwork(audit_sub6_edge)
simpleNetwork(audit_sub7_edge)
simpleNetwork(audit_sub8_edge) %>%
  saveNetwork(file = 'file.html')

# Network of all externals

audit_sub9 = filter(audit, status == 'externe')

audit_sub9_edge <- audit_sub9 %>%
  select(n_poste, Name) %>%
  inner_join(., select(., n_poste, Name), by = "n_poste") %>%
  rename(name1 = Name.x, name2 = Name.y) %>%
  filter(name1 != name2) %>%
  unique %>%
  arrange(n_poste) %>%
  select(2,3)

simpleNetwork(audit_sub9_edge)

# Counting NAs in Level

sum(is.na(audit$Level))

# CHORD diagram

school <- c('CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','CY Tech','Howest','Gothenburg','Singidunum','Singidunum')
student <- c('Sarvesh','Neha','Amr','Khushi','Anh Thu','Yasmine','Buu','Maxime','Gabriel','Aya','Maxime','Rodolphe','Gwénaëlle','Casper','Andreas','Zuk','Johann')
university <- c('Gothenburg','Gothenburg','Gothenburg','Gothenburg','Gothenburg','Howest','Howest','Howest','Howest','Howest','Reutlingen','Reutlingen','VUB','CY Tech','CY Tech','CY Tech','CY Tech')
data <- data.frame(student, university)
adjacencyData <- with(data, table(school, university))
par(cex = 2)
chordDiagram(adjacencyData, transparency = 0.5)

# Sankey diagram

links <- data.frame(
  source=c("group_A","group_A", "group_B", "group_C", "group_C", "group_E"), 
  target=c("group_C","group_D", "group_E", "group_F", "group_G", "group_H"), 
  value=c(2,3, 2, 3, 1, 3))

nodes <- data.frame(
  name=c(as.character(links$source), 
         as.character(links$target)) %>% unique())

links$IDsource <- match(links$source, nodes$name)-1 
links$IDtarget <- match(links$target, nodes$name)-1

p <- sankeyNetwork(Links = links, Nodes = nodes,
                   Source = "IDsource", Target = "IDtarget",
                   Value = "value", NodeID = "name", 
                   sinksRight=FALSE)
p

# MBA

tel = read.csv('Social Network Analysis\\tel_samp_rec.csv')

tel <- tel %>% 
  drop_na(disc1.rec.lev1)


