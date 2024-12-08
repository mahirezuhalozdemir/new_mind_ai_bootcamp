import pandas as pd
import matplotlib.pyplot as plt
# Veri kümesini yükleyin
data = pd.read_csv('updated_dataset.csv')

# Etiket sütununu seçin
y = data['class']

# Sınıf değerlerini say
class_counts = y.value_counts()

# Daire grafiği oluştur
plt.figure(figsize=(8, 6))
class_counts.plot.pie(autopct='%1.1f%%', labels=['Positive', 'Neutral', 'Negative'], colors=['lightblue', 'orange', 'lightgreen'])
plt.title('Class Distribution')
plt.ylabel('')  # Y eksenini kaldırmak için
plt.show()
