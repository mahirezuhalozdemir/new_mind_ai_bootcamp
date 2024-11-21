#gerekli kütüphaneleri import edelim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def category_sales_analysis(sales_data):
    # Kategorilere göre toplam satışları hesaplama
    category_sales = sales_data.groupby('kategori')['toplam_satis'].sum()

    # Toplam satış miktarını hesaplıyoruz
    total_sales = sales_data['toplam_satis'].sum()

    # Her kategorinin tüm satışlar içindeki oranını hesaplıyoruz
    category_sales_percentage = (category_sales / total_sales) * 100

    # Sonuçları birleştiriyoruz
    sales_summary = pd.DataFrame({
        'Toplam Satış': category_sales,
        'Oran (%)': category_sales_percentage
    })

    # Kategorilere göre sıralama yapıyoruz
    sales_summary = sales_summary.sort_values(by='Toplam Satış', ascending=False)

    print(sales_summary)

    plt.figure(figsize=(10, 6))
    # Bar grafiği çiziyoruz
    category_sales.sort_values().plot(kind='barh', color='blue')
    # Başlık ve etiketler
    plt.title('Ürün Kategorilerine Göre Toplam Satış')
    plt.xlabel('Toplam Satış')
    plt.ylabel('Kategori')

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()

    # labels = category_sales_percentage.index
    # sizes = category_sales_percentage.values
    # colors = plt.cm.Paired(range(len(labels)))  # Farklı renkler
    #
    # # Pasta grafiğini çiziyoruz
    # plt.figure(figsize=(8, 8))
    # plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
    #
    # # Başlık ekliyoruz
    # plt.title('Ürün Kategorilerine Göre Satış Oranları')
    #
    # # Grafiği gösteriyoruz
    # plt.tight_layout()
    # plt.show()


def analyze_sales_by_age_group(merged_data):
    # Yaş gruplarını tanımlıyoruz
    bins = [0, 24, 34, 44, 54, float('inf')]  # 0-25, 26-35, 36-50, 50+
    labels = ['18-24', '25-34', '35-44', '45-54', '55+']

    # Yaş gruplarını 'yas' sütununa göre belirliyoruz
    merged_data['age_group'] = pd.cut(merged_data['yas'], bins=bins, labels=labels, right=False)

    # Yaş gruplarına göre toplam satışları hesaplıyoruz
    age_group_sales = merged_data.groupby('age_group')['toplam_satis'].sum()

    # Satışları görselleştiriyoruz
    plt.figure(figsize=(8, 6))
    age_group_sales.plot(kind='bar', color='blue', edgecolor='black')

    # Başlık ve etiketler
    plt.title('Yaş Gruplarına Göre Toplam Satışlar')
    plt.xlabel('Yaş Grupları')
    plt.ylabel('Toplam Satış')
    plt.xticks(rotation=0)
    plt.grid(True, axis='y')

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()


def analyze_category_by_age_group(merged_data):
    # Yaş gruplarını tanımlıyoruz
    bins = [0, 24, 34, 44, 54, float('inf')]  # 0-24, 25-34, 35-44, 45-54, 55+
    labels = ['18-24', '25-34', '35-44', '45-54', '55+']

    # Yaş gruplarını ekliyoruz
    merged_data['age_group'] = pd.cut(merged_data['yas'], bins=bins, labels=labels, right=False)

    # Yaş gruplarına ve kategorilere göre toplam satışları hesaplıyoruz
    age_category_sales = merged_data.groupby(['age_group', 'kategori'])['toplam_satis'].sum().unstack()

    """
    # Satışları görselleştiriyoruz
    age_category_sales.plot(kind='bar', stacked=True, figsize=(10, 7), colormap='viridis') 
    # Başlık ve etiketler
    plt.title('Yaş Gruplarına Göre Satış Kategorileri')
    plt.xlabel('Yaş Grupları')
    plt.ylabel('Toplam Satış')
    plt.xticks(rotation=0)
    plt.legend(title='Kategoriler', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    # Grafik gösterimi
    plt.show()
    """
    age_category_sales.plot(kind='bar', figsize=(10, 7), colormap='viridis')
    plt.title('Yaş Gruplarına Göre Satış Kategorileri')
    plt.xlabel('Yaş Grupları')
    plt.ylabel('Toplam Satış')
    plt.xticks(rotation=0)
    plt.legend(title='Kategoriler', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Grafik gösterimi
    plt.show()


def analyze_for_gender(merged_data):
    gender_sales = merged_data.groupby('cinsiyet')['harcama_miktari'].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.bar(gender_sales['cinsiyet'], gender_sales['harcama_miktari'], color=['blue', 'pink'])
    plt.title('Kadın ve Erkek Müşterilerin Toplam Harcama Miktarları')
    plt.xlabel('Cinsiyet')
    plt.ylabel('Toplam Harcama')
    plt.show()
    #
    # merged_data['tarih'] = pd.to_datetime(merged_data['tarih'], dayfirst=True,errors='coerce')
    # # Aylık ve Cinsiyete Göre Satır Sayısı
    # monthly_gender_count = merged_data.groupby([pd.Grouper(key='tarih', freq='M'), 'cinsiyet']).size().reset_index(
    #     name='count')
    #
    # # Ay ve yıl bilgisini içeren yeni bir sütun oluşturma (örneğin: '2022-12')
    # monthly_gender_count['ay_yil'] = monthly_gender_count['tarih'].dt.strftime('%Y-%m')
    #
    # # Grafik oluşturma
    # plt.figure(figsize=(12, 6))

    # bar_width = 0.35
    # # X eksenindeki her bir ay için pozisyonları belirliyoruz
    # positions = range(len(monthly_gender_count['ay_yil'].unique()))
    #
    # # Kadın ve Erkek için barları çizeceğiz
    # for i, gender in enumerate(monthly_gender_count['cinsiyet'].unique()):
    #     gender_data = monthly_gender_count[monthly_gender_count['cinsiyet'] == gender]
    #     # Kadın ve Erkek barlarını yanyana yerleştiriyoruz
    #     plt.bar([p + i * bar_width for p in positions], gender_data['count'], width=bar_width, label=gender)
    #
    # # Başlık ve etiketler
    #
    # plt.title('Aylık Kadın ve Erkek Kullanıcı Satış Sayısı')
    # plt.xlabel('Ay-Yıl')
    # plt.ylabel('Satış Sayısı')
    # plt.xticks([p + bar_width for p in positions], monthly_gender_count['ay_yil'].unique(),
    #            rotation=45)  # X eksenindeki etiketler
    # plt.grid(True)
    # plt.legend()
    # # Grafik gösterimi
    # plt.tight_layout()
    # plt.show()
    #
    #
    # women_data = monthly_gender_count[monthly_gender_count['cinsiyet'] == 'Kadın']
    # men_data = monthly_gender_count[monthly_gender_count['cinsiyet'] == 'Erkek']
    # plt.plot(women_data['ay_yil'], women_data['count'], marker='o', label='Kadın', color='blue')
    # plt.plot(men_data['ay_yil'], men_data['count'], marker='o', label='Erkek', color='green')
    # plt.title('Aylık Kadın ve Erkek Satış Sayısı')
    # plt.xlabel('Ay-Yıl')
    # plt.ylabel('Satış Sayısı')
    # plt.xticks(rotation=45)  # X eksenindeki etiketler için dönüş
    # plt.grid(True)
    # # Efsane ekleme
    # plt.legend()
    # # Grafik gösterimi
    # plt.tight_layout()
    # plt.show()


def gender_analyze_category(merged_data):
    merged_data['tarih'] = pd.to_datetime(merged_data['tarih'], dayfirst=True, errors='coerce')

    # Cinsiyet ve kategori bazında toplam satışları hesaplama
    gender_category_sales = merged_data.groupby(['cinsiyet', 'kategori']).agg({'toplam_satis': 'sum'}).reset_index()

    # Cinsiyet ve kategori bazında satışları pivot yaparak daha kolay görselleştirme
    gender_category_sales_pivot = gender_category_sales.pivot(index='kategori', columns='cinsiyet',
                                                              values='toplam_satis')

    # Grafik oluşturma
    plt.figure(figsize=(12, 6))

    # Yan yana barlar (bar plot)
    gender_category_sales_pivot.plot(kind='bar', stacked=False, ax=plt.gca())

    # Başlık ve etiketler
    plt.title('Kadın ve Erkek Müşterilerin Kategorilere Göre Satış Dağılımı')
    plt.xlabel('Kategori')
    plt.ylabel('Toplam Satış')
    plt.xticks(rotation=45)  # X eksenindeki etiketler için dönüş
    plt.grid(True)

    # Efsane ekleme
    plt.legend(title='Cinsiyet')

    # Grafik gösterimi
    plt.tight_layout()
    plt.show()