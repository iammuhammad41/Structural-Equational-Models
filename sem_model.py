"""
Structural Equation Modeling (SEM) example using semopy.

This script:
 1. Simulates a simple two–latent variable model:
      • η1 → y1, y2
      • η2 → y3, y4
      • η2 ← η1
 2. Fits the SEM to the simulated data.
 3. Prints parameter estimates and fit statistics.
"""

import numpy as np
import pandas as pd
from semopy import Model, Optimizer
from semopy import calc_stats

# ─── Simulate Data ────────────────────────────────────────────────────────────
np.random.seed(42)
n_samples = 500

# Latent η1
eta1 = np.random.normal(size=n_samples)
# Indicators of η1
y1 = 0.8 * eta1 + np.random.normal(scale=0.5, size=n_samples)
y2 = 0.7 * eta1 + np.random.normal(scale=0.5, size=n_samples)

# Latent η2 driven by η1
eta2 = 0.9 * eta1 + np.random.normal(scale=0.7, size=n_samples)
# Indicators of η2
y3 = 0.9 * eta2 + np.random.normal(scale=0.5, size=n_samples)
y4 = 0.6 * eta2 + np.random.normal(scale=0.5, size=n_samples)

data = pd.DataFrame({
    'y1': y1, 'y2': y2,
    'y3': y3, 'y4': y4
})

# ─── 2. Specify SEM Model ───────────────────────────────────────────────────────
model_desc = """
# Measurement (Λ)  
eta1 =~ y1 + y2  
eta2 =~ y3 + y4  

# Structural (B)  
eta2 ~ eta1  
"""

# ── Fit Model ─────────────────────────────────────────────────────────────────
model = Model(model_desc)
opt = Optimizer(model)
opt.optimize(data)

# ─── Inspect Results ───────────────────────────────────────────────────────────
print("=== Parameter Estimates ===")
estimates = model.inspect()
print(estimates[['name', 'value']])

print("\n=== Fit Statistics ===")
stats = calc_stats(model, data)
for k, v in stats.items():
    print(f"{k}: {v:.3f}")

# ─── saving Results ───────────────────────────────────────────────────
model.save('sem_model_results.json')
data.to_csv('simulated_sem_data.csv', index=False)
