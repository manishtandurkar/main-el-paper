# AGENT_PAPER.md — VegShift: Technical Specification for IEEE Access Paper

> **Purpose:** This file is the canonical reference for any AI agent writing the IEEE Access paper on VegShift. It contains every technical detail needed: datasets, models, metrics, methodology, and results. Do not infer from partial context — use this file as ground truth.

---

## 1. PAPER METADATA

| Field | Value |
|---|---|
| **Target Journal** | IEEE Access |
| **Paper Type** | Research Article (multi-model comparative study) |
| **Working Title** | VegShift: Detecting Crop Viability Loss Events After Climate Zone Transitions in Indian Cities Using Multi-Source Geospatial and Temporal Deep Learning |
| **Domain** | Climate informatics, agricultural AI, time-series classification |
| **Geographic Scope** | 10 major Indian cities |
| **Temporal Scope** | 2000–2024 (25 years) |
| **Primary Contribution** | Novel dual-deficit crop viability loss event (CVLE) definition + 8-model comparative study with uncertainty quantification |

---

## 2. PROBLEM STATEMENT

### 2.1 Core Question
After a city's Köppen-Geiger climate zone shifts, which crops can no longer be grown there, and when exactly does that become true?

### 2.2 Key Concept: Crop Viability Loss Event (CVLE)
A formally timestamped event marking the year when a city's climate permanently crossed below a crop's minimum viability threshold due to **simultaneous** atmospheric failure and groundwater failure.

**Definition (formal):**
A CVLE occurs in year t if:
1. `dual_deficit == 1` in both year t and year t-1 (consecutive, prevents single-year anomalies)
2. At least 2 of the following 3 thresholds are breached in year t:
   - `sowing_window_miss > 0.6` (monsoon >60% late beyond optimal sow date)
   - `crop_water_deficit > 0.4` (>40% of crop water requirement unmet by rain)
   - `gdd_adequate == 0` (insufficient Growing Degree Days for crop maturation)

**Dual-deficit definition:** Occurs when BOTH:
- Atmospheric deficit: `crop_water_deficit > 0.4`
- Hydrological deficit: `recharge_efficiency < 0.30` (aquifer recharge failing)

### 2.3 Why This Matters
Existing crop failure research either uses static agroclimatic zones (ignoring trends) or single-variable thresholds (rainfall alone). VegShift is the first to combine Köppen zone transition detection with dual atmospheric+hydrological failure for formal event timestamping.

---

## 3. DATASETS

### 3.1 Dataset 1: Daily Atmospheric Climate

| Property | Value |
|---|---|
| **Source** | Open-Meteo / Kaggle Historical Weather Dataset |
| **File** | `data/raw/climate/india_2000_2024_daily_weather.csv` |
| **Size** | ~91,321 rows, ~190 MB |
| **Coverage** | 10 cities × 25 years × 365.25 days ≈ 91,000 rows |
| **Raw variables** | `temperature_2m_max`, `temperature_2m_min`, `precipitation_sum`, `wind_speed_10m_max` |
| **Processed file** | `data/processed/kaggle_climate.csv` (5.6 MB) |

**Preprocessing (pipeline/step0b_preprocess_datasets.py):**
- Rename → `temp_max`, `temp_min`, `temp_mean` (= (max+min)/2)
- `precipitation_sum` → `rainfall`
- Wind: km/h → m/s (÷3.6) → `wind_speed`
- **Humidity derivation (novel):** No raw humidity in dataset. Estimated via back-calculation from Steadman's apparent temperature inversion:
  ```
  e  = (AT_mean - T_mean + 0.70×wind_ms + 4.00) / 0.33
  es = 6.1078 × exp(17.27×T_mean / (237.3 + T_mean))
  RH = clip((e/es)×100, 5, 100)
  ```
  Validation: Mumbai ~90%, Chennai ~88%, Delhi ~74%, Jaipur ~65% — all climatologically consistent.

### 3.2 Dataset 2: Groundwater Levels (CGWB)

| Property | Value |
|---|---|
| **Source** | Central Groundwater Board (CGWB) of India |
| **Citation** | DOI: 10.6084/m9.figshare.29293877.v3; Nature Scientific Data (October 2025) |
| **File** | `data/raw/cgwb/CGWB_India_quality_controlled_GWLs_ref_sy_2000_2022.csv` |
| **Size** | 2,760 rows (2,759 wells + header) |
| **Coverage** | 2,759 observation wells across India; seasonal readings (Jan, May, Aug, Nov) 2000–2022 |
| **Unit** | Metres Below Ground Level (mbgl) — higher = deeper = worse depletion |
| **Processed file** | `data/processed/groundwater_annual.csv` (11 KB) |

**Well counts per city (50 km radius):**

| City | Wells | City | Wells |
|---|---|---|---|
| Lucknow | 18 | Hyderabad | 9 |
| Mumbai | 14 | Chennai | 5 |
| Delhi | 12 | Kolkata | 3 |
| Pune | 10 | Ahmedabad | 3 |
| Bangalore | 7 | **Jaipur** | **0 (nearest-well proxy)** |

**Data quality flags (`gw_imputed` column):**
- `0` = measured within 50 km radius
- `1` = pre-2005 backfill or 2023–2024 imputation (CGWB ends 2022; 2023–2024 filled with city-group mean)
- `2` = nearest-well proxy (Jaipur only; Rajasthan absent from CGWB entirely)

**Special cases:**
- **Jaipur:** 0 wells within 50 km; Step 3 uses 5 nearest regardless of distance, `gw_imputed=2`
- **Kolkata:** No May readings; global median imputed
- **Pre-2005:** Sparse coverage; backfilled using 2005–2007 mean depletion rate per city

### 3.3 Dataset 3: FAO GAEZ v4 Crop Suitability

| Property | Value |
|---|---|
| **Source** | FAO & IIASA Global Agro-Ecological Zones v4 |
| **Download** | FAO S3: `s3://data.gaezdev.aws.fao.org/res05/CRUTS32/Hist/8110H/` |
| **Format** | GeoTIFF rasters (9 km resolution) |
| **Coverage** | 6 crops for the 10 Indian cities; rainfed, high-input, 1981–2010 baseline |
| **Processed file** | `data/processed/gaez_baseline.csv` (406 bytes, 10 rows) |

**Suitability scale (1–7):**
| Score | Category |
|---|---|
| 1–2 | Not suitable / very marginal |
| 3 | Marginally suitable |
| 4 | Moderately suitable |
| 5–6 | Suitable / very suitable |
| 7 | Optimally suitable |

Note: Raw GeoTIFFs contain values 8–10 (irrigated potential); clipped to 7 (rainfed only).

**Crop-city assignments and ECOCROP thresholds:**

| City | Crop | GDD_min | Water_req (mm) | Sow_DOY | Max_Temp (°C) | Köppen 2000 | Group |
|---|---|---|---|---|---|---|---|
| Delhi | Wheat | 1200 | 450 | 120 | 35 | BSh | At-risk |
| Jaipur | Mustard | 800 | 300 | 120 | 35 | BWh | At-risk |
| Ahmedabad | Cotton | 1800 | 700 | 152 | 40 | BSh | At-risk |
| Lucknow | Sugarcane | 2500 | 1500 | 90 | 38 | Cwa | At-risk |
| Hyderabad | Groundnut | 1600 | 500 | 152 | 40 | BSh | At-risk |
| Chennai | Rice | 2000 | 1200 | 152 | 38 | Aw | At-risk |
| Bangalore | Ragi | 1400 | 350 | 152 | 38 | Aw | At-risk |
| Pune | Sorghum | 1400 | 400 | 152 | 40 | BSh | **Control** |
| Kolkata | Rice | 2000 | 1200 | 135 | 38 | Am | **Control** |
| Mumbai | Rice | 2000 | 1200 | 152 | 38 | Am | **Control** |

---

## 4. MASTER DATASET

**File:** `data/processed/vegshift_master.csv`  
**Dimensions:** 250 rows × 45 columns (10 cities × 25 years)  
**Target variable:** `cvle_label` (binary: 0 = no crop failure, 1 = CVLE event)  
**Positive cases:** 19 out of 250 rows (7.6% prevalence)

### 4.1 Feature Set (17 time-varying + 5 static)

**Time-Varying Features:**

| Feature | Derivation | Physical Meaning |
|---|---|---|
| `temp_mean` | Annual mean of daily temp_mean | Baseline warmth |
| `temp_max` | Annual mean of daily temp_max | Heat stress |
| `rainfall_annual` | Annual sum of daily rainfall | Total precipitation |
| `wind_speed` | Annual mean of wind_speed | Evapotranspiration proxy |
| `humidity` | Annual mean of derived RH | Air moisture |
| `n_dry_months` | Count(monthly rain < 60 mm) | Drought months |
| `monsoon_onset_doy` | Day-of-year when 5-day cumulative rain > 25 mm | Planting season start (IMD standard) |
| `sowing_window_miss` | (actual_onset - optimal_sow_doy) / 30 | Sowing delay in month units |
| `gdd_accumulation` | Σ max(T_daily_mean − T_base, 0), Apr–Sep | Heat units for crop maturation |
| `crop_water_deficit` | (water_req − rainfall_annual) / water_req | Fractional precipitation shortfall |
| `pre_monsoon_depth_mbgl` | Median of May GW readings (50 km radius) | Peak dry-season depletion |
| `depletion_rate` | Year-over-year change in Jan depth | Aquifer extraction rate |
| `recharge_efficiency` | (May_depth − Aug_depth) / rainfall_annual | Metres aquifer rises per mm rain |
| `dual_deficit` | 1 if crop_water_deficit>0.4 AND recharge_efficiency<0.30 | No usable backup water |
| `gdd_adequate` | 1 if gdd_accumulation ≥ gdd_min else 0 | Crop can complete maturation |
| `koppen_zone_enc` | Integer encoding of Köppen zone string | Climate regime identity |
| `cycle_sin_5yr` | sin(2π × year_index / 5) | 5-year cyclicity (TFT only) |
| `cycle_cos_5yr` | cos(2π × year_index / 5) | 5-year cyclicity (TFT only) |

**Static Features (per city-crop pair):**

| Feature | Source |
|---|---|
| `gaez_baseline_class` | FAO GAEZ raster pixel value at city centroid |
| `gdd_min` | ECOCROP crop parameter |
| `water_req` | ECOCROP crop parameter |
| `sow_doy` | ECOCROP crop parameter |
| `max_temp` | ECOCROP heat stress limit |

### 4.2 Train / Validation / Test Split

| Split | Years | Rows | Positives |
|---|---|---|---|
| Train | 2000–2018 | 190 | 16 |
| Validation | 2000–2021 | 220 | 19 (cumulative; used for early stopping) |
| Test | 2022–2024 | 30 | 1 |

**Note:** Temporal split used throughout — no shuffling, no leakage. Test set imbalance (1:29) is an acknowledged limitation; see Section 9.

---

## 5. MODELS

### 5.1 Temporal Fusion Transformer (TFT) — Primary Model

**Framework:** PyTorch Lightning + pytorch-forecasting

| Hyperparameter | Value |
|---|---|
| Encoder length (lookback) | 5 years |
| Prediction length | 3 years |
| Hidden size | 64 |
| Attention heads | 4 |
| Dropout | 0.1 |
| Hidden continuous size | 32 |
| Output quantiles | 7 (0.1, 0.25, 0.5, 0.75, 0.9 + 2 calibration quantiles) |
| Loss | QuantileLoss (multi-output quantile regression) |
| Optimizer | Adam |
| Learning rate | 1e-3 |
| Batch size | 16 |
| Max epochs | 50 |
| Early stopping patience | 5 (on val_loss) |
| Gradient clipping | 0.1 |
| Total parameters | ~115k |

**Architecture notes:**
- Time-varying known inputs: 17 features listed in Section 4.1
- Static categorical: `city`, `crop`
- Static real: `gaez_baseline_class`, `gdd_min`, `water_req`, `sow_doy`, `max_temp`
- Normalizer: GroupNormalizer by city with softplus transformation
- Output: 7-quantile distribution per future timestep

**Files:** `pipeline/step6_tft_train.py`, `pipeline/step7_tft_predict.py`, `pipeline/tft_shared.py`  
**Checkpoint:** `models/tft/vegshift-tft-best.ckpt`

### 5.2 Random Forest (RF)

| Hyperparameter | Value |
|---|---|
| n_estimators | 300 |
| max_depth | 6 |
| min_samples_leaf | 2 |
| class_weight | balanced |
| random_state | 42 |

**File:** `models/baselines/rf_baseline.pkl`

### 5.3 Logistic Regression (LR)

| Hyperparameter | Value |
|---|---|
| Penalty | L2 |
| max_iter | 2000 |
| class_weight | balanced |

**File:** `models/baselines/lr_baseline.pkl`

### 5.4 XGBoost (XGB)

| Hyperparameter | Value |
|---|---|
| n_estimators | 300 |
| max_depth | 6 |
| learning_rate | 0.05 |
| subsample | 0.8 |
| colsample_bytree | 0.8 |
| eval_metric | logloss |
| scale_pos_weight | neg_count / pos_count |

**File:** `models/baselines/xgb_baseline.pkl`

### 5.5 LightGBM (LGB)

| Hyperparameter | Value |
|---|---|
| n_estimators | 300 |
| max_depth | 6 |
| learning_rate | 0.05 |
| subsample | 0.8 |
| colsample_bytree | 0.8 |
| class_weight | balanced |

**File:** `models/baselines/lgb_baseline.pkl`

### 5.6 LSTM

| Hyperparameter | Value |
|---|---|
| Input features | 17 |
| Hidden size | 64 |
| Num layers | 2 |
| Dropout | 0.2 |
| Output | Dense(64→1) + Sigmoid |
| Sequence length | 5 years (rolling windows) |
| Optimizer | Adam (lr=1e-3) |
| Loss | Binary Cross-Entropy |
| Epochs | 30 |

**File:** `models/baselines/lstm_baseline.pt`

### 5.7 Temporal Convolutional Network (TCN)

| Hyperparameter | Value |
|---|---|
| Channels | 64 (all layers) |
| Num layers | 4 |
| Kernel size | 3 |
| Dilation | 2^i per layer (1, 2, 4, 8) — exponential, causal |
| Dropout | 0.2 |
| Output | Linear(64→1) + Sigmoid |
| Activation | ReLU |
| Input shape | (batch, seq_len=5, n_features=17) |
| Epochs | 20 |

**Architecture:** Causal conv1d blocks with residual connections  
**File:** `models/deep_models/tcn.pt`

### 5.8 Vanilla Transformer

| Hyperparameter | Value |
|---|---|
| d_model | 64 |
| Attention heads | 4 |
| Num encoder layers | 2 |
| Feedforward dim | 256 (d_model × 4) |
| Dropout | 0.1 |
| Positional encoding | Sinusoidal, max_len=512 |
| Input shape | (batch, seq_len=5, n_features=17) |
| Epochs | 20 |

**Architecture:** Input projection → Positional encoding → TransformerEncoder → Dense(d_model→1) → Sigmoid  
**File:** `models/deep_models/transformer.pt`

### 5.9 Common Preprocessing

**Scaler:** `StandardScaler` (sklearn) fit on training rows only, applied to val/test  
**Scaler file:** `models/baselines/scaler.pkl`  
**Sequence construction (sequential models):** Rolling 5-year windows per city  
**Script:** `pipeline/step8_baselines.py`, `pipeline/step20_deep_models.py`, `pipeline/research_shared.py`

---

## 6. EVALUATION RESULTS

### 6.1 Unified Test-Set Metrics (n=30, years 2022–2024)

All thresholds determined by F1-macro optimisation over validation set (not fixed at 0.5).

| Model | AUC-ROC | F1 (macro) | Brier Score | Accuracy | Optimal Threshold |
|---|---|---|---|---|---|
| Logistic Regression | **1.0000** | **1.0000** | **0.0216** | **1.0000** | 0.80 |
| Random Forest | 0.9655 | 0.8246 | 0.0253 | 0.9667 | 0.15 |
| Transformer | 0.9655 | 0.7321 | 0.0442 | 0.9333 | 0.50 |
| TCN | 0.9310 | 0.6296 | 0.0282 | 0.8667 | 0.10 |
| XGBoost | 0.8966 | 0.4915 | 0.0323 | 0.9667 | 0.05 |
| LightGBM | 0.8621 | 0.4915 | 0.0346 | 0.9667 | 0.25 |
| LSTM | 0.8621 | 0.5957 | 0.0485 | 0.8333 | 0.15 |
| TFT | 0.0690 | 0.4915 | 0.0334 | 0.9667 | 0.05 |

**Source file:** `data/output/comparative/metrics_table.json`

### 6.2 Uncertainty Quantification (Step 23)

| Method | Model | ECE | Brier | Mean Pred Std | 90% Interval Width |
|---|---|---|---|---|---|
| Tree Variance | Random Forest | **0.045** | 0.025 | 0.082 | 0.270 |
| MC Dropout (50 passes) | TCN | 0.051 | 0.028 | 0.098 | 0.322 |
| MC Dropout (50 passes) | Transformer | 0.062 | 0.044 | 0.116 | 0.381 |
| MC Dropout (50 passes) | LSTM | 0.068 | 0.048 | 0.125 | 0.410 |

ECE = Expected Calibration Error (10-bin histogram method)  
**Source file:** `data/output/uncertainty_metrics.json`

### 6.3 Feature Group Ablation (Step 22)

Models tested on 5 feature subsets independently:

| Feature Group | Features Included | RF AUC | XGB AUC | LSTM AUC |
|---|---|---|---|---|
| Climate | temp_mean, temp_max, rainfall_annual, wind_speed, humidity, n_dry_months | 0.8276 | 0.6552 | 0.2069 |
| Phenology | monsoon_onset_doy, sowing_window_miss, gdd_accumulation, gdd_adequate | 0.9310 | 0.7241 | 0.2414 |
| Hydrology | pre_monsoon_depth_mbgl, depletion_rate, recharge_efficiency, crop_water_deficit, dual_deficit | 0.8621 | 0.3966 | 0.8621 |
| Static Context | gaez_baseline_class, koppen_zone_enc | **0.9828** | **0.9828** | 0.9655 |
| All Features | All 17 features | 0.9655 | 0.7931 | 0.8621 |

**Key finding:** Static context alone (baseline FAO suitability + current Köppen zone) achieves 0.98+ AUC, dominating prediction.  
**Source file:** `data/output/ablation_results.json`

### 6.4 Statistical Significance Tests (Step 21)

**Method:** Pairwise Wilcoxon signed-rank test on per-sample Brier loss (n=30 pairs)  
**Comparisons:** 28 pairs (8 choose 2)  
**Threshold:** p < 0.05 for significance  
**Source file:** `data/output/comparative/stats_tests.json`

**Causal linkage test (Step 10):**  
Wilcoxon signed-rank comparing CVLE risk mean in [-3, -1] years pre-transition vs [+1, +3] years post-transition. Tests whether transition causally elevates crop failure risk.  
**Source file:** `data/output/transition_cvle_linkage.json`

---

## 7. METHODOLOGY DETAILS

### 7.1 Köppen-Geiger Classification (Step 1)

**Method:** Rule-based classification using:
- Annual temperature and precipitation from `climate_annual.csv`
- Threshold rules from Peel et al. (2007) world map
- Zones encoded as strings (e.g., `BSh`, `BWh`, `Aw`, `Am`, `Cwa`)

**Output:** `data/processed/koppen_annual.csv` (250 rows: city × year → zone)

### 7.2 Transition Detection (Step 1b)

**Persistence filter:** A transition is recorded only if the new zone persists for **3+ consecutive years** (prevents noise from single anomalous years).

**Output:** `data/output/transition_report.json`

### 7.3 Annual Feature Aggregation (Steps 2–3)

**Climate aggregation (Step 2):**
- Monthly grouping of daily data → annual features
- Growing season: April–September (months 4–9)
- GDD base temperature = crop-specific `gdd_base` from ECOCROP
- Monsoon onset: first day-of-year where 5-consecutive-day rain sum > 25 mm and ≥ 3 rainy days (IMD standard, starting from DOY 121)

**Groundwater aggregation (Step 3):**
- Spatial join: all wells within 50 km radius of city centroid
- Seasonal aggregation: median across wells per season (Jan, May, Aug, Nov)
- Annual features: pre-monsoon depth (May), post-monsoon depth (Aug), depletion rate (ΔJan year-on-year), recharge efficiency (depth rise / rainfall)

### 7.4 CVLE Label Construction (Step 5)

```python
# Pseudocode — see pipeline/step5_join_and_features.py
for city in cities:
    for year_i in range(1, len(city_data)):
        consecutive_dual = (
            city_data[year_i]['dual_deficit'] == 1 and
            city_data[year_i-1]['dual_deficit'] == 1
        )
        t1 = int(city_data[year_i]['sowing_window_miss'] > 0.6)
        t2 = int(city_data[year_i]['crop_water_deficit'] > 0.4)
        t3 = int(city_data[year_i]['gdd_adequate'] == 0)
        cvle[year_i] = 1 if (consecutive_dual and (t1 + t2 + t3) >= 2) else 0
```

**Thresholds:**
- `CROP_WATER_DEFICIT_THRESHOLD` = 0.4
- `RECHARGE_EFFICIENCY_THRESHOLD` = 0.30
- `SOWING_WINDOW_MISS_THRESHOLD` = 0.6

### 7.5 Class Imbalance Handling

1. `class_weight='balanced'` for RF, LR, LGB
2. `scale_pos_weight = neg_count / pos_count` for XGBoost
3. F1-macro optimal threshold search (not fixed 0.5) for all models in Step 21
4. Brier score and ECE used as calibration metrics alongside AUC

### 7.6 SHAP Explainability (Step 9)

**Method:** SHAP TreeExplainer on RF, XGBoost, LightGBM  
**Outputs:** Global feature importance (mean |SHAP|) + per-city breakdown  
**File:** `data/output/shap_explanation.json`

### 7.7 Control City Validation (Step 12)

Pune, Kolkata, Mumbai used as control cities (expected to remain climatically stable 2000–2024). CVLE labels should remain 0 for controls; any positives = false detection rate.

---

## 8. FILE STRUCTURE (KEY FILES FOR PAPER)

```
pipeline/
  step0_master_index.py          # 250-row skeleton (10 cities × 25 years)
  step0b_preprocess_datasets.py  # Humidity derivation, column standardisation
  step1_koppen_classification.py # Köppen zone assignment per city-year
  step1b_transition_detection.py # Persistent (3+ yr) zone transition detection
  step2_climate_aggregate.py     # Annual GDD, monsoon onset, water deficit
  step3_groundwater_aggregate.py # City-level GW: depletion, recharge efficiency
  step4_gaez_extract.py          # Crop suitability raster extraction
  step5_join_and_features.py     # 3-source join → vegshift_master.csv + CVLE labels
  step6_tft_train.py             # TFT training (5-yr lookback, 7 quantiles)
  step7_tft_predict.py           # TFT predictions + attention extraction
  step8_baselines.py             # RF, LR, XGBoost, LightGBM, LSTM training
  step9_shap_explainability.py   # SHAP analysis
  step10_causal_linkage.py       # Wilcoxon: pre vs post transition risk
  step20_deep_models.py          # TCN + Vanilla Transformer training
  step21_unified_eval.py         # Unified metrics table + pairwise Wilcoxon
  step22_ablation.py             # Feature group ablation (5 groups × 3 models)
  step23_uncertainty.py          # MC dropout (50 passes) + tree variance + ECE
  tft_shared.py                  # TimeSeriesDataSet builder, feature constants
  research_shared.py             # FEATURES list, FEATURE_GROUPS, model class definitions

data/processed/vegshift_master.csv  # 250 rows × 45 cols — main training file
data/output/comparative/metrics_table.json   # All 8 models unified metrics
data/output/ablation_results.json            # Feature group ablation
data/output/uncertainty_metrics.json         # ECE, Brier, MC std
data/output/transition_cvle_linkage.json     # Causal linkage stats
data/output/shap_explanation.json            # Feature importance
data/output/crop_viability_events.json       # All dated CVLE events
data/output/transition_report.json           # Detected Koppen transitions
```

---

## 9. LIMITATIONS (DISCLOSE IN PAPER)

| Limitation | Detail |
|---|---|
| Test set size | n=30 total, 1 positive case; AUC and precision metrics statistically unstable |
| Class imbalance | 1:29 in test set; all-negative trivially achieves 96.7% accuracy |
| CGWB data gap | Ends 2022; 2023–2024 groundwater imputed from city-group mean |
| Jaipur groundwater | Zero wells within 50 km; nearest-well proxy used (`gw_imputed=2`) |
| TFT failure | AUC=0.069; pytorch-forecasting's QuantileLoss not suited for binary CVLE detection on this dataset size |
| Humidity derivation | Estimated from temperature inversion, not directly measured |
| GAEZ static baseline | 1981–2010 baseline; does not capture post-2010 suitability shifts |
| CVLE subjectivity | Thresholds (0.4, 0.30, 0.6) are domain-informed but not empirically derived from yield loss data |

---

## 10. KEY FINDINGS (FOR ABSTRACT / CONCLUSION)

1. **Simple models outperform deep models:** LR (AUC=1.0) and RF (AUC=0.9655) outperform TFT (AUC=0.069), suggesting the CVLE classification problem is largely linearly separable in feature space for this dataset.

2. **Static context dominates:** Ablation shows `gaez_baseline_class + koppen_zone_enc` alone achieves AUC=0.98 (RF, XGB), meaning the baseline FAO suitability + current climate regime nearly fully determines viability loss risk.

3. **Hydrology critical for recurrent models:** Hydrological features achieve AUC=0.8621 for LSTM (highest group), indicating temporal models specifically exploit groundwater depletion signals.

4. **Deep sequential models effective:** TCN (0.9310) and Transformer (0.9655) both outperform LSTM (0.8621), suggesting convolution/attention better exploit 5-year crop cycle structure than recurrence.

5. **Tree variance best-calibrated:** RF ECE=0.045 outperforms all neural MC-dropout methods (ECE 0.051–0.068), making it the most reliable for probability estimates.

6. **Dual-deficit definition validated:** Control cities (Pune, Kolkata, Mumbai) produce near-zero CVLE rates, validating the dual-threshold formulation.

---

## 11. SUGGESTED IEEE ACCESS SECTIONS

```
I.   Introduction
     - Climate-driven agricultural risk in India
     - Gap: lack of formal event timestamping tied to climate zone transitions
     - Contributions: CVLE definition, 3-source dataset fusion, 8-model comparative study

II.  Related Work
     - Köppen climate classification in agriculture
     - Crop failure prediction (ML survey)
     - Groundwater depletion + agriculture interaction
     - TFT and temporal deep learning for climate

III. Study Area and Data
     - 10 Indian cities (Table: coordinates, crops, control/at-risk)
     - Dataset 1: Open-Meteo daily climate (Table: variables, size)
     - Dataset 2: CGWB groundwater (Table: wells per city, imputation)
     - Dataset 3: FAO GAEZ v4 crop suitability (Table: crop-city pairs, thresholds)

IV.  Methodology
     A. Köppen-Geiger classification and transition detection
     B. Feature engineering (GDD, monsoon onset, dual-deficit)
     C. CVLE label definition (Algorithm box: pseudocode)
     D. Model architectures (TFT, RF, LR, XGB, LGB, LSTM, TCN, Transformer)
     E. Evaluation metrics and threshold optimisation
     F. Uncertainty quantification (MC dropout, tree variance, ECE)
     G. Feature group ablation
     H. Causal linkage analysis (Wilcoxon)

V.   Experiments and Results
     A. Unified test-set performance (Table: 8 models × 5 metrics)
     B. Pairwise statistical significance
     C. Feature group ablation results (Table: 5 groups × 3 models)
     D. Uncertainty quantification (Table: ECE, Brier, interval widths)
     E. SHAP feature importance
     F. CVLE events timeline per city

VI.  Discussion
     - Why simple models win (feature space separability, dataset size)
     - Why TFT fails (quantile loss + binary target + n=250)
     - Role of static vs dynamic features
     - Groundwater as the differentiating signal for recurrent models
     - Limitations and validity threats

VII. Conclusion
     - CVLE framework novelty
     - RF as recommended model for deployment
     - Future: larger geographic scope, crop yield ground truth validation
```

---

## 12. CONSTANTS REFERENCE

```python
# Spatial
RADIUS_KM = 50                          # Well aggregation radius
CITY_COORDS = {                         # (lat, lon)
    'Delhi':     (28.6139, 77.2090),
    'Mumbai':    (19.0760, 72.8777),
    'Kolkata':   (22.5726, 88.3639),
    'Chennai':   (13.0827, 80.2707),
    'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Ahmedabad': (23.0225, 72.5714),
    'Jaipur':    (26.9124, 75.7873),
    'Lucknow':   (26.8467, 80.9462),
    'Pune':      (18.5204, 73.8567),
}

# Temporal
PERSISTENCE = 3                         # Koppen transition persistence (years)
GROWING_SEASON_MONTHS = range(4, 10)    # April–September

# CVLE thresholds
CROP_WATER_DEFICIT_THRESHOLD = 0.4
RECHARGE_EFFICIENCY_THRESHOLD = 0.30
SOWING_WINDOW_MISS_THRESHOLD = 0.6

# Monsoon detection (IMD standard)
MONSOON_START_DOY = 121
MONSOON_RAIN_THRESHOLD = 2.5            # mm/day
MONSOON_WINDOW_DAYS = 5
MONSOON_RAIN_DAYS_REQUIRED = 3
```

---

## 13. TECH STACK

| Category | Library | Version |
|---|---|---|
| Data | pandas | ≥2.0 |
| Data | numpy | ≥1.24 |
| Statistics | scipy | ≥1.10 |
| ML — tree/linear | scikit-learn | ≥1.3 |
| ML — boosting | xgboost | ≥2.0 |
| ML — boosting | lightgbm | ≥4.0 |
| ML — deep | torch (PyTorch) | ≥2.0 |
| ML — deep | pytorch-lightning | ≥2.0 |
| ML — TFT | pytorch-forecasting | ≥1.0 |
| Geospatial | rasterio | ≥1.3 |
| Explainability | shap | ≥0.44 |
| Visualisation | plotly | ≥5.18 |
| Dashboard | dash | ≥2.14 |
| API | fastapi | ≥0.110 |
| Testing | pytest | ≥7.0 |

---

*Last updated by AGENT_PAPER.md generator on 2026-06-16. All numbers sourced from pipeline output files in `data/output/`. For any number not in this file, check the corresponding JSON in `data/output/`.*
