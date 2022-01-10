from torchtext.legacy import data
from torchtext.data.utils import get_tokenizer
import torch
from torch import nn, optim


### READING THE DATA ###

tokenizer = get_tokenizer('basic_english')
TEXT = data.Field(sequential=True, tokenize=tokenizer, lower=True)
LABEL = data.LabelField(sequential=False)

train_data, dev_data = data.TabularDataset.splits(
    path='data',
    train = 'sentiment.train.tsv',
    validation = 'sentiment.dev.tsv',
    format='tsv',
    fields=[('label', LABEL), ('text', TEXT)],
)

# take 10000 most frequent words as vocab, the rest is treated as <unk>
# for reference: the initial vocab size is 16517
TEXT.build_vocab(train_data, max_size=10000)
LABEL.build_vocab(train_data)

# create iterators for train/dev datasets
train_it, dev_it = data.BucketIterator.splits(
  (train_data, dev_data),
  sort_key = lambda x: len(x.text),
  sort = True,
  shuffle = True,
  batch_sizes=(32,32)
)

### DEFINING THE MODEL ###

class Classifier(nn.Module):
    def __init__(self, vocab_size, num_classes, embed_size, hidden_size, dropout_rate):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(hidden_size*2, num_classes)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, text):
        embedding = self.dropout(self.embedding(text))
        lstm_output, hidden = self.lstm(embedding)
        lstm_output = self.dropout(lstm_output)
        pooling = torch.amax(lstm_output, dim=0)
        scores = self.linear(self.dropout(pooling))
        return scores

VOCAB_SIZE = len(TEXT.vocab)
NUM_CLASSES = 5
EMBED_SIZE = 350
HIDDEN_SIZE = 64
DROPOUT = 0.3
LEARNING_RATE = 0.02
NUM_EPOCHS = 10

model = Classifier(vocab_size=VOCAB_SIZE, num_classes=NUM_CLASSES,
                   embed_size=EMBED_SIZE, hidden_size=HIDDEN_SIZE, dropout_rate=DROPOUT)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

total_dev_tags = sum(1 for _ in dev_data)
best_accuracy = None


### TRAINING ###

for epoch in range(NUM_EPOCHS):
    # Put model into training mode
    model.train()
    for instance in train_it:
        model.zero_grad()
        input_sentence = instance.text.to(device)
        targets = instance.label.to(device)
        scores = model(input_sentence)
        loss = criterion(scores, targets)
        loss.backward()
        optimizer.step()

    # validation 
    with torch.no_grad():
        model.eval()
        true_positives = 0
        for dev_instance in dev_it:
            input_sentence = dev_instance.text.to(device)
            scores = model(input_sentence)
            correct = dev_instance.label
            predictions = [torch.max(x, 0)[1].item() for x in scores]

            for i in range(len(predictions)):
                if predictions[i] == correct[i]:
                    true_positives += 1

        accuracy = true_positives/total_dev_tags
        print("Validation Accuracy:", accuracy)

        # save model with best accuracy so far
        if best_accuracy is None or best_accuracy < accuracy:
          best_accuracy = accuracy
          torch.save(model.state_dict(), "model.pth")
          print("Saved!")

        true_positives = 0
        model.train()

print("TRAINING FINISHED.")
print("Best Accuracy:", best_accuracy)
