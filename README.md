
# GROUP67_CENG313

CENG313 project based on the Kaggle competition **NeurIPS – Open Polymer Prediction 2025**.

- Competition: https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025
- Course organization: https://github.com/ceng313-2026
- Notebook for Assignment 1: [`assignment1_eda_baseline.ipynb`](assignment1_eda_baseline.ipynb) ([open in Colab](https://colab.research.google.com/github/ceng313-2026/GROUP67_CENG313/blob/main/assignment1_eda_baseline.ipynb))

## Team

| Name | Student ID | GitHub username |
| :--- | :--- | :--- |
| Yusuf Emin Acar | 23118080089 | [yusuf8886147](https://github.com/yusuf8886147) |

**Group ID:** 67 (individual group)

## Project Description

The goal of the competition is to predict five physical properties of polymers directly from their chemical structure, given as a SMILES string.

| Target | Property | Unit |
| :--- | :--- | :--- |
| `Tg` | Glass transition temperature | °C |
| `FFV` | Fractional free volume | dimensionless |
| `Tc` | Crystallization temperature | °C |
| `Density` | Polymer density | g/cm³ |
| `Rg` | Radius of gyration | Å |

Submissions are scored with a weighted MAE over the five targets (see the competition's Evaluation page). Since the competition is closed, we evaluate our models with a **held-out split (80% train / 20% test, `random_state=42`) of the labeled training data**, as allowed by the course instructions. Because the held-out split is not the official test set, our MAE/RMSE values are not directly comparable to the Kaggle leaderboard.

## Dataset

The data comes from the competition (`train.csv`, `test.csv`, `sample_submission.csv`). **Data files are not committed to this repository**; the notebook downloads them with the Kaggle API into `data/`.

`train.csv` contains 7,973 rows and 7 columns: `id`, `SMILES` and the five targets. Most target values are missing, because each polymer was measured for only a few properties:

| Column | Labeled rows | Missing (%) |
| :--- | ---: | ---: |
| `FFV` | 7,030 | 11.83 |
| `Tc` | 737 | 90.76 |
| `Rg` | 614 | 92.30 |
| `Density` | 613 | 92.31 |
| `Tg` | 511 | 93.59 |

Key observations from the EDA:

- Four of the five targets are labeled for fewer than 10% of the polymers, so each target has to be modeled on its own, much smaller subset.
- Only `FFV` has a large labeled set. `Tg`, `Density` and `Rg` have only a few hundred labeled samples each, so the test split for these targets is small and the metrics are noisy.
- The targets have very different scales (e.g. `Tg` in the tens to hundreds of °C vs. `FFV` around 0.3–0.4), so the errors can only be compared within the same target, and a weighted metric is needed for an overall score.
- Boxplots show outliers in several targets, which is why we avoid mean-based filling and why MAE is reported next to RMSE.

## Approach (Assignment 1: EDA and Baseline)

1. **EDA (`src/utils.py`)**: target distributions, correlation heatmap, missing value analysis and boxplots for outlier inspection.
2. **Preprocessing (`src/data.py`)**: target columns are **never imputed**. Filling them with the median would create synthetic labels and leak information into the evaluation. For each target, only the rows where that target is known are used for training and testing.
3. **Baseline models (`src/models.py`)**: three models are compared for each of the five targets:
   - Dummy Regressor (predicts the training mean),
   - Linear Regression,
   - Random Forest Regressor (`n_estimators=100`).

   The only feature used in this baseline is the **length of the SMILES string**. It is intentionally simple: it gives a reference point that the proposed solution in Assignment 2 has to beat.

## Results

Evaluation on the 20% held-out split, separately for each target (lower is better; best MAE per target in bold):

| Target | Model | MAE | RMSE |
| :--- | :--- | ---: | ---: |
| **Tg** | Dummy (Mean) | 81.1405 | 98.3658 |
| | Linear Regression | 78.1331 | 94.8620 |
| | Random Forest | **77.2824** | 95.8310 |
| **FFV** | Dummy (Mean) | 0.0215 | 0.0322 |
| | Linear Regression | 0.0209 | 0.0317 |
| | Random Forest | **0.0207** | 0.0316 |
| **Tc** | Dummy (Mean) | 0.0808 | 0.0925 |
| | Linear Regression | 0.0786 | 0.0922 |
| | Random Forest | **0.0681** | 0.0864 |
| **Density** | Dummy (Mean) | **0.1060** | 0.1325 |
| | Linear Regression | 0.1088 | 0.1353 |
| | Random Forest | 0.1084 | 0.1454 |
| **Rg** | Dummy (Mean) | 3.9269 | 4.7052 |
| | Linear Regression | 3.6387 | 4.5656 |
| | Random Forest | **3.6241** | 4.8020 |

### Discussion

- The SMILES length alone is a weak feature: compared with the mean predictor, the best model reduces MAE by only about 4.8% for `Tg`, 3.7% for `FFV` and 7.7% for `Rg`. The largest gain is for `Tc` (about 15.7%, Random Forest).
- For `Density`, neither Linear Regression nor Random Forest beats the mean predictor, which means that chain length carries almost no information about density.
- Random Forest has a lower MAE but a higher RMSE than the dummy model for `Density` and `Rg`. This suggests that it overfits the small labeled sets and makes some large errors.
- These results show that a string-length feature is not enough. For Assignment 2 we plan to use chemically meaningful features (e.g. RDKit molecular descriptors and fingerprints), stronger models, and a metric that follows the competition's weighted MAE.

## Repository Structure

```text
GROUP67_CENG313/
├── README.md
├── assignment1_eda_baseline.ipynb
├── .gitignore
└── src/
    ├── data.py        # loading and preprocessing
    ├── models.py      # baseline models
    └── utils.py       # plots and helper functions
```

`assignment2_solution.ipynb` will be added for Assignment 2. Reusable code lives in `src/` and is imported by the notebooks.

## How to Run

1. Open `assignment1_eda_baseline.ipynb` in Google Colab.
2. **Kaggle API access:** save your Kaggle API token in Colab's *Secrets* tab (key icon in the left panel) under the name `KAGGLE_API_TOKEN` and enable notebook access. The notebook reads it with `userdata.get()`. Do not upload or commit `kaggle.json`.
3. Run all cells from top to bottom. The notebook will:
   - clone this repository so that the code in `src/` is used,
   - download the competition data into `data/`,
   - run the EDA and train and evaluate the baseline models.

Requirements: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn` (all preinstalled on Colab).

## Progress Log

| Date | Work done |
| :--- | :--- |
| TODO | Repository created, competition selected |10/11/2026
| TODO | Data loading (`data.py`) and EDA functions (`utils.py`) |11/11/2026
| TODO | First baseline model (`models.py`) |12/11/2026
| 12 /11 / 2026 | Fixed the target imputation data leakage; implemented Dummy, Linear and Random Forest baselines for all five targets |
| 12 /11 /  2026 | Replaced manual `kaggle.json` upload with Colab Secrets |
| 12 /11 / 2026 | Updated README; repository prepared for transfer to `ceng313-2026` and tag `assignment1` |

## Kaggle Submission History

| Date | Submission | Notebook / model | Score |
| :--- | :--- | :--- | :--- |
| – | – | – | – |

No Kaggle submissions were made for Assignment 1. The competition is closed, so models are evaluated with the held-out split described above.

## Notes

- All code in this repository was written by the group member. No Kaggle notebooks or cells were copied.
- Data files and credentials are excluded through `.gitignore`.

