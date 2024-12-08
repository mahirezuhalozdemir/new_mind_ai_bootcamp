import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import resample

def get_condition_info():
    # Rating ve condition bazında gruplama yap
    positive_condition = data[data['class'] == 1]['condition'].value_counts()
    neutral_condition = data[data['class'] == 0]['condition'].value_counts()
    negative_condition = data[data['class'] == -1]['condition'].value_counts()

    # Dağılımı yazdır
    print("Positive Class Condition Distribution:")
    print(positive_condition.head())

    print("\nNeutral Class Condition Distribution:")
    print(neutral_condition.head())

    print("\nNegative Class Condition Distribution:")
    print(negative_condition.head())

def visualise_condition_distrubution():
    # Pozitif sınıf için condition dağılımı
    positive_condition = data[data['class'] == 1]['condition'].value_counts()
    positive_condition = positive_condition.head(8)  # En fazla görülen 5 condition
    positive_condition.plot(kind='bar', title="Positive Class Condition Distribution", figsize=(12, 8),
                            color='lightblue')
    plt.ylabel("Count")
    plt.xticks(rotation=0, ha='center')  # X ekseni etiketlerini döndür
    plt.show()

    # Nötr sınıf için condition dağılımı
    neutral_condition = data[data['class'] == 0]['condition'].value_counts()
    neutral_condition = neutral_condition.head(8)  # En fazla görülen 5 condition
    neutral_condition.plot(kind='bar', title="Neutral Class Condition Distribution", figsize=(12, 8), color='lightblue')
    plt.ylabel("Count")
    plt.xticks(rotation=0, ha='center')  # X ekseni etiketlerini döndür
    plt.show()

    # Negatif sınıf için condition dağılımı
    negative_condition = data[data['class'] == -1]['condition'].value_counts()
    negative_condition = negative_condition.head(8)  # En fazla görülen 10 condition
    negative_condition.plot(kind='bar', title="Negative Class Condition Distribution", figsize=(12, 8),
                            color='lightblue')
    plt.ylabel("Count")
    plt.xticks(rotation=0, ha='center')  # X ekseni etiketlerini döndür
    plt.show()

    # Pozitif sınıf için ilk 10 condition ve sayıları
    print("Positive Class Top 10 Conditions:")
    print(positive_condition)

    # Nötr sınıf için ilk 10 condition ve sayıları
    print("\nNeutral Class Top 10 Conditions:")
    print(neutral_condition)

    # Negatif sınıf için ilk 10 condition ve sayıları
    print("\nNegative Class Top 10 Conditions:")
    print(negative_condition)


def filter_conditions(data, top_conditions, output_file):
    """
    Verilen veri kümesinden yalnızca belirlenen top_conditions'ı içeren satırları filtreler
    ve sonucu yeni bir dosyaya kaydeder.

    Args:
        data (pd.DataFrame): Veri kümesi.
        top_conditions (list): Tutulacak condition'ların listesi.
        output_file (str): Kaydedilecek dosya adı.
    """
    # Veriyi filtrele
    filtered_data = data[data['condition'].isin(top_conditions)]

    # Yeni veri setini kaydet
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtrelenmiş veri başarıyla '{output_file}' dosyasına kaydedildi.")

    # Filtrelenmiş condition dağılımını yazdır
    print("Condition Dağılımı:")
    print(filtered_data['condition'].value_counts())


def reduce_condition(data, condition_name, target_fraction=0.5):
    # Belirtilen condition'a ait pozitif sınıfı filtrele
    condition_data = data[(data['condition'] == condition_name) & (data['class'] == 1)]

    # Hedef veri sayısını hesapla
    target_size = int(len(condition_data) * target_fraction)

    # Condition için rastgele örnek seç
    reduced_condition_data = resample(condition_data, replace=False, n_samples=target_size, random_state=42)

    # Silinen condition dışındaki verileri koru
    other_data = data[~((data['condition'] == condition_name) & (data['class'] == 1))]

    # Güncellenmiş veri setini birleştir
    updated_data = pd.concat([other_data, reduced_condition_data])
    return updated_data


# Veri kümesini yükle
data = pd.read_csv('updated_dataset.csv')
# top_conditions = ["birth control", "depression", "acne", "anxiety", "pain"]
# filter_conditions(data, top_conditions, 'filtered_dataset.csv')


#pozitif sınıftan veri azaltmak
# "Birth Control" condition değerini yarıya düşür
# updated_data = reduce_condition(data, condition_name="pain", target_fraction=0.5)
# # Yeni veri setini kaydet
# updated_data.to_csv('updated_dataset.csv', index=False)


visualise_condition_distrubution()