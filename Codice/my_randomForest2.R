cv_random_forest <- function(train, hp_list, test, n_folds){
  
  library(superml)
  
  rf <- RFTrainer$new(classification=1,
                      min_node_size=1)
  
  rf_cv <-GridSearchCV$new(trainer = rf,
                         parameters = hp_list,
                         n_folds = n_folds,
                         scoring = c("f1"))
  
  rf_cv$fit(train, "goal_YN")
  hp_best <- rf_cv$best_iteration()
  
  rf_best <- RFTrainer$new(n_estimator=hp_best[["n_estimators"]],
                           max_depth=hp_best[["max_depth"]],
                           classification=1,
                           max_features=hp_best[["max_features"]],
                           min_node_size=1,
                           seed=123,
                           verbose=TRUE)
  
  rf_best$fit(train, "goal_YN")
  predictions <- rf_best$predict(test)
  
  return( list(pred=predictions, rf=rf_best, hp=hp_best) )
}

