#gerekli kütüphaneleri import edelim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def about_csv_files(csv_data):
    #okunan csv dosyası hakkında gerekli bilgileri öğrenelim
    #satır sayısı,sütun sayısı, sütun isimleri ve dosyaya ait ilk 5 satır verisi
    print('Rows count:', csv_data.shape[0])  # Rows count
    print('Columns count:', csv_data.shape[1])  # columns count
    print('Column names:', csv_data.columns.tolist())  # columns names
    print('Csv head: ',csv_data.head())

def analysis_missing_data(csv_data):
    #csv dosyasındaki her bir sütun taranarak eksik veri sayısı döndürülür
    print("Customer Data - Eksik veriler:\n", csv_data.isnull().sum())
    #customer data : eksik veri yok
    #sales data : eksik veri yok

def change_and_fill_data(csv_data,column,file_path):
    #csv dosyasındaki integer olması gereken veriler(fiyat..) integer olarak dönüştürülür.
    #dönüştürülemeyenler NaN olarak doldurulur.
    print('dosyanın ilk 5 değeri: ',csv_data[column].head())
    csv_data[column] = pd.to_numeric(csv_data[column], errors='coerce')
    # NaN olan değerler ortalama değer ile doldurulur
    mean_value = csv_data[column].mean()
    csv_data.loc[:, column] = csv_data[column].fillna(mean_value)  # Eksik değerleri doldurma
    csv_data.to_csv(file_path, index=False)
    print('dosyanın ilk 5 değeri: ', csv_data[column].head())
    print(file_path, 'dosyası için', column, 'sütunu güncellenmiştir.')



def find_outliers_iqr(csv_data,column):
    #seçilen veriseti ve sütun için çeyrekler açıklığına göre aykırı değerler bulunur
    Q1 = csv_data[column].quantile(0.25) #1.çeyrek değeri(25. yüzde)
    Q3 = csv_data[column].quantile(0.75) #3.çeyrek değeri(75. yüzde)
    IQR = Q3 - Q1 #çeyrekler açıklığı
    lower_bound = Q1 - 1.5 * IQR #alt sınır
    upper_bound = Q3 + 1.5 * IQR #üst sınır
    #aykırı değerleri belirleyelim(alt sınırdan düşük ve üst sınırdan yüksek veriler aykırıdır)
    outliers = csv_data[(csv_data[column] < lower_bound) | (csv_data[column] > upper_bound)]
    if not outliers.empty:
        #eğer aykırı değer listesi boş değilse, outliers vardır
        print(f"Aykırı Değerler {column} sütununda tespit edildi:")
        print(outliers)
    else:
        #eğer aykırı değer listesi boşsa outliers yoktur
        print(f"{column} sütununda aykırı değer bulunmadı.")

    #Boxplot ile aykırı değerleri görselleştirme
    #verilerin çeyrekler ortalama etrafında dağıımını görüntüleriz
    #aykırı değer varsa çeyrekler dışında yer alır
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=csv_data[column])
    plt.title(f'{column} Sütununda Aykırı Değerlerin Boxplot Gösterimi', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.grid(True)
    plt.show()

    #Zaman serisi çizgisi ve aykırı değerlerin scatter plot ile görselleştirilmesi
    #dağılım grafiğine göre aykırı değerler kırmızı işaretlenerek verilerden uzaklığı görselleştirilir
    """
    plt.figure(figsize=(12, 6))
    plt.plot(csv_data[column], label=f'{column} Değeri', color='blue', linestyle='-')
    plt.scatter(outliers.index, outliers[column], color='red', label='Aykırı Değerler', s=80, marker='o')
    # Başlık ve etiketler
    plt.title(f'{column} Zaman Serisi ve Aykırı Değerler', fontsize=14)
    plt.xlabel('İndeks', fontsize=12)
    plt.ylabel(f'{column} Değeri', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    """

def find_outliers_z_score(df, column):
    #z skor değerine göre aykırı değerlerin bulunması
    #verinin ortalamadan uzaklığı ve standart sapma hesaplanarak -3/+3 değeri dışındakiler aykırı olarak belirlenir
    #ortalama ve standart sapmanın hesaplanması
    mean = df[column].mean()
    std_dev = df[column].std()
    # Z-skoru hesaplanması
    df['z_score'] = (df[column] - mean) / std_dev
    # Aykırı değerleri tespit etme
    outliers = df[df['z_score'].abs() > 3]
    #print(len(outliers))
    #Z-skoru histogram ile görselleştirme
    #verinin genel dağılımı görselleştirilerek aykırı değerler rahatça görülür
    plt.figure(figsize=(10, 6))
    sns.histplot(df['z_score'], bins=30, kde=True, color='purple')
    plt.axvline(x=3, color='red', linestyle='--', label='Z-skoru Eşiği (3)')
    plt.axvline(x=-3, color='red', linestyle='--', label='Z-skoru Eşiği (-3)')
    plt.title('Z-Skoru Dağılımı ve Aykırı Değerler', fontsize=14)
    plt.xlabel('Z-Skoru', fontsize=12)
    plt.ylabel('Frekans', fontsize=12)
    plt.legend()
    plt.show()

def merge_csv_files(sales_data,customer_data):
    #müşteri id değerine göre iki dosyayı birleştirelim
    merged_data = pd.merge(sales_data, customer_data, on='musteri_id', how='inner')

    print("Birleştirilmiş Veri Seti:")
    print(merged_data)

    #birleştirilen dosyayı kaydedelim
    merged_data.to_csv('merged_data.csv', index=False)
    print("Birleştirilmiş veri 'merged_data.csv' olarak kaydedildi.")



#sales data --> ['tarih', 'ürün_kodu', 'ürün_adi', 'kategori', 'fiyat', 'adet', 'toplam_satis', 'musteri_id']
#customer data --> ['musteri_id', 'isim', 'cinsiyet', 'yas', 'sehir', 'harcama_miktari']

