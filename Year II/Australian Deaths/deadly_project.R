library(dplyr)
library(ggplot2)
install.packages('BiocManager')
if(!require(pacman))install.packages("pacman")
pacman::p_load('dplyr','tidyr','gapminder','ggplot2','ggalt','forcats','R.utils','png','grid','ggpubr','scales','bbplot')
install.packages('devtools')
devtools::install_github('bbc/bbplot')


install.packages("installr")
library(installr)
updateR()


# List of all causes

causes <- grimdatagovau %>%
  group_by(cause_of_death) %>%
  summarise()

# Pie chart of the proportion of natural deaths

non_natural <- grimdatagovau %>%
  filter(!is.na(deaths)) %>%
  filter(cause_of_death != "All causes combined (ICD-10 all)" & AGE_GROUP != "Total" & SEX != "Persons") %>%
  filter(grepl('Accident|Assault|Suicide|accident',cause_of_death))

natural <- grimdatagovau %>%
  filter(!is.na(deaths)) %>%
  filter(cause_of_death != "All causes combined (ICD-10 all)" & AGE_GROUP != "Total" & SEX != "Persons") %>%
  filter(!grepl('Accident|Assault|Suicide|accident',cause_of_death))

x <- sum(non_natural$deaths, na.rm = TRUE)  
y <- sum(natural$deaths, na.rm = TRUE) 

naturality <- data.frame(group=c("Non natural","Natural"),value=c(x,y))

pie <- ggplot(naturality,aes(x="", y=value, fill=group))+
  geom_bar(width = 1, stat = "identity")+
  coord_polar("y", start=0)+
  bbc_style()+
  theme(legend.position = "bottom",axis.text.x=element_blank(),axis.ticks=element_blank(),panel.grid=element_blank())

pie

# Counting the non natural causes

acc_drown <- grimdatagovau %>%
  filter(cause_of_death == "Accidental drowning (ICD-10 W65-W74)" & AGE_GROUP != "Total" & SEX != "Persons")

acc_drown_value <- sum(acc_drown$deaths, na.rm = TRUE)

acc_pois <- grimdatagovau %>%
  filter(cause_of_death == "Accidental poisoning (ICD-10 X40-X49)" & AGE_GROUP != "Total" & SEX != "Persons")

acc_pois_value <- sum(acc_pois$deaths, na.rm = TRUE)

acc_pois_2 <- grimdatagovau %>%
  filter(cause_of_death == "Accidental poisoning, including drugs causing adverse effects in therapeutic use (ICD-10 X40-X49, Y40-Y59)" & AGE_GROUP != "Total" & SEX != "Persons")

acc_pois_2_value <- sum(acc_pois_2$deaths, na.rm = TRUE)

ass <- grimdatagovau %>%
  filter(cause_of_death == "Assault (ICD-10 X85-Y09)" & AGE_GROUP != "Total" & SEX != "Persons")

ass_value <- sum(ass$deaths, na.rm = TRUE)

land <- grimdatagovau %>%
  filter(cause_of_death == "Land transport accidents (ICD-10 V01-V89)" & AGE_GROUP != "Total" & SEX != "Persons")

land_value <- sum(land$deaths, na.rm = TRUE)

suic <- grimdatagovau %>%
  filter(cause_of_death == "Suicide (ICD-10 X60-X84, Y87.0)" & AGE_GROUP != "Total" & SEX != "Persons")

suic_value <- sum(suic$deaths, na.rm = TRUE)

# Sum of the non natural deaths

total_non_natural <- acc_drown_value + acc_pois_value + acc_pois_2_value + ass_value + land_value + suic_value

# Cleaning and sum

cleaned <- grimdatagovau %>%
  filter(!is.na(deaths)) %>%
  filter(cause_of_death != "All causes combined (ICD-10 all)" & AGE_GROUP != "Total" & SEX != "Persons")

cleaned_value <- sum(cleaned$deaths, na.rm = TRUE)

all_causes <- grimdatagovau %>%
  filter(!is.na(deaths)) %>%
  filter(cause_of_death == "All causes combined (ICD-10 all)" & AGE_GROUP != "Total" & SEX != "Persons")

all_causes_value <- sum(all_causes$deaths, na.rm = TRUE)

# Pie chart of the different non natural causes

non_naturality <- data.frame(group=c("Accidental drowning","Accidental poisoning","Accidental poisoning including drugs","Assault","Land vehicle accident","Suicide"),value=c(acc_drown_value,acc_pois_value,acc_pois_2_value,ass_value,land_value,suic_value))

pie2 <- ggplot(non_naturality,aes(x="", y=value, fill=group))+
  geom_bar(width = 1, stat = "identity")+
  coord_polar("y", start=0)+
  bbc_style()+
  theme(legend.position = "bottom",axis.text.x=element_blank(),axis.ticks=element_blank(),panel.grid=element_blank())+
  scale_y_continuous(labels = scales::comma)

pie2

# Studying the evolution of suicide

suic_evol <- grimdatagovau %>%
  filter(cause_of_death == "Suicide (ICD-10 X60-X84, Y87.0)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

graph <- ggplot(suic_evol, aes(x=suic_evol$YEAR, y=suic_evol$deaths)) +
  geom_line()+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)

graph

# The evolution of the proportion of suicides

total_evol <- grimdatagovau %>%
  filter(cause_of_death == "All causes combined (ICD-10 all)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

suic_prop <- data.frame(YEAR = total_evol$YEAR, suic_deaths = suic_evol$deaths, total_deaths = total_evol$deaths)

suic_prop$division <- suic_prop$suic_deaths / suic_prop$total_deaths
suic_prop$percentage <- 100*(suic_prop$division)
# suic_prop$percent <- sapply(suic_prop$percentage, function(x) as.numeric(gsub("%","",x)))

graph2 <- ggplot(suic_prop, aes(x=YEAR, y=percent)) +
  geom_line()+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)

graph2

graph3 <- ggplot(suic_evol, aes(x=suic_evol$YEAR, y=suic_evol$deaths)) +
  geom_histogram(stat="identity")+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)

graph3

graph4 <- ggplot(suic_prop, aes(x=YEAR, y=percent)) +
  geom_histogram(stat="identity")+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)

graph4

# Let's look at all the non-natural causes

land_evol <- grimdatagovau %>%
  filter(cause_of_death == "Land transport accidents (ICD-10 V01-V89)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
#  filter(!is.na(deaths)) %>%
  summarise()

assa_evol <- grimdatagovau %>%
  filter(cause_of_death == "Assault (ICD-10 X85-Y09)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

pois2_evol <- grimdatagovau %>%
  filter(cause_of_death == "Accidental poisoning, including drugs causing adverse effects in therapeutic use (ICD-10 X40-X49, Y40-Y59)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

pois_evol <- grimdatagovau %>%
  filter(cause_of_death == "Accidental poisoning (ICD-10 X40-X49)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

drow_evol <- grimdatagovau %>%
  filter(cause_of_death == "Accidental drowning (ICD-10 W65-W74)" & AGE_GROUP == "Total" & SEX == "Persons") %>%
  group_by(YEAR, deaths) %>%
  summarise()

combined_evol <- data.frame(YEAR = suic_evol$YEAR, Suicide = suic_evol$deaths, Land_vehicle_accident = land_evol$deaths, Assault = assa_evol$deaths, Accidental_poisoning_including_drugs = pois2_evol$deaths, Accidental_poisoning = pois_evol$deaths, Accidental_drowning = drow_evol$deaths)

graph5 <- ggplot(combined_evol, aes(x=YEAR)) +
  geom_line(aes(y = Suicide, color = "purple"))+
  geom_line(aes(y = Land_vehicle_accident, color = "blue"))+
  geom_line(aes(y = Assault, color = "cyan"))+
  geom_line(aes(y = Accidental_poisoning_including_drugs, color = "green"))+
  geom_line(aes(y = Accidental_poisoning, color = "brown"))+
  geom_line(aes(y = Accidental_drowning, color = "red"))+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)+
  scale_color_identity(name = "Causes",
                       breaks = c("purple","blue","cyan","green","brown","red"),
                       labels = c("Suicide","Land vehicle accident","Assault","Accidental poisoning w/ drugs","Accidental poisoning","Accidental drowning"),
                       guide = "legend")

graph5

# All non-natural causes, but percentage

combined_evol$Total <- total_evol$deaths
combined_evol$percentSuicide <- 100*(combined_evol$Suicide/combined_evol$Total)
combined_evol$percentLand <- 100*(combined_evol$Land_vehicle_accident/combined_evol$Total)
combined_evol$percentAssault <- 100*(combined_evol$Assault/combined_evol$Total)
combined_evol$percentPois2 <- 100*(combined_evol$Accidental_poisoning_including_drugs/combined_evol$Total)
combined_evol$percentPois <- 100*(combined_evol$Accidental_poisoning/combined_evol$Total)
combined_evol$percentDrown <- 100*(combined_evol$Accidental_drowning/combined_evol$Total)

graph6 <- ggplot(combined_evol, aes(x=YEAR)) +
  geom_line(aes(y = percentSuicide, color = "purple"))+
  geom_line(aes(y = percentLand, color = "blue"))+
  geom_line(aes(y = percentAssault, color = "cyan"))+
  geom_line(aes(y = percentPois2, color = "green"))+
  geom_line(aes(y = percentPois, color = "brown"))+
  geom_line(aes(y = percentDrown, color = "red"))+
  bbc_style()+
  theme(legend.position = "bottom")+
  scale_y_continuous(labels = scales::comma)+
  scale_color_identity(name = "Causes",
                       breaks = c("purple","blue","cyan","green","brown","red"),
                       labels = c("Suicide","Land vehicle accident","Assault","Accidental poisoning w/ drugs","Accidental poisoning","Accidental drowning"),
                       guide = "legend")

graph6
