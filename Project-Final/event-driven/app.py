from flask import Flask, request, render_template
import joblib

# Flask uygulamasını başlat
app = Flask(__name__)

# Önceden eğitilmiş modeli ve vectorizer'ı yükle
model = joblib.load('svc_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kullanıcıdan gelen yorum
        user_review = request.form.get('review')

        # Metin verisini işleme ve model tarafından sınıflandırma
        review_vector = vectorizer.transform([user_review])
        prediction = model.predict(review_vector)[0]

        # Sonucu ekrana yazdırma
        if prediction == 1.0:
            result = 'Olumlu'
        elif prediction == -1.0:
            result = 'Olumsuz'
        else:
            result = 'Nötr'

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
