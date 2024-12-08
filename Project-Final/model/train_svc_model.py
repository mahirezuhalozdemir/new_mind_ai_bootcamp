from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# Veriyi yükle
import pandas as pd
data = pd.read_csv('updated_dataset2.csv')

# Özellik ve etiketleri ayır
X = data['review']
y = data['class']

# TF-IDF kullanarak kelime frekanslarını çıkar
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))  # max_features ile en sık kullanılan 5000 kelimeyi alabilirsiniz
X = vectorizer.fit_transform(X)

# Eğitim ve test veri setini ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVC(random_state=42)

model.fit(X_train, y_train)
# Test setinde tahmin yap
y_pred = model.predict(X_test)

# Sonuçları değerlendirme
print(classification_report(y_test, y_pred))
accuracy = accuracy_score(y_test, y_pred)
print(f"Total Accuracy: {accuracy:.4f}")