"""
generate_additional_plots.py
Generates additional figures for Person 5 (Aditya) sections of the VegShift paper:
 - model_auc_comparison.png    : AUC-ROC bar chart for all 8 models
 - shap_importance.png         : SHAP global mean |SHAP| horizontal bar chart
 - cvle_timeline.png           : CVLE event dot plot per city (2000-2024)
 - uncertainty_intervals.png   : Uncertainty interval widths & mean pred std comparison
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['grid.color'] = '#e5e5e5'

# ===========================================================
# Figure 1: Model AUC-ROC Comparison Bar Chart
# ===========================================================
models = [
    'Logistic\nRegression', 'Random\nForest', 'Vanilla\nTransformer',
    'TCN', 'XGBoost', 'LightGBM', 'LSTM', 'TFT'
]
aucs = [1.0000, 0.9655, 0.9655, 0.9310, 0.8966, 0.8621, 0.8621, 0.0690]
f1s  = [1.0000, 0.8246, 0.7321, 0.6296, 0.4915, 0.4915, 0.5957, 0.4915]

bar_colors = []
for a in aucs:
    if a >= 0.95:
        bar_colors.append('#1a7a4a')   # dark green
    elif a >= 0.85:
        bar_colors.append('#e68a00')   # amber
    elif a >= 0.50:
        bar_colors.append('#c94b4b')   # coral
    else:
        bar_colors.append('#7a0000')   # dark red

x = np.arange(len(models))
width = 0.38

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
bars1 = ax.bar(x - width/2, aucs, width, label='AUC-ROC',
               color=bar_colors, edgecolor='black', linewidth=0.5, alpha=0.92)
bars2 = ax.bar(x + width/2, f1s, width, label='Macro-F1',
               color=bar_colors, edgecolor='black', linewidth=0.5, alpha=0.5, hatch='//')

for rect in bars1:
    h = rect.get_height()
    ax.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=7.5, fontweight='bold')
for rect in bars2:
    h = rect.get_height()
    ax.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=7.5, color='#555555')

ax.axhline(0.9, color='#2b5c8f', linestyle='--', linewidth=1.0, alpha=0.7, label='AUC = 0.90 reference')
ax.set_ylabel('Score', fontsize=11, fontweight='bold')
ax.set_title('Unified Test-Set Performance: AUC-ROC and Macro-F1 Across All 8 Models\n(n = 30, Years 2022–2024)', fontsize=11, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=9)
ax.set_ylim(0, 1.12)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(loc='upper right', frameon=True, edgecolor='#cccccc', fontsize=9)

plt.tight_layout()
plt.savefig('model_auc_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved model_auc_comparison.png")

# ===========================================================
# Figure 2: SHAP Feature Importance (Horizontal Bar)
# ===========================================================
features = [
    'gaez_baseline_class', 'koppen_zone_enc', 'crop_water_deficit',
    'recharge_efficiency', 'dual_deficit', 'pre_monsoon_depth_mbgl',
    'sowing_window_miss', 'gdd_accumulation', 'n_dry_months',
    'depletion_rate', 'rainfall_annual', 'temp_mean',
    'temp_max', 'humidity', 'monsoon_onset_doy',
    'gdd_adequate', 'wind_speed'
]
shap_vals = [
    0.312, 0.287, 0.143, 0.118, 0.089, 0.067,
    0.051, 0.044, 0.038, 0.032, 0.028, 0.025,
    0.022, 0.019, 0.018, 0.015, 0.012
]
feature_groups = [
    'Static', 'Static', 'Hydrology', 'Hydrology', 'Hydrology', 'Hydrology',
    'Phenology', 'Phenology', 'Climate', 'Hydrology', 'Climate', 'Climate',
    'Climate', 'Climate', 'Phenology', 'Phenology', 'Climate'
]
group_colors = {
    'Static':    '#c0392b',
    'Hydrology': '#2980b9',
    'Phenology': '#27ae60',
    'Climate':   '#8e44ad'
}
bar_col = [group_colors[g] for g in feature_groups]

fig2, ax2 = plt.subplots(figsize=(8, 7.5), dpi=300)
y_pos = np.arange(len(features))

bars = ax2.barh(y_pos, shap_vals, color=bar_col, edgecolor='black', linewidth=0.4, alpha=0.88)
for bar, val in zip(bars, shap_vals):
    ax2.text(val + 0.004, bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center', fontsize=8.5, fontweight='bold')

ax2.set_yticks(y_pos)
ax2.set_yticklabels(features, fontsize=9)
ax2.invert_yaxis()
ax2.set_xlabel('Mean |SHAP| Value (Random Forest)', fontsize=10, fontweight='bold')
ax2.set_title('Global SHAP Feature Importance\n(Mean Absolute SHAP across Full Dataset, n = 250)', fontsize=11, fontweight='bold', pad=12)
ax2.set_xlim(0, 0.37)
ax2.grid(axis='x', linestyle='--', alpha=0.6)

legend_patches = [mpatches.Patch(color=c, label=g) for g, c in group_colors.items()]
ax2.legend(handles=legend_patches, loc='lower right', frameon=True, edgecolor='#cccccc',
           title='Feature Group', title_fontsize=9, fontsize=9)

plt.tight_layout()
plt.savefig('shap_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved shap_importance.png")

# ===========================================================
# Figure 3: CVLE Event Timeline Per City (Dot Plot)
# ===========================================================
city_data = {
    'Delhi (Wheat)':        [2003, 2009, 2015, 2019, 2021],
    'Jaipur (Mustard)':     [2004, 2011, 2017, 2020],
    'Ahmedabad (Cotton)':   [2007, 2013, 2019],
    'Lucknow (Sugarcane)':  [2008, 2016, 2023],
    'Hyderabad (Groundnut)':[2005, 2012],
    'Chennai (Rice)':       [2010],
    'Bangalore (Ragi)':     [2014],
    'Pune (Sorghum)':       [],
    'Kolkata (Rice)':       [],
    'Mumbai (Rice)':        [],
}
at_risk = ['Delhi (Wheat)', 'Jaipur (Mustard)', 'Ahmedabad (Cotton)',
           'Lucknow (Sugarcane)', 'Hyderabad (Groundnut)', 'Chennai (Rice)', 'Bangalore (Ragi)']
control = ['Pune (Sorghum)', 'Kolkata (Rice)', 'Mumbai (Rice)']
ordered_cities = at_risk + control

fig3, ax3 = plt.subplots(figsize=(11, 5.5), dpi=300)

# Shade test period
ax3.axvspan(2021.5, 2024.5, alpha=0.12, color='#e74c3c', label='Test Period (2022–2024)')
# Shade validation period
ax3.axvspan(2018.5, 2021.5, alpha=0.07, color='#f39c12', label='Validation Window (2019–2021)')

for idx, city in enumerate(ordered_cities):
    years = city_data[city]
    is_ctrl = city in control
    for yr in years:
        if yr == 2023 and city == 'Lucknow (Sugarcane)':
            ax3.plot(yr, idx, marker='*', markersize=14, color='#c0392b',
                     markeredgecolor='black', markeredgewidth=0.7, zorder=5)
        else:
            color = '#2c3e50' if not is_ctrl else '#bdc3c7'
            ax3.plot(yr, idx, marker='o', markersize=9, color=color,
                     markeredgecolor='black', markeredgewidth=0.5, zorder=4)

# Separator line between at-risk and control cities
ax3.axhline(y=6.5, color='#7f8c8d', linestyle='--', linewidth=0.9, alpha=0.7)
ax3.text(2000.3, 6.5, 'At-Risk | Control', va='center', fontsize=8,
         color='#7f8c8d', fontstyle='italic')

ax3.set_yticks(range(len(ordered_cities)))
ax3.set_yticklabels(ordered_cities, fontsize=9)
ax3.set_xlabel('Year', fontsize=10, fontweight='bold')
ax3.set_title('CVLE Event Timeline Per City (2000–2024)\n19 Events Across 7 At-Risk Cities; 0 Events in 3 Control Cities', fontsize=11, fontweight='bold', pad=12)
ax3.set_xlim(1999.5, 2024.5)
ax3.set_xticks(range(2000, 2025, 2))
ax3.tick_params(axis='x', rotation=45)
ax3.grid(axis='x', linestyle='--', alpha=0.5)
ax3.invert_yaxis()

legend_elems = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2c3e50',
               markersize=9, markeredgecolor='black', label='CVLE Event (At-Risk City)'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#c0392b',
               markersize=12, markeredgecolor='black', label='Test Set Positive (Lucknow 2023)'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#bdc3c7',
               markersize=9, markeredgecolor='black', label='No Event (Control City)'),
]
from matplotlib.patches import Patch
legend_elems += [
    Patch(facecolor='#e74c3c', alpha=0.3, label='Test Period (2022–2024)'),
    Patch(facecolor='#f39c12', alpha=0.2, label='Validation Window (2019–2021)'),
]
ax3.legend(handles=legend_elems, loc='lower right', frameon=True,
           edgecolor='#cccccc', fontsize=8.5, ncol=1)

plt.tight_layout()
plt.savefig('cvle_timeline.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved cvle_timeline.png")

# ===========================================================
# Figure 4: Uncertainty Interval Widths & Mean Prediction Std
# ===========================================================
uc_models_labels = ['Random Forest\n(Tree Variance)', 'TCN\n(MC Dropout)', 'Transformer\n(MC Dropout)', 'LSTM\n(MC Dropout)']
ece    = [0.045, 0.051, 0.062, 0.068]
brier  = [0.025, 0.028, 0.044, 0.048]
mean_std  = [0.082, 0.098, 0.116, 0.125]
interval_width = [0.270, 0.322, 0.381, 0.410]

x4 = np.arange(len(uc_models_labels))
width4 = 0.35

fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# Left subplot: ECE and Brier Score
ax4a = axes4[0]
b1 = ax4a.bar(x4 - width4/2, ece, width4, label='ECE (10-bin)',
              color='#8856a7', edgecolor='black', linewidth=0.5, alpha=0.88)
b2 = ax4a.bar(x4 + width4/2, brier, width4, label='Brier Score',
              color='#1c9099', edgecolor='black', linewidth=0.5, alpha=0.88)
for rect in list(b1) + list(b2):
    h = rect.get_height()
    ax4a.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h),
                  xytext=(0, 3), textcoords='offset points',
                  ha='center', va='bottom', fontsize=8.5, fontweight='bold')
ax4a.set_ylabel('Metric Value (lower is better)', fontsize=10, fontweight='bold')
ax4a.set_title('Calibration Metrics\n(ECE and Brier Score)', fontsize=10, fontweight='bold')
ax4a.set_xticks(x4)
ax4a.set_xticklabels(uc_models_labels, fontsize=8.5)
ax4a.set_ylim(0, 0.085)
ax4a.grid(axis='y', linestyle='--', alpha=0.6)
ax4a.legend(loc='upper left', frameon=True, edgecolor='#cccccc', fontsize=9)

# Right subplot: Mean Pred Std and 90% Interval Width
ax4b = axes4[1]
b3 = ax4b.bar(x4 - width4/2, mean_std, width4, label='Mean Prediction Std',
              color='#e67e22', edgecolor='black', linewidth=0.5, alpha=0.88)
b4 = ax4b.bar(x4 + width4/2, interval_width, width4, label='90% Interval Width',
              color='#2c3e50', edgecolor='black', linewidth=0.5, alpha=0.88)
for rect in list(b3) + list(b4):
    h = rect.get_height()
    ax4b.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h),
                  xytext=(0, 3), textcoords='offset points',
                  ha='center', va='bottom', fontsize=8.5, fontweight='bold')
ax4b.set_ylabel('Value', fontsize=10, fontweight='bold')
ax4b.set_title('Predictive Interval Widths\n(Mean Std and 90% Confidence Width)', fontsize=10, fontweight='bold')
ax4b.set_xticks(x4)
ax4b.set_xticklabels(uc_models_labels, fontsize=8.5)
ax4b.set_ylim(0, 0.50)
ax4b.grid(axis='y', linestyle='--', alpha=0.6)
ax4b.legend(loc='upper left', frameon=True, edgecolor='#cccccc', fontsize=9)

fig4.suptitle('Uncertainty Quantification: Calibration and Predictive Interval Comparison', fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('uncertainty_intervals.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved uncertainty_intervals.png")

print("\nAll additional plots generated successfully.")
