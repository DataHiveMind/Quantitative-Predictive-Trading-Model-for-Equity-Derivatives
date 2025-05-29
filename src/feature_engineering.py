import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from sklearn.decomposition import PCA

def extract_time_series_signals(df, price_col='Close'):
    """
    Extract time-series signals such as volatility and trend.
    """
    # Volatility (rolling standard deviation)
    df['volatility_20'] = df[price_col].rolling(window=20).std()
    # Trend (using rolling mean)
    df['trend_20'] = df[price_col].rolling(window=20).mean()
    # Stationarity test (ADF p-value)
    result = adfuller(df[price_col].dropna())
    df['adf_pvalue'] = result[1]
    return df

def compute_technical_indicators(df, price_col='Close'):
    """
    Compute technical indicators: RSI, Bollinger Bands, Moving Averages.
    """
    # Moving Average
    df['ma_20'] = df[price_col].rolling(window=20).mean()
    # Bollinger Bands
    df['bb_upper'] = df['ma_20'] + 2 * df[price_col].rolling(window=20).std()
    df['bb_lower'] = df['ma_20'] - 2 * df[price_col].rolling(window=20).std()
    # RSI
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi_14'] = 100 - (100 / (1 + rs))
    return df

def perform_pca(df, n_components=5, exclude_cols=None):
    """
    Perform PCA/dimensionality reduction on the feature space.
    """
    if exclude_cols is None:
        exclude_cols = []
    feature_cols = df.select_dtypes(include=[np.number]).columns.difference(exclude_cols)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df[feature_cols].fillna(0))
    for i in range(n_components):
        df[f'pca_{i+1}'] = principal_components[:, i]
    return df, pca

# Example usage (to be removed or placed under __main__ guard in production)
# df = extract_time_series_signals(df)
# df = compute_technical_indicators(df)
# df, pca_model = perform_pca(df, n_components=5)