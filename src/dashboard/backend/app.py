"""
Flask backend API for Brent Oil Price Change Point Analysis Dashboard.
Serves data and analysis results to the React frontend.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Data paths
DATA_DIR = '../../data'
REPORTS_DIR = '../../reports'

def load_brent_data():
    """Load Brent oil price data."""
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'BrentOilPrices.csv'))
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
        df = df.dropna().sort_values('Date')
        return df
    except Exception as e:
        print(f"Error loading Brent data: {e}")
        return None

def load_events_data():
    """Load major events data."""
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'major_events.csv'))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        print(f"Error loading events data: {e}")
        return None

def load_processed_data():
    """Load processed data with log returns."""
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'processed_brent_data.csv'), 
                        index_col=0, parse_dates=True)
        return df
    except Exception as e:
        print(f"Error loading processed data: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Brent Oil Analysis API is running'
    })

@app.route('/api/data/brent-prices', methods=['GET'])
def get_brent_prices():
    """Get Brent oil price data."""
    df = load_brent_data()
    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500
    
    # Convert to JSON-serializable format
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'price': float(row['Price'])
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m-%d'),
            'end': df['Date'].max().strftime('%Y-%m-%d')
        }
    })

@app.route('/api/data/events', methods=['GET'])
def get_events():
    """Get major events data."""
    df = load_events_data()
    if df is None:
        return jsonify({'error': 'Failed to load events data'}), 500
    
    # Convert to JSON-serializable format
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'event': row['Event'],
            'category': row['Category'],
            'description': row['Description'],
            'impact_score': int(row['Impact_Score']),
            'region': row['Region']
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'categories': df['Category'].unique().tolist(),
        'regions': df['Region'].unique().tolist()
    })

@app.route('/api/data/log-returns', methods=['GET'])
def get_log_returns():
    """Get log returns data."""
    df = load_processed_data()
    if df is None:
        return jsonify({'error': 'Failed to load processed data'}), 500
    
    # Convert to JSON-serializable format
    data = []
    for date, row in df.iterrows():
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'log_returns': float(row['log_returns']),
            'volatility': float(row.get('volatility', 0)),
            'high_volatility': bool(row.get('high_volatility', False))
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'statistics': {
            'mean': float(df['log_returns'].mean()),
            'std': float(df['log_returns'].std()),
            'min': float(df['log_returns'].min()),
            'max': float(df['log_returns'].max())
        }
    })

@app.route('/api/analysis/summary', methods=['GET'])
def get_analysis_summary():
    """Get analysis summary statistics."""
    df = load_processed_data()
    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500
    
    # Calculate summary statistics
    summary = {
        'total_observations': len(df),
        'date_range': {
            'start': df.index.min().strftime('%Y-%m-%d'),
            'end': df.index.max().strftime('%Y-%m-%d')
        },
        'price_statistics': {
            'mean': float(df['Price'].mean()),
            'std': float(df['Price'].std()),
            'min': float(df['Price'].min()),
            'max': float(df['Price'].max())
        },
        'returns_statistics': {
            'mean': float(df['log_returns'].mean()),
            'std': float(df['log_returns'].std()),
            'min': float(df['log_returns'].min()),
            'max': float(df['log_returns'].max())
        }
    }
    
    # Add volatility statistics if available
    if 'volatility' in df.columns:
        summary['volatility_statistics'] = {
            'mean': float(df['volatility'].mean()),
            'std': float(df['volatility'].std()),
            'high_volatility_periods': int(df['high_volatility'].sum())
        }
    
    return jsonify(summary)

@app.route('/api/analysis/volatility-periods', methods=['GET'])
def get_volatility_periods():
    """Get high volatility periods."""
    df = load_processed_data()
    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500
    
    if 'high_volatility' not in df.columns:
        return jsonify({'error': 'Volatility data not available'}), 404
    
    # Get high volatility periods
    high_vol_periods = df[df['high_volatility']]
    
    data = []
    for date, row in high_vol_periods.iterrows():
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': float(row['Price']),
            'log_returns': float(row['log_returns']),
            'volatility': float(row['volatility'])
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'total_periods': len(df),
        'percentage': round(len(data) / len(df) * 100, 2)
    })

@app.route('/api/events/near-date', methods=['GET'])
def get_events_near_date():
    """Get events within a specified date range."""
    date_str = request.args.get('date')
    days = int(request.args.get('days', 30))
    
    if not date_str:
        return jsonify({'error': 'Date parameter required'}), 400
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    df = load_events_data()
    if df is None:
        return jsonify({'error': 'Failed to load events data'}), 500
    
    # Find events within the specified range
    start_date = target_date - pd.Timedelta(days=days)
    end_date = target_date + pd.Timedelta(days=days)
    
    nearby_events = df[
        (df['Date'] >= start_date) & 
        (df['Date'] <= end_date)
    ].copy()
    
    # Add distance in days
    nearby_events['days_from_target'] = (nearby_events['Date'] - target_date).dt.days
    
    # Convert to JSON-serializable format
    data = []
    for _, row in nearby_events.iterrows():
        data.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'event': row['Event'],
            'category': row['Category'],
            'description': row['Description'],
            'impact_score': int(row['Impact_Score']),
            'region': row['Region'],
            'days_from_target': int(row['days_from_target'])
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'target_date': date_str,
        'search_range_days': days
    })

@app.route('/api/analysis/price-changes', methods=['GET'])
def get_price_changes():
    """Get significant price changes."""
    df = load_processed_data()
    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500
    
    # Calculate price changes
    df['price_change'] = df['Price'].pct_change()
    df['price_change_abs'] = df['price_change'].abs()
    
    # Get top price changes
    threshold = float(request.args.get('threshold', 0.05))  # 5% default
    significant_changes = df[df['price_change_abs'] >= threshold].copy()
    
    # Sort by absolute change
    significant_changes = significant_changes.sort_values('price_change_abs', ascending=False)
    
    # Limit results
    limit = int(request.args.get('limit', 50))
    significant_changes = significant_changes.head(limit)
    
    data = []
    for date, row in significant_changes.iterrows():
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': float(row['Price']),
            'price_change': float(row['price_change']),
            'price_change_pct': float(row['price_change'] * 100),
            'log_returns': float(row['log_returns'])
        })
    
    return jsonify({
        'data': data,
        'count': len(data),
        'threshold': threshold,
        'total_observations': len(df)
    })

if __name__ == '__main__':
    print("Starting Brent Oil Analysis API...")
    print("Available endpoints:")
    print("  GET /api/health - Health check")
    print("  GET /api/data/brent-prices - Brent oil price data")
    print("  GET /api/data/events - Major events data")
    print("  GET /api/data/log-returns - Log returns data")
    print("  GET /api/analysis/summary - Analysis summary")
    print("  GET /api/analysis/volatility-periods - High volatility periods")
    print("  GET /api/events/near-date?date=YYYY-MM-DD&days=30 - Events near date")
    print("  GET /api/analysis/price-changes?threshold=0.05&limit=50 - Significant price changes")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 