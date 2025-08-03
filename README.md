# Brent Oil Price Change Point Analysis

## Project Overview

This project analyzes Brent oil price changes and their correlation with major geopolitical and economic events using Bayesian Change Point detection. The analysis covers the period from May 20, 1987, to September 30, 2022, and aims to provide insights for investors, policymakers, and energy companies.

## Business Objective

The main goal is to study how important events affect Brent oil prices, focusing on:
- Political decisions and conflicts in oil-producing regions
- Global economic sanctions
- OPEC policy changes
- Natural disasters and supply disruptions

## Project Structure

```
tenx-brent-change-analysis/
├── data/
│   ├── BrentOilPrices.csv          # Historical Brent oil prices (1987-2022)
│   └── major_events.csv            # Compiled major events affecting oil markets
├── notebooks/
│   └── (Jupyter notebooks for analysis)
├── reports/
│   └── interim_report.md           # Interim report covering Task 1
├── src/
│   ├── analysis/                   # Data analysis scripts
│   ├── dashboard/
│   │   ├── backend/               # Flask API backend
│   │   └── frontend/              # React frontend
│   └── models/                    # PyMC3 change point models
└── README.md
```

## Key Features

### Analysis Components
- **Change Point Detection**: Bayesian modeling using PyMC3 to identify structural breaks
- **Event Correlation**: Association of detected changes with major geopolitical events
- **Impact Quantification**: Measurement of event effects on oil prices
- **Interactive Dashboard**: Web-based visualization tool for stakeholders

### Technical Stack
- **Python**: Primary analysis language
- **PyMC3**: Bayesian modeling and MCMC sampling
- **Flask**: Backend API for dashboard
- **React**: Frontend dashboard interface
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Seaborn**: Visualization

## Data Sources

### Brent Oil Prices
- **Source**: Historical daily prices
- **Period**: May 20, 1987 - September 30, 2022
- **Format**: CSV with Date and Price columns
- **Records**: ~9,000 daily observations

### Major Events Dataset
- **Events**: 35+ significant geopolitical and economic events
- **Categories**: Conflict, Political, Economic, OPEC, Natural Disaster
- **Impact Scores**: 1-9 scale based on historical significance
- **Regions**: Global, Middle East, North America, Europe, etc.

## Analysis Workflow

### Phase 1: Data Preparation
1. Load and clean Brent oil price data
2. Convert to time series format
3. Calculate log returns for stationarity
4. Perform exploratory data analysis

### Phase 2: Change Point Modeling
1. Implement Bayesian Change Point model using PyMC3
2. Define priors and likelihood functions
3. Run MCMC sampling for parameter estimation
4. Validate model convergence

### Phase 3: Event Association
1. Correlate detected change points with major events
2. Quantify impact magnitudes
3. Develop causal hypotheses
4. Generate insights for stakeholders

### Phase 4: Dashboard Development
1. Create Flask API for data serving
2. Build React frontend with interactive visualizations
3. Implement event highlighting and filtering
4. Deploy for stakeholder access

## Key Events Analyzed

| Event | Date | Category | Impact Score |
|-------|------|----------|--------------|
| Iraq Invasion of Kuwait | 1990-08-02 | Conflict | 9 |
| 9/11 Attacks | 2001-09-11 | Political | 8 |
| Lehman Brothers Collapse | 2008-09-15 | Economic | 9 |
| OPEC Production Cut Failure | 2020-03-06 | OPEC | 8 |
| COVID-19 Lockdowns | 2020-03-23 | Economic | 9 |
| Russia Invades Ukraine | 2022-02-24 | Conflict | 9 |

## Assumptions and Limitations

### Key Assumptions
- Market efficiency in reflecting available information
- Event impacts occur within days to weeks
- Linear relationships between events and price changes
- Independent event occurrences

### Critical Limitations
- **Correlation vs. Causation**: Statistical correlation doesn't prove causation
- **Multiple Events**: Simultaneous events may have confounding effects
- **Market Sentiment**: Expectations and sentiment play significant roles
- **Model Constraints**: Discrete regime changes may miss gradual transitions

## Getting Started

### Prerequisites
```bash
# Python 3.8+
pip install pymc3 pandas numpy matplotlib seaborn
pip install flask flask-cors
npm install -g create-react-app
```

### Installation
```bash
git clone <repository-url>
cd tenx-brent-change-analysis
pip install -r requirements.txt
```

### Running Analysis
```bash
# Data preprocessing
python src/analysis/preprocess_data.py

# Change point modeling
python src/models/change_point_analysis.py

# Dashboard backend
cd src/dashboard/backend
python app.py

# Dashboard frontend
cd src/dashboard/frontend
npm start
```

## Deliverables

### Interim Submission (July 30, 2025)
- ✅ Interim report covering Task 1
- ✅ Major events dataset compilation
- ✅ Project structure and workflow definition

### Final Submission (August 5, 2025)
- Complete change point analysis with PyMC3
- Interactive dashboard with React/Flask
- Technical report and executive summary
- GitHub repository with all code and documentation

## Team

**Birhan Energies Data Science Team**
- **Tutors**: Mahlet, Rediet, Kerod, Rehmet
- **Focus**: Energy sector data-driven insights
- **Mission**: Navigate global energy market complexities

## Contact

For questions or collaboration, please use the #all-week10 channel or contact the data science team at Birhan Energies.

---

**Last Updated**: July 30, 2025  
**Next Review**: August 1, 2025