#gerekli kütüphaneleri import edelim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def city_spending(merged_data):
    city_spending = merged_data.groupby('sehir')['harcama_miktari'].sum().reset_index()

    # Şehirleri en çok harcama yapanlara göre sıralama
    city_spending_sorted = city_spending.sort_values(by='harcama_miktari', ascending=False)

    # Sonuçları yazdırma
    print(city_spending_sorted)

    # Grafik ile görselleştirme
    plt.figure(figsize=(12, 6))
    plt.bar(city_spending_sorted['sehir'], city_spending_sorted['harcama_miktari'], color='blue')

    # Başlık ve etiketler
    plt.title('Şehir Bazında Toplam Harcama Miktarı')
    plt.xlabel('Şehir')
    plt.ylabel('Toplam Harcama Miktarı')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()


def mean_sales_data(sales_data):
    sales_data['tarih'] = pd.to_datetime(sales_data['tarih'], dayfirst=True,errors='coerce')
    sales_data['ay'] = sales_data['tarih'].dt.to_period('M')  # Ay bazında periyot ekleyelim

    # Ürün ve ay bazında toplam satış miktarını hesapla
    monthly_sales_per_product = sales_data.groupby(['ürün_adi', 'ay'])['toplam_satis'].sum().reset_index()

    # Önceki aya göre değişim yüzdesini hesaplama
    monthly_sales_per_product['sales_change'] = monthly_sales_per_product.groupby('ürün_adi')[
                                                    'toplam_satis'].pct_change() * 100

    # Ortalama satış değişim yüzdesini hesapla
    average_sales_change = monthly_sales_per_product.groupby('ürün_adi')['sales_change'].mean().reset_index()

    # Sonuçları yazdırma
    print(average_sales_change)

    # Grafik ile görselleştirme
    import matplotlib.pyplot as plt

    # Bar chart ile her ürün için ortalama satış artışını görselleştir
    plt.figure(figsize=(14, 7))
    plt.bar(average_sales_change['ürün_adi'], average_sales_change['sales_change'], color='blue')

    # Başlık ve etiketler
    plt.title('Ürün Bazında Ortalama Satış Artışı')
    plt.xlabel('Ürün Adı')
    plt.ylabel('Ortalama Satış Artışı (%)')
    plt.xticks(rotation=90)
    plt.grid(True)

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()


def mean_category(sales_data):
    # 'tarih' sütununu tarih formatına dönüştür
    sales_data['tarih'] = pd.to_datetime(sales_data['tarih'], dayfirst=True,errors='coerce')

    # 'ay' sütunu ekleyelim (yıl-ay formatında)
    sales_data['ay'] = sales_data['tarih'].dt.to_period('M')

    # Kategori bazında aylık satış satır sayısını hesaplama
    monthly_sales_count_by_category = sales_data.groupby(['kategori', 'ay']).size().reset_index(name='satir_sayisi')

    # Aylık değişim oranını hesaplamak
    monthly_sales_count_by_category['sales_change'] = monthly_sales_count_by_category.groupby('kategori')[
                                                          'satir_sayisi'].pct_change() * 100

    # Kategorilere göre değişim oranını görselleştirme
    plt.figure(figsize=(14, 8))

    # Her kategori için ayrı bir çizgi grafiği çizeceğiz
    for category in monthly_sales_count_by_category['kategori'].unique():
        category_data = monthly_sales_count_by_category[monthly_sales_count_by_category['kategori'] == category]
        plt.plot(category_data['ay'].astype(str), category_data['sales_change'],linewidth=2.5, label=category)

    # Başlık ve etiketler
    plt.title('Kategorilere Göre Aylık Satış Sayısı Değişim Oranları')
    plt.xlabel('Tarih(Ay)')
    plt.ylabel('Aylık Satış Değişim Oranı (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.grid(True)

    # Efsane ekleme
    plt.legend()

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()
