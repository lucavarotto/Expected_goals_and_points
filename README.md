# Expected Goals and Expected Points in Football

![R](https://img.shields.io/badge/R-glmnet%20%7C%20rpart%20%7C%20randomForest-276DC3?logo=r&logoColor=white)
![Python](https://img.shields.io/badge/Python-statsbombpy%20%7C%20imblearn-3776AB?logo=python&logoColor=white)
![StatsBomb](https://img.shields.io/badge/data-StatsBomb%20open%20data-E8344E)
![LaTeX](https://img.shields.io/badge/LaTeX-thesis-008080?logo=latex&logoColor=white)

An **Expected Goal** (xG) is the probability that a single shot ends up in the
net. Summing the xG of every shot a team takes measures the chances it created,
regardless of whether the ball went in: it separates merit from luck in a
result. An **Expected Point** (xP) pushes the idea to the scoreline, estimating
how many points a team would take on average if the same match were played
many times over.

This is my BSc thesis. It builds an xG model from scratch on 52,792 shots of
open StatsBomb data, compares seven classifiers across four ways of handling a
badly unbalanced response, and then uses the best of them to analyse a single
match and to recompute a whole league table in Expected Points, with Monte
Carlo simulation.

**Academic context.** *Applicazione di modelli di classificazione per la
valutazione delle prestazioni nel calcio: gli Expected Goals e gli Expected
Points*, BSc in *Statistics for Technology and Science*, University of Padua,
academic year 2023/2024, supervisor Prof. Manuela Cattelan. The thesis is in
Italian, and so are the comments in the code.

---

## The pipeline

Run the stages in order. Each script resolves its paths from its own location,
so the working directory does not matter.

| Stage | File | What it does |
| --- | --- | --- |
| 1. Scraping | `creazione_dataset/matches_lists/matches_lists_creation.py` | builds the match list of each competition from `statsbombpy` |
| | `creazione_dataset/matches_data/download_eventDATA.py` | downloads the event data of those matches and keeps the shots |
| | `creazione_dataset/games_results/get_season_results.py` | downloads the final results of every match |
| 2. Merge | `Codice/creazione_dataset_uncleaned.R` | stacks the ten competitions into one dataset of shots |
| 3. Cleaning and EDA | `Codice/analisi_esplorativa.Rmd` | drops the variables with too many missing values, turns the pitch coordinates into distance from goal and shot angle, explores the data, and writes the estimation, test, oversampled and undersampled datasets |
| 4. SMOTE-NC | `Codice/SMOTE_creation.Rmd`, `Codice/SMOTE_NC.py` | standardises the two quantitative variables and generates the synthetic minority observations |
| 5. Choice of `k` | `Codice/SMOTE_k_choice.Rmd`, `Codice/SMOTE_k_choice_scaled.Rmd` | compares the SMOTE-NC datasets built with `k` from 1 to 17 |
| 6. Models | `Codice/logistica_base.Rmd` | logistic regression on distance and angle only, the reference model |
| | `Codice/modellazione_originale.Rmd`, `_oversampled`, `_undersampled`, `_SMOTE`, `_SMOTE_scaled` | forward logistic, Lasso, Grouped Lasso and classification trees, one file per balancing technique |
| | `Codice/random_forest.Rmd`, `Codice/random_forest_2.Rmd` | random forests, with the helpers `my_randomForest.R` and `my_randomForest2.R` |
| | `Codice/NN.R` | a neural network, tried and left aside |
| 7. Applications | `Codice/single_match_analysis.Rmd` | shot map and cumulative xG of one match |
| | `Codice/Evaluation.Rmd` | Expected Points by Monte Carlo and the estimated league table |

---

## Repository structure

```
Expected_goals_and_points/
├── Codice/                          the analysis, one file per stage above
├── creazione_dataset/               the three scrapers (their output stays local)
├── Figures/                         figures produced by the .Rmd files
│   ├── analisi_esplorativa/
│   ├── logistica_base/
│   ├── mod_orig/  mod_oversampled/  mod_undersampled/  mod_SMOTE/
│   ├── RF/
│   └── single_match/
├── Report/
│   ├── Varotto_Luca.pdf             the thesis (Italian)
│   └── Varotto_Luca_presentazione.pdf
├── .gitignore
└── README.md
```

### What is not in this repository

**Neither the data nor the fitted models have been uploaded**, and of the
thesis only the PDF is here:

| Not published | What it is | Why |
| --- | --- | --- |
| `Dataset_ausiliari/` | the estimation, test and balanced datasets, 155 MB | regenerable from the scrapers and stages 2 to 4 |
| `RF_pred/` | the fitted random forests, 128 MB | regenerable by re-running stage 6 |
| the scrapers' output | match lists, event data and results, 16 MB | it is StatsBomb's data, free to download but not mine to redistribute |
| `Paper/` | the articles behind the method | works by other authors, cited in the thesis |
| the LaTeX source of the thesis | `.tex`, the template and its styles | of the thesis, only the PDF is published |
| `Codice/*.pdf` | the knitted output of the `.Rmd` files | regenerable by knitting them |

Together they are 319 MB of the 327 the project takes locally. To rebuild them,
run the pipeline from stage 1: the StatsBomb data is freely available through
`statsbombpy`.

---

## Results

### The data

Ten complete competitions of open StatsBomb data: the 2015/2016 seasons of
Premier League, Bundesliga, Ligue 1, La Liga and Serie A, the 2018 and 2022
World Cups, the 2020 and 2024 Euros and the 2023 Africa Cup of Nations. The
**9,998 shots of Serie A 2015/2016 are the test set**, the remaining **42,794
the estimation set**.

The response is heavily unbalanced: 4,573 goals against 38,221 misses, so
**10.7% positives**. Three variables were dropped for missingness — aerial duel
won (9.7%), one-on-one (26.2%) and empty goal (75.5%) — and the pitch
coordinates were turned into distance from the centre of the goal and shot
angle, which makes the model symmetric with respect to the middle of the pitch
and the coefficients readable.

### Seven models, four datasets

Each model was fitted on the unbalanced data and on three balanced versions,
random oversampling, pseudo-random undersampling and SMOTE-NC. The table
reports the best case of each model by F-score, with the classification
threshold chosen to maximise it.

| Model | Dataset | AUC | Threshold | F-score | Specificity | Sensitivity | Accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic, distance + angle | SMOTE-NC | 0.774 | 0.700 | 0.360 | 0.893 | 0.445 | 0.850 |
| **Logistic, forward** | **unbalanced** | 0.815 | 0.188 | **0.424** | **0.900** | 0.526 | **0.864** |
| Logistic, Lasso | SMOTE-NC | 0.812 | 0.424 | 0.422 | 0.892 | 0.543 | 0.859 |
| Logistic, Grouped Lasso | unbalanced | **0.816** | 0.158 | 0.418 | 0.880 | **0.567** | 0.850 |
| Tree, Gini | SMOTE-NC | 0.780 | 0.786 | 0.384 | 0.890 | 0.487 | 0.852 |
| Tree, cross-entropy | SMOTE-NC | 0.771 | 0.788 | 0.390 | 0.893 | 0.489 | 0.854 |
| Random forest | undersampled | 0.804 | 0.716 | 0.416 | 0.894 | 0.527 | 0.859 |

Three things stand out. SMOTE-NC wins in four of the seven rows, random
oversampling in none. The **best model overall is the plainest one**, a logistic
regression selected forward on the unbalanced data, which includes every
explanatory variable and beats both regularised versions and both tree-based
models on F-score. And no model gets anywhere near a sensitivity of 0.6: with
one shot in ten ending in a goal, half the goals are missed by any threshold
that keeps the false positives under control.

### One match

Napoli–Juventus, 26 September 2015, finished 2–1 for Napoli. Of the 26 shots,
14 by Napoli and 12 by Juventus, **only one passed the 0.188 threshold**, so the
model expected a single goal where three were scored. Summing the xG gives
**0.74 to Napoli and 1.16 to Juventus**, and the cumulative xG curve shows
Juventus creating barely 0.15 xG in the first half and about 1 in the second,
after conceding. By the model Juventus deserved more, and lost.

### A league table in Expected Points

Simulating each shot as a Bernoulli trial with its own xG, **B = 10,000** times
per match, gives the probability of each outcome. For Napoli–Juventus: 22.0%
Napoli, 31.2% draw, 46.8% Juventus, hence **0.973 xP against 1.715 xP**. Napoli
took 3 points and Juventus 0, so Juventus ended the match 1.7 points short of
what it deserved.

Repeated over the whole season, the estimated table disagrees with the real one
in ways worth noticing: Juventus won the league by 9 points but comes **second**
by xP, behind Napoli, 75.3 against 75.6; the three teams qualifying for the
Europa League are not the ones that qualified; and Frosinone, last in reality,
sits **13th** on Expected Points.

Both applications assume that shots are independent within a match, which is
not quite true, but is needed to keep the problem tractable.

---

## References

The full bibliography is in the thesis. The works it leans on most:

1. Robberechts, P., & Davis, J. (2020). *How data availability affects the
   ability to learn good xG models*.
2. Tippet, J. (2019). *The Expected Goals Philosophy: A Game-Changing Way of
   Analysing Football*.
3. Pollard, R., & Reep, C. (1997). *Measuring the effectiveness of playing
   strategies at soccer*.
4. StatsBomb open data, through the `statsbombpy` library.

---

## Author

**Luca Varotto** — BSc in Statistics for Technology and Science, University of
Padua, academic year 2023/2024. Supervisor Prof. Manuela Cattelan, Department
of Statistical Sciences.
