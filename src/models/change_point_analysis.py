"""
Bayesian Change Point Analysis for Brent Oil Prices using PyMC3.
Detects structural breaks in oil price behavior and quantifies uncertainty.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc3 as pm
import arviz as az
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_processed_data(file_path='../../data/processed_brent_data.csv'):
    """
    Load processed Brent oil price data.
    
    Args:
        file_path (str): Path to processed data file
        
    Returns:
        pd.DataFrame: Processed time series data
    """
    print("Loading processed data...")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"Loaded {len(df)} observations")
    return df

def simple_change_point_model(data, n_changepoints=3):
    """
    Implement a simple Bayesian change point model.
    
    Args:
        data (np.array): Time series data (log returns)
        n_changepoints (int): Number of change points to detect
        
    Returns:
        pm.Model: PyMC3 model object
    """
    print(f"Building change point model with {n_changepoints} change points...")
    
    n = len(data)
    
    with pm.Model() as model:
        # Prior for change point locations
        # Uniform prior over all possible locations
        changepoints = pm.Uniform('changepoints', 
                                 lower=0, 
                                 upper=n, 
                                 shape=n_changepoints)
        
        # Sort change points to ensure they're in chronological order
        sorted_changepoints = pm.Deterministic('sorted_changepoints', 
                                             pm.math.sort(changepoints))
        
        # Priors for means in each regime
        means = pm.Normal('means', mu=0, sd=0.1, shape=n_changepoints + 1)
        
        # Prior for standard deviation
        sigma = pm.HalfNormal('sigma', sd=0.1)
        
        # Create regime indicators
        regime = np.zeros(n, dtype=int)
        for i in range(n):
            for j, cp in enumerate(sorted_changepoints):
                if i >= cp:
                    regime[i] = j + 1
        
        # Select appropriate mean for each observation
        mu = pm.Deterministic('mu', means[regime])
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=mu, sd=sigma, observed=data)
    
    return model

def run_mcmc_sampling(model, draws=2000, tune=1000):
    """
    Run MCMC sampling for the change point model.
    
    Args:
        model (pm.Model): PyMC3 model
        draws (int): Number of posterior samples
        tune (int): Number of tuning steps
        
    Returns:
        pm.backends.base.MultiTrace: MCMC trace
    """
    print("Running MCMC sampling...")
    
    with model:
        trace = pm.sample(draws=draws, tune=tune, return_inferencedata=True)
    
    return trace

def analyze_convergence(trace):
    """
    Analyze MCMC convergence.
    
    Args:
        trace: MCMC trace object
    """
    print("\n=== Convergence Analysis ===")
    
    # Summary statistics
    summary = az.summary(trace)
    print("\nParameter Summary:")
    print(summary)
    
    # Check R-hat values
    r_hat_values = summary['r_hat']
    print(f"\nR-hat values range: {r_hat_values.min():.3f} to {r_hat_values.max():.3f}")
    
    if r_hat_values.max() < 1.1:
        print("✓ Model has converged (all R-hat < 1.1)")
    else:
        print("⚠ Warning: Some parameters may not have converged")
    
    return summary

def plot_trace(trace, save_path='../../reports/trace_plots.png'):
    """
    Plot MCMC trace plots.
    
    Args:
        trace: MCMC trace object
        save_path (str): Path to save the plot
    """
    print("Creating trace plots...")
    
    az.plot_trace(trace)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Trace plots saved to {save_path}")

def plot_changepoint_posteriors(trace, dates, save_path='../../reports/changepoint_posteriors.png'):
    """
    Plot posterior distributions of change points.
    
    Args:
        trace: MCMC trace object
        dates (pd.DatetimeIndex): Date index
        save_path (str): Path to save the plot
    """
    print("Creating change point posterior plots...")
    
    # Extract change point samples
    changepoint_samples = trace.posterior['sorted_changepoints'].values
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i in range(4):  # Plot first 4 change points
        if i < changepoint_samples.shape[1]:
            # Convert to dates
            cp_dates = [dates[int(cp)] for cp in changepoint_samples[:, i, :].flatten()]
            
            axes[i].hist(cp_dates, bins=30, alpha=0.7, color=f'C{i}')
            axes[i].set_title(f'Change Point {i+1} Posterior Distribution')
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel('Frequency')
            axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Change point posterior plots saved to {save_path}")

def extract_changepoint_dates(trace, dates, confidence_level=0.95):
    """
    Extract change point dates with confidence intervals.
    
    Args:
        trace: MCMC trace object
        dates (pd.DatetimeIndex): Date index
        confidence_level (float): Confidence level for intervals
        
    Returns:
        dict: Change point information
    """
    print("Extracting change point dates...")
    
    changepoint_samples = trace.posterior['sorted_changepoints'].values
    n_changepoints = changepoint_samples.shape[1]
    
    changepoint_info = {}
    
    for i in range(n_changepoints):
        # Convert samples to dates
        cp_dates = [dates[int(cp)] for cp in changepoint_samples[:, i, :].flatten()]
        
        # Calculate statistics
        mean_date = np.mean(cp_dates)
        median_date = np.median(cp_dates)
        
        # Calculate confidence interval
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower_date = np.percentile(cp_dates, lower_percentile)
        upper_date = np.percentile(cp_dates, upper_percentile)
        
        changepoint_info[f'cp_{i+1}'] = {
            'mean_date': mean_date,
            'median_date': median_date,
            'lower_ci': lower_date,
            'upper_ci': upper_date,
            'confidence_level': confidence_level
        }
        
        print(f"Change Point {i+1}:")
        print(f"  Mean: {mean_date.strftime('%Y-%m-%d')}")
        print(f"  Median: {median_date.strftime('%Y-%m-%d')}")
        print(f"  {confidence_level*100}% CI: {lower_date.strftime('%Y-%m-%d')} to {upper_date.strftime('%Y-%m-%d')}")
    
    return changepoint_info

def compare_regime_parameters(trace):
    """
    Compare parameters between different regimes.
    
    Args:
        trace: MCMC trace object
    """
    print("\n=== Regime Parameter Comparison ===")
    
    # Extract mean parameters
    means_samples = trace.posterior['means'].values
    
    for i in range(means_samples.shape[1]):
        regime_means = means_samples[:, i, :].flatten()
        print(f"Regime {i+1} mean: {np.mean(regime_means):.6f} ± {np.std(regime_means):.6f}")

def save_results(changepoint_info, file_path='../../reports/changepoint_results.csv'):
    """
    Save change point results to CSV.
    
    Args:
        changepoint_info (dict): Change point information
        file_path (str): Path to save results
    """
    print(f"Saving results to {file_path}...")
    
    results = []
    for cp_name, cp_data in changepoint_info.items():
        results.append({
            'change_point': cp_name,
            'mean_date': cp_data['mean_date'].strftime('%Y-%m-%d'),
            'median_date': cp_data['median_date'].strftime('%Y-%m-%d'),
            'lower_ci': cp_data['lower_ci'].strftime('%Y-%m-%d'),
            'upper_ci': cp_data['upper_ci'].strftime('%Y-%m-%d'),
            'confidence_level': cp_data['confidence_level']
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(file_path, index=False)
    print("Results saved successfully!")

def main():
    """
    Main function to run the change point analysis.
    """
    print("=== Bayesian Change Point Analysis ===\n")
    
    # Load data
    df = load_processed_data()
    
    # Use log returns for analysis
    data = df['log_returns'].values
    dates = df.index
    
    # Build model
    model = simple_change_point_model(data, n_changepoints=3)
    
    # Run MCMC sampling
    trace = run_mcmc_sampling(model)
    
    # Analyze convergence
    summary = analyze_convergence(trace)
    
    # Create plots
    plot_trace(trace)
    plot_changepoint_posteriors(trace, dates)
    
    # Extract change point dates
    changepoint_info = extract_changepoint_dates(trace, dates)
    
    # Compare regime parameters
    compare_regime_parameters(trace)
    
    # Save results
    save_results(changepoint_info)
    
    print("\n=== Change Point Analysis Complete ===")
    print("Results are ready for event correlation analysis!")

if __name__ == "__main__":
    main() 