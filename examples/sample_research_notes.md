# Research Notes - AI in Climate Modeling

**Topic:** Hybrid approaches combining physical models with AI
**Papers Analyzed:** 25
**Date:** 2024-01-15

---

## Key Papers

### 1. Physics-Informed Neural Networks (PINNs)
**Raissi et al. (2019) - JCP**
- Method: Encode physics equations in NN loss function
- Application: Fluid dynamics, heat transfer
- Relevance: Shows feasibility of physics-AI hybrid
- Limitation: Not tested on climate scale

### 2. WeatherBench
**Rasp et al. (2020) - JAMES**
- Benchmark dataset for ML weather prediction
- Compares pure ML vs NWP models
- Finding: ML competitive but less interpretable
- Our use: Baseline for comparison

### 3. FourCastNet
**Pathak et al. (2022) - Nature**
- Transformer-based weather forecasting
- Achieves SOTA on medium-range prediction
- Gap: No physics integration
- Relevance: Architecture inspiration

[... 22 more papers ...]

---

## Research Gaps Identified

### Gap 1: No Large-Scale Physics-AI Hybrid
- Existing work: small scale or theoretical
- Opportunity: Demonstrate at global climate scale
- Our approach: Residual learning with physics constraints

### Gap 2: Interpretability Trade-off Unsolved
- Pure AI: accurate but opaque
- Pure physics: interpretable but slow
- Our contribution: Maintain both via attention mechanisms

### Gap 3: Limited Long-Term Validation
- Most ML models: days to weeks ahead
- Climate needs: years to decades
- Our focus: Extend to seasonal predictions

---

## Methodology Insights

**Common approaches:**
1. Pure physics (GCMs): 40% of papers
2. Pure ML: 35% of papers
3. Statistical hybrids: 20% of papers
4. Deep learning + physics: 5% (emerging)

**Our novel angle:** Residual learning where AI learns corrections to physics model

---

## Datasets Available

1. **ERA5** - 40 years, global, hourly
2. **CMIP6** - Multi-model ensemble
3. **WeatherBench** - Standard benchmark
4. **ClimateNet** - Labeled extreme events

**Our choice:** ERA5 (most comprehensive, well-validated)

---

## Open Questions

1. How to balance physics loss vs data loss?
2. Which architecture: CNN vs Transformer vs hybrid?
3. How much physics knowledge to encode?
4. Computational efficiency vs accuracy trade-off?

---

## Next Steps

1. Implement baseline physics model
2. Train pure AI model for comparison
3. Design hybrid architecture
4. Run ablation studies
5. Write paper!
