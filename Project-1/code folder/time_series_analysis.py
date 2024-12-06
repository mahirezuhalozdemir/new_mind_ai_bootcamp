#gerekli kütüphaneleri import edelim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def convert_to_numeric_and_save(csv_data, column, file_path):
    #Satış verisini sayısal hale getirme
    csv_data[column] = pd.to_numeric(csv_data[column], errors='coerce')

    #Sayısal hale getirilmiş veriyi CSV dosyasına kaydetme
    csv_data.to_csv(file_path, index=False)

    # Kaydedilen dosya yolunu yazdırma
    print(f"{file_path} dosyası başarıyla güncellendi.")


def detect_outliers(csv_data, column):
    # IQR ile aykırı değerleri bulma
    Q1 = csv_data[column].quantile(0.25)
    Q3 = csv_data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_iqr = csv_data[column][(csv_data[column] < lower_bound) | (csv_data[column] > upper_bound)]

    # Normal değerleri aykırı olmayanlar
    normal_values = csv_data[column][(csv_data[column] >= lower_bound) & (csv_data[column] <= upper_bound)]

    return normal_values, outliers_iqr, lower_bound, upper_bound


def replace_outliers_with_mean(csv_data, column, file_path):
    # Aykırı değerleri IQR yöntemi ile buluyoruz
    _,outliers, lower_bound, upper_bound = detect_outliers(csv_data, column)
    # Sütunun ortalama değerini hesaplıyoruz
    non_outliers = csv_data[(csv_data[column] >= lower_bound) & (csv_data[column] <= upper_bound)]
    mean_value = non_outliers[column].mean()  # Yalnızca normal verilerin ortalamasını alıyoruz

    # Aykırı değerleri ortalama ile değiştiriyoruz
    csv_data[column] = csv_data[column].apply(lambda x: mean_value if (x < lower_bound or x > upper_bound) else x)

    # Değişikliklerden sonra veriyi CSV dosyasına kaydediyoruz
    csv_data.to_csv(file_path, index=False)
    print(f"Veri güncellendi ve '{file_path}' dosyasına kaydedildi.")
    #görselleştirip veri dağılımını görelim
    plt.figure(figsize=(10, 6))
    plt.scatter(csv_data.index, csv_data[column], label='Veri Noktaları', color='blue', alpha=0.5)
    plt.xlabel('Index')
    plt.ylabel(column)
    plt.title(f'{column} Aykırı Değerler Görselleştirmesi')
    plt.legend()
    plt.show()

# Histogram ile görselleştirme
def plot_histogram_with_outliers(csv_data, column):
    # IQR aykırı değerlerini bulalım
    normal_values, outliers_iqr,_,_ = detect_outliers(csv_data, column)

    # Histogramı çizelim
    plt.figure(figsize=(10, 6))

    # Normal veriler için histogram
    sns.histplot(normal_values, kde=True, color='skyblue', bins=20, label='Normal Veriler')

    # Aykırı veriler için histogram (kırmızı ile)
    sns.histplot(outliers_iqr, kde=False, color='red', bins=20, label='Aykırı Değerler')

    # Başlık ve etiketler
    plt.title(f'{column} Sütununun Histogramı ve Aykırı Değerler', fontsize=14)
    plt.xlabel(f'{column} Değeri', fontsize=12)
    plt.ylabel('Frekans', fontsize=12)
    plt.legend()
    plt.grid(True)

    # Scatter plot ile aykırı ve normal verileri görselleştirelim
    # Normal verileri mavi, aykırı verileri kırmızı gösterelim
    plt.figure(figsize=(10, 6))

    # Normal veriler
    plt.scatter(normal_values.index, normal_values, color='blue', label='Normal Veriler', s=100)

    # Aykırı veriler
    plt.scatter(outliers_iqr.index, outliers_iqr, color='red', label='Aykırı Değerler (IQR)', s=100)

    # Başlık ve etiketler
    plt.title(f'{column} Sütunundaki Normal ve Aykırı Değerler', fontsize=14)
    plt.xlabel('İndeks', fontsize=12)
    plt.ylabel(f'{column} Değeri', fontsize=12)
    plt.legend()
    plt.grid(True)

    plt.show()


def analys_trend_for_sales_data(sales_data):
    sales_data['tarih'] = pd.to_datetime(sales_data['tarih'],  dayfirst=True,errors='coerce')

    # Haftalık ve Aylık Bazda Toplam Satış Analizi
    # Haftalık bazda toplam satış
    weekly_sales = sales_data.resample('W-Mon', on='tarih').agg({'toplam_satis': 'sum'})
    # Aylık bazda toplam satış
    monthly_sales = sales_data.resample('ME', on='tarih').agg({'toplam_satis': 'sum'})

    # Haftalık ve aylık bazda satış trendlerini görselleştirme
    plt.figure(figsize=(14, 7))

    # Haftalık toplam satış
    plt.subplot(1, 2, 1)
    plt.plot(weekly_sales.index, weekly_sales['toplam_satis'], label='Haftalık Toplam Satış', color='blue')
    plt.title('Haftalık Satış Trendleri')
    plt.xlabel('Tarih')
    plt.ylabel('Toplam Satış')
    plt.grid(True)
    plt.legend()

    # Aylık toplam satış
    plt.subplot(1, 2, 2)
    plt.plot(monthly_sales.index, monthly_sales['toplam_satis'], label='Aylık Toplam Satış', color='blue')
    plt.title('Aylık Satış Trendleri')
    plt.xlabel('Tarih')
    plt.ylabel('Toplam Satış')
    plt.grid(True)
    plt.legend()

    # Grafiklerin gösterimi
    plt.tight_layout()
    plt.show()


def analysis_weekly_sales_data(sales_data):
    # her ayın ilk ve son satış gününne göre analiz
    # 'tarih' sütununu datetime formatına çevirelim
    sales_data['tarih'] = pd.to_datetime(sales_data['tarih'], dayfirst=True,errors='coerce')

    # 1. Her Ayın İlk ve Son Satış Gününü Bulma
    monthly_sales = sales_data.groupby(sales_data['tarih'].dt.to_period('M')).agg(
        first_sale_day=('tarih', 'min'),  # her ayın ilk satış günü
        last_sale_day=('tarih', 'max')  # her ayın son satış günü
    ).reset_index()

    monthly_sales['first_sale_day'] = monthly_sales['first_sale_day'].dt.day
    monthly_sales['last_sale_day'] = monthly_sales['last_sale_day'].dt.day

    #
    # plt.figure(figsize=(10, 6))
    #
    # # İlk satış günleri
    # plt.plot(monthly_sales['tarih'].dt.to_timestamp(), monthly_sales['first_sale_day'], 'o-', label='İlk Satış Günü',
    #          color='blue')
    #
    # # Son satış günleri
    # plt.plot(monthly_sales['tarih'].dt.to_timestamp(), monthly_sales['last_sale_day'], 'o-', label='Son Satış Günü',
    #          color='red')
    #
    # # Başlık ve etiketler
    # plt.title('Her Ayın İlk ve Son Satış Günleri (Gün Numaraları)')
    # plt.xlabel('Ay')
    # plt.ylabel('Gün Numarası')
    # plt.xticks(rotation=45)  # X eksenindeki tarihleri daha kolay okunabilir yapmak için döndürüyoruz
    # plt.grid(True)
    #
    # # Efsane ekleme
    # plt.legend()
    #
    # # Grafik gösterimi
    # plt.tight_layout()
    # plt.show()
    # Hafta sayısına göre toplam satıs grafiği
    # sales_data['tarih'] = pd.to_datetime(sales_data['tarih'], dayfirst=True,errors='coerce')
    # Haftalık satışları hesaplama (Ürün başına toplam satış)
    # weekly_sales = sales_data.resample('W-Mon', on='tarih').agg({'toplam_satis': 'sum'})
    # weekly_sales['hafta'] = range(1, len(weekly_sales) + 1)  # Basit numaralandırma (1, 2, 3, ...)

    # Grafikle Görselleştirme
    # plt.figure(figsize=(10, 6))
    # # Haftalık satış trendini çizme
    # plt.plot(weekly_sales['hafta'], weekly_sales['toplam_satis'], color='blue', label='Haftalık Satışlar')
    # # Başlık ve etiketler
    # plt.title('Haftalık Satış Trendleri')
    # plt.xlabel('Hafta')
    # plt.ylabel('Toplam Satış')
    # plt.xticks(weekly_sales['hafta'][::5], labels=[f'{i}. Hafta' for i in weekly_sales['hafta'][::5]], rotation=45)
    #
    # #plt.xticks(weekly_sales['hafta'], labels=[f'{i}. Hafta' for i in weekly_sales['hafta']], rotation=45)
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()


def trend_monthly_sales_data(sales_data):
    sales_data['tarih'] = pd.to_datetime(sales_data['tarih'], dayfirst=True, errors='coerce')
    monthly_sales = sales_data.resample('M', on='tarih').agg({'toplam_satis': 'sum'})

    # Grafik boyutunu ayarlıyoruz
    plt.figure(figsize=(14, 8))

    # Yıllara göre gruplayıp, her yıl için aylık satışları çiziyoruz
    years = monthly_sales.index.year.unique()
    for year in years:  # Her yıl için bir çizgi çiziyoruz
        year_sales = monthly_sales[monthly_sales.index.year == year]

        # Aylık toplam satışları çiziyoruz
        plt.plot(year_sales.index.month, year_sales['toplam_satis'], label=f'{year}', marker='o')

    # Başlık ve etiketler
    plt.title('Yıllık Aylık Satış Trendleri')
    plt.xlabel('Ay')
    plt.ylabel('Toplam Satış')
    # X eksenini ay olarak etiketliyoruz (1=Ocak , 2=Şubat, ....)
    plt.xticks(np.arange(1, 13), labels=['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                                         'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'])
    plt.grid(True)
    plt.legend()
    # Grafik gösterimi
    plt.tight_layout()
    plt.show()

