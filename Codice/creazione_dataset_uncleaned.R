rm(list=ls())
create_home_dummy <- function(dataset, results){
  
  dataset <- left_join(dataset,
                       results %>% dplyr::select(match_id, home_team, away_team),
                       by=join_by(match_id==match_id))
  
  dataset$home <- NA
  for (i in 1:nrow(dataset)){
    if (dataset[i,"team"]==dataset[i,"home_team"]){
      dataset[i,"home"] <- "Yes"}
    else { dataset[i,"home"] <- "No"}
  }
  
  dataset <- dataset %>% dplyr::select(!home_team)
  dataset <- dataset %>% dplyr::select(!away_team)
  
  return(dataset)
}


dat1 <- read.csv("../creazione_dataset/matches_data/Premier_shots_2015_2016.csv")
dat1[dat1 == ""] <- FALSE
head(dat1,10)

res1 <- read_csv("../creazione_dataset/games_results/premier_2015_16_games_results.csv")
dat1 <- create_home_dummy(dat1, res1)

dat2 <- read.csv("../creazione_dataset/matches_data/Liga_shots_2015_2016.csv")
dat2[dat2 == ""] <- FALSE
res2 <- read_csv("../creazione_dataset/games_results/Liga_2015_16_games_results.csv")
dat2 <- create_home_dummy(dat2, res2)

dat3 <- read.csv("../creazione_dataset/matches_data/Ligue1_shots_2015_2016.csv")
dat3[dat3 == ""] <- FALSE
res3 <- read_csv("../creazione_dataset/games_results/Ligue1_2015_16_games_results.csv")
dat3 <- create_home_dummy(dat3, res3)

dat4 <- read.csv("../creazione_dataset/matches_data/Bundes_shots_2015_2016.csv")
dat4[dat4 == ""] <- FALSE
res4 <- read_csv("../creazione_dataset/games_results/Bundes_2015_16_games_results.csv")
dat4 <- create_home_dummy(dat4, res4)

dat5 <- read.csv("../creazione_dataset/matches_data/WC_shots_2022.csv")
dat5[dat5 == ""] <- FALSE
dat5$home <- "Neutral"

dat6 <- read.csv("../creazione_dataset/matches_data/WC_shots_2018.csv")
dat6[dat6 == ""] <- FALSE
dat6$home <- "Neutral"

dat7 <- read.csv("../creazione_dataset/matches_data/EURO_shots_2020.csv")
dat7[dat7 == ""] <- FALSE
dat7$home <- "Neutral"

dat8 <- read.csv("../creazione_dataset/matches_data/EURO_shots_2024.csv")
dat8[dat8 == ""] <- FALSE
dat8$home <- "Neutral"

dat9 <- read.csv("../creazione_dataset/matches_data/CAF_shots_2023.csv")
dat9[dat9 == ""] <- FALSE
dat9$home <- "Neutral"

dat <- rbind(dat1, dat2, dat3, dat4, dat5, dat6, dat7, dat8, dat9)

save(dat, file="../Dataset_ausiliari/dat_uncleaned.Rdata")