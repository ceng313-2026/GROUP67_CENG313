# Yapay zeka modelleri
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_baseline_model(df, target_col='Tg'):
    print(f"--- Baseline Modeller Eğitiliyor (Hedef: {target_col}) ---")
    data = df.dropna(subset=[target_col]).copy()
    X = data['SMILES'].apply(len).values.reshape(-1, 1)
    y = data[target_col].values
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    results = {}
    
    models = {
        'Dummy (Mean)': DummyRegressor(strategy='mean'),
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    for name, m in models.items():
        m.fit(X_tr, y_tr)
        pred = m.predict(X_te)
        results[name] = {
            'MAE': mean_absolute_error(y_te, pred),
            'RMSE': np.sqrt(mean_squared_error(y_te, pred))
        }
        print(f"{name} -> MAE: {results[name]['MAE']:.4f}, RMSE: {results[name]['RMSE']:.4f}")
    
    print("-" * 50)
    return results

def evaluate_all_targets(df):
    targets = ['Tg', 'FFV', 'Tc', 'Density', 'Rg']
    all_results = {}
    for t in targets:
        if t in df.columns:
            all_results[t] = train_baseline_model(df, target_col=t)
    return all_results
