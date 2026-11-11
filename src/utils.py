# Grafik ve yardimci fonksiyonlar

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_target_distributions(df):
    """Hedeflerin (Tg ve Tc) dağılım grafiklerini çizer."""
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['Tg'].dropna(), kde=True, color='blue', bins=30)
    plt.title('Tg (Glass Transition Temp) Dağılımı')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['Tc'].dropna(), kde=True, color='red', bins=30)
    plt.title('Tc (Melting Temp) Dağılımı')
    
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df):
    """Sayısal değişkenler arası korelasyonu çizer."""
    plt.figure(figsize=(8, 6))
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Sayısal Değişkenler Korelasyon Haritası')
    plt.show()

def analyze_missing_values(df):
    """Verisetindeki eksik değerlerin sayısını, yüzdesini raporlar ve Barplot çizer."""
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'Eksik_Sayisi': missing, 'Yuzde(%)': missing_percent})
    missing_df = missing_df[missing_df['Eksik_Sayisi'] > 0].sort_values(by='Yuzde(%)', ascending=False)
    
    print("\n--- Eksik Veri Analizi ---")
    if missing_df.empty:
        print("Verisetinde eksik değer bulunmamaktadır.")
    else:
        print(missing_df)
        
        # Eksik verileri Barplot ile görselleştirme (Uyarı vermeyen modern versiyon)
        plt.figure(figsize=(10, 5))
        sns.barplot(data=missing_df.reset_index(), x='Yuzde(%)', y='index', hue='index', palette='viridis', legend=False)
        plt.title('Eksik Veri Yüzdeleri (Missing Values)')
        plt.xlabel('Eksik Oranı (%)')
        plt.ylabel('Öznitelikler')
        plt.tight_layout()
        plt.show()

def plot_boxplots(df):
    """Sayısal sütunlardaki aykırı değerleri (outliers) görmek için kutu grafiği çizer."""
    plt.figure(figsize=(12, 6))
    numeric_df = df.select_dtypes(include=['float64', 'int64']).drop(columns=['id'], errors='ignore')
    sns.boxplot(data=numeric_df, orient='h')
    plt.title('Sayısal Değişkenler Aykırı Değer (Outlier) Analizi')
    plt.show()
