setwd("C:/Users/eleoc/Desktop/WORK/Y3S1")

# Libraries

library(dplyr)
library(ggplot2)

rm(list = ls())
rm()

# Import data

youtube = read.csv('Project\\youtubesenttitle.csv')

# Add weekdays

youtube <- youtube %>%
  mutate(publish_day = weekdays(as.Date(publish_time)))

# Add HDI

youtube <- youtube %>%
  mutate(country_HDI = case_when(country_code == 'CA' ~ 0.929,
                                 country_code == 'DE' ~ 0.947,
                                 country_code == 'FR' ~ 0.901,
                                 country_code == 'GB' ~ 0.932,
                                 country_code == 'IN' ~ 0.645,
                                 country_code == 'JP' ~ 0.919,
                                 country_code == 'KR' ~ 0.916,
                                 country_code == 'MX' ~ 0.779,
                                 country_code == 'RU' ~ 0.824,
                                 country_code == 'US' ~ 0.926,
                                 TRUE ~ 0)) %>%
  mutate(country_IHDI = case_when(country_code == 'CA' ~ 0.848,
                                 country_code == 'DE' ~ 0.869,
                                 country_code == 'FR' ~ 0.820,
                                 country_code == 'GB' ~ 0.856,
                                 country_code == 'IN' ~ 0.475,
                                 country_code == 'JP' ~ 0.843,
                                 country_code == 'KR' ~ 0.815,
                                 country_code == 'MX' ~ 0.613,
                                 country_code == 'RU' ~ 0.740,
                                 country_code == 'US' ~ 0.808,
                                 TRUE ~ 0)) %>%
  mutate(country_happiness = case_when(country_code == 'CA' ~ 7.103,
                                 country_code == 'DE' ~ 7.155,
                                 country_code == 'FR' ~ 6.69,
                                 country_code == 'GB' ~ 7.064,
                                 country_code == 'IN' ~ 3.819,
                                 country_code == 'JP' ~ 5.94,
                                 country_code == 'KR' ~ 5.845,
                                 country_code == 'MX' ~ 6.317,
                                 country_code == 'RU' ~ 5.477,
                                 country_code == 'US' ~ 6.951,
                                 TRUE ~ 0))

youtube_num <- data.matrix(select(youtube,10,11,12,13,21,26,27,28))

# Plots

youtube %>%
  filter(country_code == 'FR' & category_title == 'Gaming') %>%
  ggplot(aes(x=likes)) +
  geom_line(aes(y = title.polarity), color = "darkred") 

youtube %>%
  filter(country_code == 'FR' & category_title == 'Gaming') %>%
  ggplot(aes(x=title.polarity)) +
  geom_histogram(fill = "darkred", color = 'black')

youtube %>%
  filter(country_code == 'FR' & category_title == 'Gaming') %>%
  ggplot(aes(x=publish_day)) +
  geom_histogram(fill = "darkred", color = 'black', stat = 'count')

youtube %>%
  ggplot(aes(x=likes)) +
  geom_line(aes(y = title.polarity), color = "darkred")

youtube %>%
  ggplot(aes(x=title.polarity)) +
  geom_histogram(fill = "darkred", color = 'black')

youtube %>%
  ggplot(aes(x=publish_day)) +
  geom_histogram(fill = "darkred", color = 'black', stat = 'count')

heatmap(youtube_num)
