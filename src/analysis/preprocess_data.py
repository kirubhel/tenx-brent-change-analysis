"""
Data preprocessing script for Brent oil price analysis.
Loads and prepares data for change point analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_brent_data(file_path='../../data/BrentOilPrices.csv'):
    """
    Load and preprocess Brent oil price data.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned time series data
    """
    print("Loading Brent oil price data...")
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    
    # Handle missing dates
    df = df.dropna()
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Set date as index
    df.set_index('Date', inplace=True)
    
    print(f"Loaded {len(df)} records from {df.index.min()} to {df.index.max()}")
    return df

def calculate_returns(df):
    """
    Calculate log returns from price data.
    
    Args:
        df (pd.DataFrame): Price data with Date index
        
    Returns:
        pd.DataFrame: Data with log returns added
    """
    print("Calculating log returns...")
    
    # Calculate log returns
    df['log_returns'] = np.log(df['Price'] / df['Price'].shift(1))
    
    # Remove first row (NaN)
    df = df.dropna()
    
    return df

def basic_statistics(df):
    """
    Calculate basic statistics for the time series.
    
    Args:
        df (pd.DataFrame): Time series data
    """
    print("\n=== Basic Statistics ===")
    print(f"Total observations: {len(df)}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Price range: ${df['Price'].min():.2f} to ${df['Price'].max():.2f}")
    print(f"Mean price: ${df['Price'].mean():.2f}")
    print(f"Price volatility: {df['Price'].std():.2f}")
    print(f"Log returns mean: {df['log_returns'].mean():.6f}")
    print(f"Log returns std: {df['log_returns'].std():.6f}")

def plot_time_series(df, save_path='../../reports/price_timeseries.png'):
    """
    Create time series plots for prices and returns.
    
    Args:
        df (pd.DataFrame): Time series data
        save_path (str): Path to save the plot
    """
    print("Creating time series plots...")
    
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    # Price plot
    axes[0].plot(df.index, df['Price'], linewidth=0.5, alpha=0.8)
    axes[0].set_title('Brent Oil Prices (1987-2022)', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Price (USD/barrel)')
    axes[0].grid(True, alpha=0.3)
    
    # Log returns plot
    axes[1].plot(df.index, df['log_returns'], linewidth=0.5, alpha=0.8, color='orange')
    axes[1].set_title('Log Returns', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Log Returns')
    axes[1].set_xlabel('Date')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Plot saved to {save_path}")

def plot_distributions(df, save_path='../../reports/distributions.png'):
    """
    Create distribution plots for prices and returns.
    
    Args:
        df (pd.DataFrame): Time series data
        save_path (str): Path to save the plot
    """
    print("Creating distribution plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Price distribution
    axes[0,0].hist(df['Price'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,0].set_title('Price Distribution')
    axes[0,0].set_xlabel('Price (USD/barrel)')
    axes[0,0].set_ylabel('Frequency')
    
    # Log returns distribution
    axes[0,1].hist(df['log_returns'], bins=50, alpha=0.7, color='orange', edgecolor='black')
    axes[0,1].set_title('Log Returns Distribution')
    axes[0,1].set_xlabel('Log Returns')
    axes[0,1].set_ylabel('Frequency')
    
    # Price box plot
    axes[1,0].boxplot(df['Price'])
    axes[1,0].set_title('Price Box Plot')
    axes[1,0].set_ylabel('Price (USD/barrel)')
    
    # Log returns box plot
    axes[1,1].boxplot(df['log_returns'])
    axes[1,1].set_title('Log Returns Box Plot')
    axes[1,1].set_ylabel('Log Returns')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Plot saved to {save_path}")

def identify_volatility_periods(df, window=30):
    """
    Identify periods of high volatility.
    
    Args:
        df (pd.DataFrame): Time series data
        window (int): Rolling window size for volatility calculation
        
    Returns:
        pd.DataFrame: Data with volatility measures
    """
    print("Identifying volatility periods...")
    
    # Calculate rolling volatility
    df['volatility'] = df['log_returns'].rolling(window=window).std()
    
    # Identify high volatility periods (above 95th percentile)
    volatility_threshold = df['volatility'].quantile(0.95)
    df['high_volatility'] = df['volatility'] > volatility_threshold
    
    print(f"High volatility threshold: {volatility_threshold:.4f}")
    print(f"High volatility periods: {df['high_volatility'].sum()} days")
    
    return df

def save_processed_data(df, file_path='../../data/processed_brent_data.csv'):
    """
    Save processed data for further analysis.
    
    Args:
        df (pd.DataFrame): Processed time series data
        file_path (str): Path to save the processed data
    """
    print(f"Saving processed data to {file_path}...")
    df.to_csv(file_path)
    print("Data saved successfully!")

def main():
    """
    Main function to run the data preprocessing pipeline.
    """
    print("=== Brent Oil Price Data Preprocessing ===\n")
    
    # Load data
    df = load_brent_data()
    
    # Calculate returns
    df = calculate_returns(df)
    
    # Basic statistics
    basic_statistics(df)
    
    # Create visualizations
    plot_time_series(df)
    plot_distributions(df)
    
    # Identify volatility periods
    df = identify_volatility_periods(df)
    
    # Save processed data
    save_processed_data(df)
    
    print("\n=== Preprocessing Complete ===")
    print("Data is ready for change point analysis!")

if __name__ == "__main__":
    main() 