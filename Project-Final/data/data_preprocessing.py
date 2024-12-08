import pandas as pd

#load dataset
data = pd.read_csv('dataset.csv')

#classify reviews according to rating value
def classify_rating(rating):
    if rating >= 7:
        return 1  # Positive review
    elif rating >= 4:
        return 0  # Neutral review
    else:
        return -1  # Negative review

#apply rating value for class
data['class'] = data['rating'].apply(classify_rating)

# save new file
output_file = 'dataset_with_class.csv'
data.to_csv(output_file, index=False)
print(f"Yeni veri seti '{output_file}' adıyla kaydedildi.")