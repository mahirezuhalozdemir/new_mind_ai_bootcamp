# dosyalardan ilgili fonksiyonlar import edilir
from data_manipulation import about_csv_files, analysis_missing_data, find_outliers_iqr, find_outliers_z_score, \
    merge_csv_files, change_and_fill_data

from time_series_analysis import analys_trend_for_sales_data, analysis_weekly_sales_data, trend_monthly_sales_data,\
convert_to_numeric_and_save, plot_histogram_with_outliers, replace_outliers_with_mean

from categorical_quantitative_analysis import category_sales_analysis,analyze_sales_by_age_group, analyze_category_by_age_group,\
analyze_for_gender, gender_analyze_category

from advanced_data_manipulation import city_spending, mean_sales_data, mean_category

from extra_anaylses import cohort_analyese, pareto_anaylse, regression_model

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#csv dosyalarını okuyalım
sales_data = pd.read_csv('data/satis_verisi_5000.csv')
#5000 data, 8 feature, Column names: ['tarih', 'ürün_kodu', 'ürün_adi', 'kategori', 'fiyat', 'adet', 'toplam_satis', 'musteri_id']
customer_data = pd.read_csv('data/musteri_verisi_5000.csv')
#5000 data,6 feature, ['musteri_id', 'isim', 'cinsiyet', 'yas', 'sehir', 'harcama_miktari']


def main():
    # print("\n--- CSV Dosyalarının Genel Bilgileri ---")
    # about_csv_files(sales_data)
    # about_csv_files(customer_data)

    # print("\n--- Eksik Verilerin Analizi ---")
    # analysis_missing_data(customer_data)
    # analysis_missing_data(sales_data)

    # print("\n--- Farklı Değerlerin Tespiti ---")
    # change_and_fill_data(sales_data,'fiyat','data/satis_verisi_5000.csv')
    # change_and_fill_data(customer_data,'harcama_miktari','data/musteri_verisi_5000.csv')

    # print("\n--- Aykırı Değerlerin Tespiti (IQR Yöntemi) ---")
    # find_outliers_iqr(customer_data, 'harcama_miktari')
    # find_outliers_iqr(sales_data, 'fiyat')

    # print("\n--- Aykırı Değerlerin Tespiti (Z-Score Yöntemi) ---")
    # find_outliers_z_score(customer_data, 'harcama_miktari')
    # find_outliers_z_score(sales_data, 'fiyat')

    # print("\n--- Veri Setlerinin Birleştirilmesi ---")
    # merge_csv_files(sales_data,customer_data)

    # Birleştirilmiş veriyi tekrar oku
    merged_data = pd.read_csv('data/merged_data.csv')
    # print("Birleştirilmiş veri:\n", merged_data.head())

    # print("\n--- Satış Veriseti Trend Analizi ---")
    #Toplam satış verilerini nümerik değere dönüştürmek için
    # convert_to_numeric_and_save(sales_data,'toplam_satis','data/satis_verisi_5000.csv')

    #aykırı ve normal verileri görselleşitrmek için
    # plot_histogram_with_outliers(sales_data,'toplam_satis')

    #aykırı değerler ortalama değer ile değiştirilir
    # replace_outliers_with_mean(sales_data,'toplam_satis','data/satis_verisi_5000.csv')

    #toplam satış verisi üzerinden trend analizi
    # analys_trend_for_sales_data(sales_data)

    # ayın ilk ve son satış günü için
    # analysis_weekly_sales_data(sales_data)

    # her yılın aynı aylarındaki satış miktarı
    # trend_monthly_sales_data(sales_data)

    # kategorilere göre toplam satış miktarı ve oranı
    # category_sales_analysis(sales_data)

    # yaşa göre kullanıcı analizi
    # analyze_sales_by_age_group(merged_data)

    # yaşlara göre en çok tercih edilen kategroiler
    # analyze_category_by_age_group(merged_data)

    # cinsiyete göre satış analizi
    # analyze_for_gender(merged_data)

    # cinsiyete göre kategori satış analizi
    # gender_analyze_category(merged_data)

    # şehir bazında harcama miktarları
    # city_spending(merged_data)

    # ortalama satış oranı
    # mean_sales_data(merged_data)

    # kategorilere göre aylık toplam satış
    # mean_category(merged_data)

    # Pareto analizi
    # pareto_anaylse(merged_data)

    # Cohort analizi
    # cohort_analyese(merged_data)

    # Regresyon Modeli
    # regression_model(merged_data)

if __name__ == "__main__":
    main()
