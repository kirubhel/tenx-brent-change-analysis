"""
Simplified Change Point Analysis for Brent Oil Prices.
Uses statistical methods to identify structural breaks without PyMC3.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_processed_data(file_path='../../data/processed_brent_data.csv'):
    """Load processed Brent oil price data."""
    print("Loading processed data...")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"Loaded {len(df)} observations")
    return df

def detect_change_points_rolling_mean(data, window=252, threshold=2.0):
    """
    Detect change points using rolling mean comparison.
    
    Args:
        data (pd.Series): Time series data
        window (int): Rolling window size (252 = 1 year)
        threshold (float): Standard deviation threshold for change detection
        
    Returns:
        list: Indices of detected change points
    """
    print("Detecting change points using rolling mean analysis...")
    
    # Calculate rolling mean and standard deviation
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    
    # Calculate z-score of current value vs rolling mean
    z_scores = np.abs((data - rolling_mean) / rolling_std)
    
    # Find points where z-score exceeds threshold
    change_points = z_scores > threshold
    
    # Get indices of change points
    change_point_indices = change_points[change_points].index.tolist()
    
    print(f"Detected {len(change_point_indices)} potential change points")
    return change_point_indices

def detect_volatility_changes(data, window=60, threshold=1.5):
    """
    Detect changes in volatility using rolling standard deviation.
    
    Args:
        data (pd.Series): Time series data (log returns)
        window (int): Rolling window size
        threshold (float): Threshold for volatility change detection
        
    Returns:
        list: Indices of volatility change points
    """
    print("Detecting volatility change points...")
    
    # Calculate rolling volatility
    rolling_vol = data.rolling(window=window).std()
    
    # Calculate volatility changes
    vol_changes = rolling_vol.pct_change()
    
    # Find significant volatility changes
    vol_change_points = np.abs(vol_changes) > threshold
    
    # Get indices
    vol_change_indices = vol_change_points[vol_change_points].index.tolist()
    
    print(f"Detected {len(vol_change_indices)} volatility change points")
    return vol_change_indices

def analyze_regime_changes(df, change_points):
    """
    Analyze regime changes at detected change points.
    
    Args:
        df (pd.DataFrame): Data with prices and returns
        change_points (list): List of change point dates
        
    Returns:
        dict: Analysis results
    """
    print("Analyzing regime changes...")
    
    results = {}
    
    for i, cp_date in enumerate(change_points):
        # Define periods before and after change point
        before_period = df[df.index < cp_date].tail(252)  # 1 year before
        after_period = df[df.index > cp_date].head(252)   # 1 year after
        
        if len(before_period) > 0 and len(after_period) > 0:
            # Calculate statistics
            before_mean = before_period['Price'].mean()
            after_mean = after_period['Price'].mean()
            before_vol = before_period['log_returns'].std()
            after_vol = after_period['log_returns'].std()
            
            # Calculate changes
            price_change = ((after_mean - before_mean) / before_mean) * 100
            vol_change = ((after_vol - before_vol) / before_vol) * 100
            
            results[f'cp_{i+1}'] = {
                'date': cp_date,
                'before_mean': before_mean,
                'after_mean': after_mean,
                'before_vol': before_vol,
                'after_vol': after_vol,
                'price_change_pct': price_change,
                'vol_change_pct': vol_change
            }
    
    return results

def plot_change_points(df, change_points, save_path='../../reports/change_points_analysis.png'):
    """Plot change points on price series."""
    print("Creating change point visualization...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # Price plot with change points
    ax1.plot(df.index, df['Price'], linewidth=0.5, alpha=0.8, label='Brent Oil Price')
    
    # Mark change points
    for cp_date in change_points:
        if cp_date in df.index:
            price_at_cp = df.loc[cp_date, 'Price']
            ax1.scatter(cp_date, price_at_cp, color='red', s=50, zorder=5)
            ax1.annotate(f'CP: {cp_date.strftime("%Y-%m")}', 
                        xy=(cp_date, price_at_cp), 
                        xytext=(10, 10), textcoords='offset points',
                        fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax1.set_title('Brent Oil Prices with Detected Change Points', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Price (USD/barrel)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Log returns plot
    ax2.plot(df.index, df['log_returns'], linewidth=0.5, alpha=0.8, color='orange', label='Log Returns')
    ax2.set_title('Log Returns', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Log Returns')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Change point plot saved to {save_path}")

def correlate_with_events(change_points, events_file='../../data/major_events.csv', days_threshold=30):
    """
    Correlate detected change points with major events.
    
    Args:
        change_points (list): Detected change point dates
        events_file (str): Path to events CSV file
        days_threshold (int): Days threshold for correlation
        
    Returns:
        dict: Event correlations
    """
    print("Correlating change points with major events...")
    
    # Load events data
    events_df = pd.read_csv(events_file)
    events_df['Date'] = pd.to_datetime(events_df['Date'])
    
    correlations = {}
    
    for i, cp_date in enumerate(change_points):
        cp_correlations = []
        
        for _, event in events_df.iterrows():
            event_date = event['Date']
            days_diff = abs((cp_date - event_date).days)
            
            if days_diff <= days_threshold:
                cp_correlations.append({
                    'event': event['Event'],
                    'event_date': event_date,
                    'days_diff': days_diff,
                    'category': event['Category'],
                    'impact_score': event['Impact_Score'],
                    'description': event['Description']
                })
        
        if cp_correlations:
            # Sort by days difference
            cp_correlations.sort(key=lambda x: x['days_diff'])
            correlations[f'cp_{i+1}'] = {
                'change_point_date': cp_date,
                'correlated_events': cp_correlations
            }
    
    return correlations

def save_results(change_points, regime_analysis, event_correlations, file_path='../../reports/change_point_results.csv'):
    """Save analysis results to CSV."""
    print(f"Saving results to {file_path}...")
    
    results = []
    for cp_name, cp_data in regime_analysis.items():
        if cp_name in event_correlations:
            events = event_correlations[cp_name]['correlated_events']
            if events:
                best_event = events[0]  # Closest event
                results.append({
                    'change_point': cp_name,
                    'date': cp_data['date'].strftime('%Y-%m-%d'),
                    'before_mean_price': round(cp_data['before_mean'], 2),
                    'after_mean_price': round(cp_data['after_mean'], 2),
                    'price_change_pct': round(cp_data['price_change_pct'], 2),
                    'vol_change_pct': round(cp_data['vol_change_pct'], 2),
                    'correlated_event': best_event['event'],
                    'event_date': best_event['event_date'].strftime('%Y-%m-%d'),
                    'days_diff': best_event['days_diff'],
                    'event_category': best_event['category'],
                    'impact_score': best_event['impact_score']
                })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(file_path, index=False)
    print("Results saved successfully!")

def main():
    """Main function to run the simplified change point analysis."""
    print("=== Simplified Change Point Analysis ===\n")
    
    # Load data
    df = load_processed_data()
    
    # Detect change points using price data
    price_change_points = detect_change_points_rolling_mean(df['Price'], window=252, threshold=2.0)
    
    # Detect volatility change points
    vol_change_points = detect_volatility_changes(df['log_returns'], window=60, threshold=1.5)
    
    # Combine change points (remove duplicates)
    all_change_points = list(set(price_change_points + vol_change_points))
    all_change_points.sort()
    
    print(f"\nTotal unique change points detected: {len(all_change_points)}")
    
    # Analyze regime changes
    regime_analysis = analyze_regime_changes(df, all_change_points)
    
    # Correlate with events
    event_correlations = correlate_with_events(all_change_points)
    
    # Create visualizations
    plot_change_points(df, all_change_points)
    
    # Save results
    save_results(all_change_points, regime_analysis, event_correlations)
    
    # Print summary
    print("\n=== Analysis Summary ===")
    print(f"Total change points detected: {len(all_change_points)}")
    print(f"Change points with event correlations: {len(event_correlations)}")
    
    for cp_name, cp_data in regime_analysis.items():
        if cp_name in event_correlations:
            events = event_correlations[cp_name]['correlated_events']
            if events:
                best_event = events[0]
                print(f"\n{cp_name} ({cp_data['date'].strftime('%Y-%m-%d')}):")
                print(f"  Price change: {cp_data['price_change_pct']:.2f}%")
                print(f"  Volatility change: {cp_data['vol_change_pct']:.2f}%")
                print(f"  Correlated event: {best_event['event']} ({best_event['days_diff']} days)")
                print(f"  Event category: {best_event['category']} (Impact: {best_event['impact_score']}/9)")
    
    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    main() 