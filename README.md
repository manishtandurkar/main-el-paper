# VegShift — IEEE Access Paper

**VegShift: Detecting Crop Viability Loss Events After Climate Zone Transitions in Indian Cities Using Multi-Source Geospatial and Temporal Deep Learning**

---

## Work Split (5 Members)

Sections are divided by logical grouping with roughly equal writing load (~5–6 items each).

---

### Manish T — Introduction & Related Work

| # | Section | Content |
|---|---------|---------|
| 1 | Abstract | ~200-word summary of CVLE framework, 3-source data, 8-model study, key results |
| 2 | Introduction | Climate-driven agricultural risk in India; gap in formal event timestamping; 3 paper contributions |
| 3 | II-A Related Work: Köppen-Geiger in Agriculture | Prior use of Köppen zones for agroclimatic zoning; limitations under non-stationary climate |
| 4 | II-B Related Work: Crop Failure Prediction | ML survey of crop failure methods; dominance of single-variable thresholds in literature |
| 5 | II-C Related Work: Groundwater & Agriculture | CGWB-documented depletion trends; irrigation dependency and crop failure links in India |
| 6 | II-D Related Work: Temporal Deep Learning | TFT, LSTM, TCN, Transformer applied to climate time-series; gaps in binary event detection |

---

### Manish H — Study Area & Data

| # | Section | Content |
|---|---------|---------|
| 7 | III-A Study Cities & Crop Assignments | 10 cities, coordinates, assigned crops, at-risk vs. control grouping table |
| 8 | III-B Dataset 1: Daily Atmospheric Climate | Open-Meteo / Kaggle dataset; 91k rows; humidity derivation via Steadman inversion; preprocessing |
| 9 | III-C Dataset 2: CGWB Groundwater | 2,759 wells; seasonal readings; 50 km radius aggregation; Jaipur proxy; imputation strategy |
| 10 | III-D Dataset 3: FAO GAEZ v4 | GeoTIFF rasters; suitability scale (1–7); crop-city table with ECOCROP thresholds |
| 11 | IV-A Köppen Classification & Transition Detection | Rule-based classification per Peel et al. (2007); 3-year persistence filter |

---

### Nikhil — Core Methodology

| # | Section | Content |
|---|---------|---------|
| 12 | IV-B Annual Feature Engineering | Derivation of all 17 time-varying + 5 static features; GDD, monsoon onset, dual-deficit |
| 13 | IV-C CVLE Definition | Dual-deficit formulation; Algorithm box (pseudocode); threshold constants; label construction |
| 14 | IV-D Model Architectures | All 8 models: TFT, RF, LR, XGB, LGB, LSTM, TCN, Transformer — hyperparameter tables |
| 15 | IV-E Train / Validation / Test Split | Temporal split (2000–2018 / 2000–2021 / 2022–2024); class imbalance handling; no shuffling |
| 16 | IV-F Evaluation Metrics & Threshold Optimisation | AUC-ROC, macro-F1, Brier, accuracy; F1-macro grid search for optimal threshold |

---

### Vinay — Evaluation Setup & Results (Part 1)

| # | Section | Content |
|---|---------|---------|
| 17 | IV-G Uncertainty Quantification | MC dropout (50 passes) for LSTM/TCN/Transformer; tree variance for RF; ECE (10-bin) |
| 18 | IV-H Feature Group Ablation | 5 groups (Climate, Phenology, Hydrology, Static Context, All); RF / XGB / LSTM |
| 19 | V-A Unified Test-Set Performance | 8-model × 5-metric results table; interpretation |
| 20 | V-B Pairwise Statistical Significance | Wilcoxon signed-rank on Brier loss; 28 pairs; significance at p < 0.05 |
| 21 | V-C Feature Group Ablation Results | Static context AUC >= 0.98; hydrology dominates recurrent models |

---

### Aditya — Results (Part 2), Discussion & Conclusion

| # | Section | Content |
|---|---------|---------|
| 22 | V-D Uncertainty Quantification Results | RF ECE = 0.045 best; interval widths; MC-dropout comparison |
| 23 | V-E SHAP Feature Importance | Global mean SHAP rankings; per-city breakdown; confirms static context dominance |
| 24 | V-F CVLE Event Timeline Per City | Dated events per at-risk city; control city near-zero rate validates dual-deficit |
| 25 | VI Discussion | Why simple models win; TFT failure analysis; static vs. dynamic features; groundwater signal; limitations |
| 26 | VII Conclusion | CVLE novelty; RF recommendation; future directions |

---

## Key Files

| File | Purpose |
|------|---------|
| `access.tex` | Main LaTeX source |
| `AGENT_PAPER.md` | Full technical spec — datasets, models, results, constants |
| `access.pdf` | Compiled output |

## Build

```bash
pdflatex -interaction=nonstopmode access.tex
pdflatex -interaction=nonstopmode access.tex
```

Two passes required for cross-references. Add `bibtex access` between passes once references are populated.
