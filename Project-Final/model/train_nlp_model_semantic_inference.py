import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import torch
from tqdm import tqdm

# Veriyi pandas DataFrame'den al
data = pd.read_csv("updated_dataset.csv")

# X (yorum metinleri) ve y (etiketler) oluşturma
X = data['review']
y = data['condition'].map({'birth control': 0, 'anxiety': 1, 'depression': 2, 'acne': 3, 'pain': 4})

# Eğitim ve test verilerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tokenizer ve model yükleme
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)

# Veriyi tokenize etme
train_encodings = tokenizer(list(X_train), padding=True, truncation=True, return_tensors="pt", max_length=512)
test_encodings = tokenizer(list(X_test), padding=True, truncation=True, return_tensors="pt", max_length=512)

# Tensor dataset oluşturma
train_dataset = TensorDataset(
    train_encodings['input_ids'],
    train_encodings['attention_mask'],
    torch.tensor(y_train.tolist())
)
test_dataset = TensorDataset(
    test_encodings['input_ids'],
    test_encodings['attention_mask'],
    torch.tensor(y_test.tolist())
)

# DataLoader'ları oluşturma
train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=8, shuffle=False)

#Modeli eğitmek için optimizasyon ayarları
optimizer = AdamW(model.parameters(), lr=2e-5)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Eğitim için epoch sayısı
epochs = 3
#eğitim döngüsü
for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch in tqdm(train_dataloader, desc=f"Epoch {epoch + 1}/{epochs}"):
        input_ids = batch[0].to(device)
        attention_mask = batch[1].to(device)
        labels = batch[2].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        optimizer.step()

    avg_train_loss = total_loss / len(train_dataloader)
    print(f"Epoch {epoch + 1} - Training loss: {avg_train_loss}")

model.eval()

predictions = []
true_labels = []

for batch in tqdm(test_dataloader, desc="Evaluating"):
    input_ids = batch[0].to(device)
    attention_mask = batch[1].to(device)
    labels = batch[2].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    logits = outputs.logits
    preds = torch.argmax(logits, dim=-1)
    predictions.extend(preds.cpu().numpy())
    true_labels.extend(labels.cpu().numpy())
print(classification_report(true_labels, predictions))
