my_RF <- function(dataset, max_cov, rf_ntree){
  
  library(randomForest)
  set.seed(789)
  
  rf <- randomForest(goal_YN ~ . ,
                       data=dataset,
                     xtest=dat_test %>% dplyr::select(!goal_YN),
                     ytest=dat_test %>% dplyr::pull(goal_YN),
                       mtry=max_cov, ntree=rf_ntree,
                     importance=T)
  
  return(list(rf=rf))
}