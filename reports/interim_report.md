# Interim Report: Brent Oil Price Change Point Analysis
**Birhan Energies - Data Science Team**  
**Date: July 30, 2025**

## Executive Summary

This interim report outlines the planned approach for analyzing Brent oil price changes and their correlation with major geopolitical and economic events. The analysis will employ Bayesian Change Point detection using PyMC3 to identify structural breaks in oil price behavior and associate them with significant events from 1987 to 2022.

## Task 1: Laying the Foundation for Analysis

### 1.1 Data Analysis Workflow

#### Phase 1: Data Preparation and Exploration
1. **Data Loading and Cleaning**
   - Load Brent oil price data (May 20, 1987 - September 30, 2022)
   - Convert date format and handle missing values
   - Create time series with proper datetime indexing

2. **Exploratory Data Analysis (EDA)**
   - Visualize price trends over time
   - Analyze price distribution and volatility patterns
   - Calculate and plot log returns for stationarity analysis
   - Identify periods of high volatility and potential change points

3. **Time Series Properties Analysis**
   - Test for stationarity using Augmented Dickey-Fuller test
   - Analyze autocorrelation and partial autocorrelation functions
   - Examine volatility clustering patterns

#### Phase 2: Event Research and Compilation
1. **Major Event Identification**
   - Research geopolitical events affecting oil markets
   - Compile OPEC decisions and production changes
   - Document economic sanctions and their timing
   - Identify conflicts in oil-producing regions

2. **Event Dataset Creation**
   - Create structured CSV with event dates and descriptions
   - Categorize events by type (political, economic, conflict, OPEC)
   - Assign impact scores based on historical significance

#### Phase 3: Change Point Modeling
1. **Model Development**
   - Implement Bayesian Change Point model using PyMC3
   - Define priors for change point locations and parameters
   - Configure MCMC sampling parameters

2. **Model Validation**
   - Check convergence diagnostics
   - Validate model assumptions
   - Compare with alternative approaches

#### Phase 4: Analysis and Interpretation
1. **Change Point Detection**
   - Identify statistically significant structural breaks
   - Quantify uncertainty in change point locations
   - Analyze parameter changes (mean, volatility)

2. **Event Association**
   - Correlate detected change points with researched events
   - Quantify impact magnitudes
   - Develop causal hypotheses

#### Phase 5: Dashboard Development
1. **Backend Development (Flask)**
   - Create APIs for data serving
   - Implement analysis result endpoints
   - Handle data filtering and querying

2. **Frontend Development (React)**
   - Design interactive visualizations
   - Implement event highlighting features
   - Create responsive dashboard interface

### 1.2 Research and Event Compilation

#### Key Events Identified (1987-2022)

| Date | Event | Category | Expected Impact |
|------|-------|----------|-----------------|
| 1990-08-02 | Iraq invades Kuwait | Conflict | Major price spike |
| 1991-01-17 | Gulf War begins | Conflict | Continued volatility |
| 1997-11-30 | OPEC increases production quota | OPEC | Price decline |
| 2001-09-11 | 9/11 attacks | Political | Market uncertainty |
| 2003-03-20 | Iraq War begins | Conflict | Supply disruption fears |
| 2008-09-15 | Lehman Brothers collapse | Economic | Global recession impact |
| 2011-02-15 | Arab Spring begins | Political | Middle East instability |
| 2014-06-20 | OPEC maintains production despite oversupply | OPEC | Price collapse |
| 2016-11-30 | OPEC+ production cut agreement | OPEC | Price recovery |
| 2020-03-06 | OPEC+ production cut failure | OPEC | Price war |
| 2020-03-23 | COVID-19 lockdowns begin | Economic | Demand collapse |
| 2022-02-24 | Russia invades Ukraine | Conflict | Supply disruption |

#### Event Dataset Structure
```csv
Date,Event,Category,Description,Impact_Score,Region
1990-08-02,Iraq Invasion of Kuwait,Conflict,Iraq invades Kuwait leading to Gulf War,9,Middle East
...
```

### 1.3 Assumptions and Limitations

#### Key Assumptions
1. **Market Efficiency**: Oil prices reflect all available information at the time
2. **Event Impact Timing**: Major events affect prices within days to weeks
3. **Linear Relationships**: Price changes are approximately linear with respect to event magnitude
4. **Independent Events**: Events are treated as independent occurrences

#### Critical Limitations
1. **Correlation vs. Causation**: 
   - Statistical correlation does not prove causation
   - Multiple events may occur simultaneously
   - Market reactions may be anticipatory rather than reactive
   - Confounding variables may exist

2. **Data Limitations**:
   - Daily prices may not capture intraday volatility
   - Missing data during market closures
   - Price manipulation or reporting errors

3. **Model Limitations**:
   - Change point models assume discrete regime changes
   - May miss gradual transitions
   - Limited to detecting mean/volatility changes

4. **Event Attribution**:
   - Difficult to isolate single event impacts
   - Market sentiment and expectations play significant roles
   - Global economic conditions may overshadow specific events

### 1.4 Communication Strategy

#### Primary Channels
1. **Interactive Dashboard**: React-based web application for stakeholders
2. **Technical Report**: Detailed analysis for data science teams
3. **Executive Summary**: High-level insights for decision makers

#### Key Stakeholders
- **Investors**: Risk management and investment timing
- **Policymakers**: Economic stability and energy security
- **Energy Companies**: Operational planning and cost management

## Task 1: Understanding the Model and Data

### 2.1 Time Series Properties

#### Expected Characteristics
1. **Non-stationarity**: Oil prices typically exhibit trends and structural breaks
2. **Volatility Clustering**: Periods of high volatility tend to cluster
3. **Fat Tails**: Price changes show leptokurtic distributions
4. **Mean Reversion**: Prices may revert to long-term averages

#### Modeling Implications
- **Log Returns**: Transform prices to log returns for stationarity
- **Multiple Change Points**: Expect multiple structural breaks over 35-year period
- **Volatility Modeling**: Include volatility change points in addition to mean changes

### 2.2 Change Point Model Purpose

#### What Change Point Models Do
1. **Identify Structural Breaks**: Detect when underlying data generating process changes
2. **Quantify Uncertainty**: Provide probabilistic estimates of change point locations
3. **Parameter Estimation**: Estimate new parameter values after changes
4. **Model Comparison**: Compare different change point specifications

#### Business Value
- **Risk Management**: Identify periods of increased market risk
- **Investment Timing**: Optimize entry/exit points based on regime changes
- **Policy Impact Assessment**: Measure effectiveness of policy interventions
- **Forecasting**: Improve predictions by accounting for regime changes

### 2.3 Expected Model Outputs

#### Primary Outputs
1. **Change Point Locations**: Posterior distributions of change point dates
2. **Parameter Changes**: Before/after means, volatilities, and other parameters
3. **Uncertainty Quantification**: Credible intervals for all estimates
4. **Model Diagnostics**: Convergence metrics and fit statistics

#### Limitations
1. **Discrete Changes**: Assumes abrupt rather than gradual transitions
2. **Limited Complexity**: May miss subtle or multiple simultaneous changes
3. **Prior Sensitivity**: Results may depend on prior specifications
4. **Computational Cost**: MCMC sampling can be computationally intensive

## Next Steps

### Immediate Actions (Next 48 hours)
1. Complete event dataset compilation
2. Implement initial data preprocessing pipeline
3. Begin exploratory data analysis
4. Set up development environment for PyMC3

### Week 1 Goals
1. Complete EDA and time series analysis
2. Implement basic change point model
3. Begin dashboard backend development
4. Draft initial findings report

### Success Metrics
- Identify 10-15 significant change points
- Associate 70%+ of change points with documented events
- Achieve model convergence with R-hat < 1.1
- Develop functional dashboard prototype

## Technical Stack

### Analysis
- **Python**: Primary analysis language
- **PyMC3**: Bayesian modeling and MCMC sampling
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Seaborn**: Visualization

### Dashboard
- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Charts**: Recharts or Chart.js
- **Deployment**: Docker containerization

### Version Control
- **GitHub**: Code repository and collaboration
- **Documentation**: Markdown and Jupyter notebooks

---

**Contact**: Data Science Team, Birhan Energies  
**Next Review**: August 1, 2025 