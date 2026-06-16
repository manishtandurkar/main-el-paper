import json
import matplotlib.pyplot as plt
import numpy as np

# Load data
with open('a:/vegshift-final/data/output/ablation_results.json', 'r') as f:
    ablation = json.load(f)

with open('a:/vegshift-final/data/output/uncertainty_metrics.json', 'r') as f:
    uncertainty = json.load(f)

# Set global styles
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['grid.color'] = '#e5e5e5'

# ------------------------------------------------------------------
# Figure 1: Ablation Results Grouped Bar Chart
# ------------------------------------------------------------------
groups = ['climate', 'phenology', 'hydrology', 'static_context', 'all']
group_labels = ['Climate', 'Phenology', 'Hydrology', 'Static Context', 'All Features']
models = ['random_forest', 'xgboost', 'lstm']
model_labels = ['Random Forest', 'XGBoost', 'LSTM']
colors = ['#2b5c8f', '#e68a00', '#2d8a4e'] # Slate Blue, Amber, Forest Green

x = np.arange(len(groups))
width = 0.25

fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

for i, (model, label, color) in enumerate(zip(models, model_labels, colors)):
    vals = [ablation[g][model] for g in groups]
    rects = ax.bar(x + (i - 1) * width, vals, width, label=label, color=color, edgecolor='black', linewidth=0.5, alpha=0.9)
    # Add values on top of bars
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.5, fontweight='bold')

ax.set_ylabel('Test AUC-ROC', fontsize=11, fontweight='bold')
ax.set_title('Feature Group Ablation Study Comparison (AUC-ROC)', fontsize=12, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(group_labels, fontsize=10)
ax.set_ylim(0, 1.1)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.legend(loc='lower left', frameon=True, edgecolor='#cccccc')

plt.tight_layout()
plt.savefig('ablation_results.png', dpi=300)
plt.close()
print("Saved ablation_results.png")

# ------------------------------------------------------------------
# Figure 2: Uncertainty Quantification Metrics
# ------------------------------------------------------------------
uc_models = ['random_forest', 'lstm', 'tcn', 'transformer', 'tft']
uc_model_labels = ['Random Forest\n(Tree Var)', 'LSTM\n(MC-Drop)', 'TCN\n(MC-Drop)', 'Transformer\n(MC-Drop)', 'TFT\n(Quantile)']
metrics = ['ece', 'brier']
metric_labels = ['Expected Calibration Error (ECE)', 'Brier Score']
uc_colors = ['#8856a7', '#1c9099'] # Purple, Teal-blue

x_uc = np.arange(len(uc_models))
width_uc = 0.35

fig2, ax2 = plt.subplots(figsize=(8.5, 4.8), dpi=300)

for i, (metric, label, color) in enumerate(zip(metrics, metric_labels, uc_colors)):
    vals_uc = [uncertainty[m][metric] for m in uc_models]
    rects_uc = ax2.bar(x_uc + (i - 0.5) * width_uc, vals_uc, width_uc, label=label, color=color, edgecolor='black', linewidth=0.5, alpha=0.9)
    
    # Add values on top of bars
    for rect in rects_uc:
        h = rect.get_height()
        ax2.annotate(f'{h:.4f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

ax2.set_ylabel('Metric Value', fontsize=11, fontweight='bold')
ax2.set_title('Uncertainty Quantification: Expected Calibration Error vs Brier Score', fontsize=12, fontweight='bold', pad=15)
ax2.set_xticks(x_uc)
ax2.set_xticklabels(uc_model_labels, fontsize=9.5)
ax2.set_ylim(0, 0.12)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
ax2.legend(loc='upper right', frameon=True, edgecolor='#cccccc')

plt.tight_layout()
plt.savefig('uncertainty_comparison.png', dpi=300)
plt.close()
print("Saved uncertainty_comparison.png")
