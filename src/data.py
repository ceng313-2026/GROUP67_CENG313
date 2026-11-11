# Veri isleme fonksiyonlari

import pandas as pd
import os

def load_data(data_path="data/train.csv"):
    """Belirtilen yoldaki CSV dosyasını okur."""
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"Veri başarıyla yüklendi! Boyut: {df.shape}")
        return df
    else:
        print(f"Hata: {data_path} dosyası bulunamadı.")
        return None

def preprocess_data(df):
    """
    Eksik verileri doldurur ve makine öğrenmesi için temel ön işleme yapar.
    Aykırı değerler (outliers) olduğu için eksikler MEDYAN ile doldurulur.
    """
    df_processed = df.copy()
    
    # Sadece sayısal sütunları seç
    numeric_cols = df_processed.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_cols:
        if col != 'id':  # id sütununu doldurmaya gerek yok
            # Her sütundaki boşlukları (NaN), o sütunun medyanı ile doldur
            df_processed[col] = df_processed[col].fillna(df_processed[col].median())
            
    print("Veri ön işleme tamamlandı. Tüm eksik sayısal değerler medyan ile dolduruldu.")
    return df_processed
