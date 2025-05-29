import numpy as np
import pandas as pd

def evaluate_performance(df, returns_col='returns', risk_free_rate=0.0):
    """
    Evaluate profitability and key financial metrics: Sharpe, Sortino, Alpha, Beta.
    """
    returns = df[returns_col]
    excess_returns = returns - risk_free_rate / 252
    sharpe = np.sqrt(252) * excess_returns.mean() / (excess_returns.std() + 1e-8)
    downside_std = returns[returns < 0].std()
    sortino = np.sqrt(252) * excess_returns.mean() / (downside_std + 1e-8)
    # Alpha/Beta vs. benchmark (assume 'benchmark_returns' in df)
    if 'benchmark_returns' in df.columns:
        cov = np.cov(returns, df['benchmark_returns'])[0][1]
        beta = cov / (df['benchmark_returns'].var() + 1e-8)
        alpha = returns.mean() - beta * df['benchmark_returns'].mean()
    else:
        alpha, beta = np.nan, np.nan
    return {
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'alpha': alpha,
        'beta': beta
    }

def calculate_var_drawdown(df, returns_col='returns', confidence_level=0.05):
    """
    Calculate Value at Risk (VaR) and drawdowns.
    """
    returns = df[returns_col]
    var = np.percentile(returns, 100 * confidence_level)
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    return {
        'VaR': var,
        'max_drawdown': max_drawdown
    }

def simulate_execution_latency(df, latency_ms=100, price_col='Close'):
    """
    Simulate execution latency by shifting trade signals and prices.
    """
    latency_periods = int(latency_ms / 1000 * 252 * 6.5 * 60)  # Approx. periods per trading day
    df = df.copy()
    df['executed_price'] = df[price_col].shift(-latency_periods)
    return df

# Example usage (to be removed or placed under __main__ guard in production)
# perf = evaluate_performance(trades_df)
# risk = calculate_var_drawdown(trades_df)
# trades_with_latency = simulate_execution_latency(trades_df)