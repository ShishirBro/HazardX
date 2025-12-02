# Florida Tropical Cyclone Risk Analysis (CLIMADA)

This project performs a comprehensive climate risk analysis for Florida, USA, focusing on Tropical Cyclone (TC) wind hazards. It uses the **CLIMADA** (CLIMate ADAptation) Python library to model hazards, exposures, vulnerabilities, and cost-benefit analysis of adaptation measures.

## Project Overview

The analysis covers the following key steps:
1.  **Hazard Modeling**: Generates historical wind footprints (1980-2020) from IBTrACS data.
2.  **Exposure Modeling**: Creates a high-resolution economic exposure model for Florida using **NASA Black Marble Nightlight** data (bypassing population data dependencies).
3.  **Vulnerability**: Applies the **Emanuel (2011)** impact function to estimate wind damage.
4.  **Adaptation**: Evaluates two adaptation measures:
    *   **Mangroves** (Ecosystem-based): modeled as a 20% reduction in damage.
    *   **Building Codes** (Grey infrastructure): modeled as a 50% reduction in damage.
5.  **Risk Assessment**: Calculates Average Annual Impact (AAI) and Exceedance Probability (EP) curves.
6.  **Cost-Benefit Analysis**: Computes Net Present Value (NPV) and Benefit-Cost Ratios for the adaptation measures over a future horizon (to 2040).

## Key Features & Workarounds

*   **Custom Exposure Loader**: Due to issues with the standard `LitPop` population download, a custom `exposure_loader.py` was built to generate economic exposure solely from nightlight satellite data, scaled to Florida's approximate asset value (~$3.5 Trillion).
*   **Statistical Extrapolation (Log-Pearson III)**:
    *   Since synthetic track generation (`calc_perturbed_trajectories`) can be unstable with limited local data, we implemented a rigorous statistical approach to estimate 100-year events.
    *   **Hazard**: Used **Log-Pearson Type III (LP3)** distribution to extrapolate extreme wind speeds for specific locations (e.g., Miami), plotting historical events using **Weibull plotting positions**.
    *   **Impact**: Used Extreme Value Theory (EVT) to extrapolate financial losses for 50-year and 100-year return periods.
*   **Detailed Visualizations**: Includes plots for storm tracks, hazard intensity footprints, exposure hexbins, impact function curves, cost-benefit waterfall charts, and EVT hazard curves.

## Project Structure

```
florida_risk_project/
├── src/
│   ├── hazard_loader.py    # Loads IBTrACS data and computes wind fields
│   ├── exposure_loader.py  # GENERATES exposure from NASA Nightlights (Custom)
│   ├── impact_calc.py      # Helper for basic impact calculation
│   ├── measures.py         # Defines Mangrove and Building Code measures
│   └── cost_benefit.py     # Orchestrates the Cost-Benefit Analysis
├── data/                   # Cache folder for downloaded HDF5/NetCDF files
├── florida_overview.ipynb  # MAIN NOTEBOOK: Runs the full end-to-end analysis
├── main_analysis.ipynb     # Scratchpad notebook
└── requirements.txt        # Python dependencies
```

## How to Run

1.  **Environment Setup**:
    Ensure you have the `climada_env` activated (conda environment with CLIMADA installed).
    ```bash
    conda activate climada_env
    ```

2.  **Dependencies**:
    Install any missing standard libraries (CLIMADA should handle most):
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execution**:
    Open and run the **`florida_overview.ipynb`** notebook. It is self-contained and will:
    *   Download necessary track and nightlight data automatically (cached in `data/`).
    *   Generate all plots inline, including the Log-Pearson III hazard curves.
    *   Print financial metrics (AAI, NPV, etc.).

## Results Summary

*   **Historical Hazard**: 40 years of data (1980-2020) provides a robust baseline for frequent events.
*   **100-Year Event**: Estimated via **Log-Pearson Type III** extrapolation, providing a scientifically defensible estimate of extreme wind speeds and losses despite the limited historical record.
*   **Adaptation**: The analysis compares the cost-effectiveness of "Green" (Mangroves) vs. "Grey" (Retrofitting) solutions, providing decision-support metrics for coastal resilience.


