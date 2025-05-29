import os
import json
import yaml
import logging
import time
from typing import Any, Dict

def load_config(filepath: str) -> Dict[str, Any]:
    """
    Load and parse configuration files (YAML or JSON).
    """
    ext = os.path.splitext(filepath)[1].lower()
    with open(filepath, 'r') as f:
        if ext in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif ext == '.json':
            return json.load(f)
        else:
            raise ValueError("Unsupported config file format. Use YAML or JSON.")

def load_env_vars(keys=None) -> Dict[str, str]:
    """
    Load environment variables. If keys is None, load all.
    """
    if keys is None:
        return dict(os.environ)
    return {key: value for key in keys if (value := os.environ.get(key)) is not None}

from typing import Optional

def setup_logger(name: str = 'trading_logger', log_file: Optional[str] = None, level=logging.INFO) -> logging.Logger:
    """
    Provide logging utilities to track performance & errors.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def benchmark(func):
    """
    Decorator to benchmark execution speed of functions.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' executed in {end - start:.4f} seconds.")
        return result
    return wrapper

# Example usage (to be removed or placed under __main__ guard in production)
# config = load_config('config.yaml')
# env_vars = load_env_vars(['API_KEY', 'SECRET'])
# logger = setup_logger(log_file='trading.log')
# @benchmark
# def test_func(): time.sleep(1)
# test_func()