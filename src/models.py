# Yapay zeka modelleri

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

def train_baseline_model(df, target_col='Tg'):
    """
    SMILES metin uzunluğunu basit bir öznitelik (feature) olarak kullanarak
    belirtilen hedef değişken için temel bir makine öğrenmesi modeli eğitir.
    """
    print(f"--- Baseline Model Eğitimi (Hedef: {target_col}) ---")
    
    # 1. Özellik Çıkarımı (Feature Engineering): SMILES string uzunluğunu hesapla
    X = df['SMILES'].apply(len).values.reshape(-1, 1)
    
    # Hedef değişkeni belirle
    y = df[target_col].values
    
    # 2. Veriyi Eğitim (%80) ve Test (%20) olarak ikiye böl
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Temel Modeli Tanımla ve Eğit (Hızlı çalışması için 10 ağaç kullanıyoruz)
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # 4. Test seti üzerinde tahmin yap ve hatayı (RMSE) ölç
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"Model başarıyla eğitildi!")
    print(f"Test Seti Hata Oranı (RMSE): {rmse:.4f}")
    
    return model
