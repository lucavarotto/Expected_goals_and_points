rm(list=ls())
gc()

load("../Dataset_ausiliari/dat_cleaned.Rdata")
load("../Dataset_ausiliari/dat_test.Rdata")

cm_and_fscore <- function(probs){
  library(yardstick)
  library(pROC)
  my_roc <- roc(dat_test$goal_YN, probs)
  auc <- pROC::auc(my_roc)
  cat("AUC:", auc, "\n\n")
  threshold <- coords(my_roc, "best", ret = "threshold",
                      best.method="closest.topleft", best.weights=c(1,mean(dat_test$goal_YN==1))) %>% as.numeric()
  
  cat("Soglia:", threshold, "\n\n")
  
  cat("\n-------------------------")
  Fitted_goal <-  ifelse(probs >= threshold, 1, 0)
  
  f_score <- tibble(t=as.factor(dat_test$goal_YN),
                    e=factor(Fitted_goal, levels=c(0,1))) %>% f_meas(truth=t,
                                                                     estimate=e, event_level = "second") %>% dplyr::select(.estimate) %>% as.numeric()
  cat("f-score:", f_score, "\n\n")
  
  caret::confusionMatrix(data=as.factor(Fitted_goal), reference=as.factor(dat_test$goal_YN))
}

library(nnet)
x_matrix <- model.matrix(goal_YN~.-1, data=dat_cleaned)
x_matrix_t <- model.matrix(goal_YN~.-1, data=dat_test)

nn <- nnet(x=x_matrix,
    y=(dat_cleaned %>% dplyr::pull(goal_YN) %>% as.numeric())-1,
    size=30, linout=F, entropy=T,
    maxit=200)

cm_and_fscore(predict(nn, x_matrix_t, type="raw") %>% as.numeric())

