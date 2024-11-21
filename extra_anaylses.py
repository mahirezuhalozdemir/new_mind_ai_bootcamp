#machine learning kütüphaneleri import edelim
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def pareto_anaylse(merged_data):
    merged_data['tarih'] = pd.to_datetime(merged_data['tarih'],dayfirst=True)

    # 2. Her bir ürün adına göre kaç satır olduğunu hesaplayın (satış sıklığını bulmak için)
    product_sales = merged_data.groupby('ürün_adi').size().reset_index(name='satis_adedi')

    # 3. Ürünleri satış sıklığına göre azalan sırayla sıralayın
    product_sales = product_sales.sort_values(by='satis_adedi', ascending=False)

    # 4. Kümülatif yüzdeyi hesaplayın
    product_sales['kümülatif_yüzde'] = product_sales['satis_adedi'].cumsum() / product_sales['satis_adedi'].sum() * 100

    # 5. Pareto grafiği oluşturma
    plt.figure(figsize=(14, 7))

    # Bar grafiği (Toplam satış sıklığı)
    plt.bar(product_sales['ürün_adi'], product_sales['satis_adedi'], color='skyblue', label='Satış Sıklığı')

    # Çizgi grafiği (Kümülatif yüzde)
    plt.plot(product_sales['ürün_adi'], product_sales['kümülatif_yüzde'], color='red', marker='o',
             label='Kümülatif Yüzde', linewidth=2.5)

    # %80 çizgisi
    plt.axhline(80, color='green', linestyle='--', label='%80 Kuralı')

    # Grafik ayarları
    plt.title('Pareto Analizi: Satışların %80’ini Oluşturan Ürünler', fontsize=16)
    plt.xlabel('Ürün Adı', fontsize=14)
    plt.ylabel('Satış Sıklığı', fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()

    # Grafik gösterimi
    plt.show()

def cohort_analyese(merged_data):
    merged_data['tarih'] = pd.to_datetime(merged_data['tarih'],dayfirst=True)
    merged_data['ay'] = merged_data['tarih'].dt.to_period('M')

    # 1. Müşterilerin ilk satın alım ayını belirleyin
    first_purchase = merged_data.groupby('musteri_id')['ay'].min().reset_index()
    first_purchase.columns = ['musteri_id', 'ilk_satinalim_ayi']

    # 2. Orijinal veri setine ilk satın alım ayını ekleyin
    merged_data = merged_data.merge(first_purchase, on='musteri_id')

    # 3. Cohort periyodunu hesaplayın
    merged_data['cohort_periyodu'] = (merged_data['ay'] - merged_data['ilk_satinalim_ayi']).apply(lambda x: x.n)

    # 4. Cohort analizi için pivot tablo oluşturun
    cohort_data = merged_data.pivot_table(
        index='ilk_satinalim_ayi',
        columns='cohort_periyodu',
        values='musteri_id',
        aggfunc='nunique'
    )

    # 5. Her cohort için tekrar alım oranlarını hesaplayın
    cohort_size = cohort_data.iloc[:, 0]
    retention_matrix = cohort_data.divide(cohort_size, axis=0)

    # 6. Cohort analizi görselleştirme
    plt.figure(figsize=(14, 8))
    sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='Blues')
    plt.title('Cohort Analizi: Müşteri Tekrar Alım Oranları')
    plt.xlabel('Aylar Sonrası')
    plt.ylabel('Cohort - İlk Satın Alım Ayı')
    plt.yticks(rotation=0)
    plt.show()

def regression_model(merged_data):
    # Tarih sütununu datetime formatına çevirin
    merged_data['tarih'] = pd.to_datetime(merged_data['tarih'],dayfirst=True)

    # Aylık satış miktarlarını hesaplayın (satır sayısını kullanarak)
    monthly_sales = merged_data.resample('M', on='tarih').size().reset_index(name='toplam_satis')

    # Tarih sütununu yıl ve ay olarak ayırın
    monthly_sales['yil'] = monthly_sales['tarih'].dt.year
    monthly_sales['ay'] = monthly_sales['tarih'].dt.month

    # Özellik ve hedef değişkenleri belirleyin
    X = monthly_sales[['yil', 'ay']]
    y = monthly_sales['toplam_satis']

    # Veriyi %80 train, %20 test olarak ayırın
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modeli oluşturun
    model = LinearRegression()

    # Modeli eğitin
    model.fit(X_train, y_train)

    # Tahminleri yapın
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Eğitim seti hataları
    print("Eğitim Seti:")
    print("MAE:", mean_absolute_error(y_train, y_pred_train))
    print("MSE:", mean_squared_error(y_train, y_pred_train))
    print("R^2:", r2_score(y_train, y_pred_train))

    # Test seti hataları
    print("\nTest Seti:")
    print("MAE:", mean_absolute_error(y_test, y_pred_test))
    print("MSE:", mean_squared_error(y_test, y_pred_test))
    print("R^2:", r2_score(y_test, y_pred_test))

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['tarih'], monthly_sales['toplam_satis'], label='Gerçek Satışlar', marker='o')
    plt.plot(monthly_sales['tarih'].iloc[-len(y_pred_test):], y_pred_test, label='Tahmin Edilen Satışlar', marker='x')
    plt.title('Aylık Satış Miktarlarının Tahmini')
    plt.xlabel('Tarih')
    plt.ylabel('Toplam Satış')
    plt.legend()
    plt.grid(True)
    plt.show()

