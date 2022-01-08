from torchtext.legacy import data
from torchtext.data.utils import get_tokenizer
import torch
from torch import nn, optim


tokenizer = get_tokenizer('basic_english')
TEXT = data.Field(sequential=True, tokenize=tokenizer, lower=True)
LABEL = data.Field(sequential=False)

train_data, dev_data = data.TabularDataset.splits(
    path='data',
    train = 'sentiment.train.tsv',
    validation = 'sentiment.dev.tsv',
    format='tsv',
    fields=[('label', LABEL), ('text', TEXT)],
)

TEXT.build_vocab(train_data)
LABEL.build_vocab(train_data)

# create iterators for train/valid datasets
train_it, valid_it = data.BucketIterator.splits(
  (train_data, dev_data),
  sort_key = lambda x: len(x.text),
  sort = True,
  shuffle = True,
  batch_sizes=(32,32)
)

class Classifier(nn.Module):

    def __init__(self, vocab_size, num_classes, embed_size, hidden_size, dropout_rate):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, bidirectional=True,
                            batch_first=True)
        self.pooling = nn.MaxPool2d(2,2)
        self.linear = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(dropout_rate)


    def forward(self, text):
        embedding = self.dropout(self.embedding(text))
        lstm_output, hidden = self.lstm(embedding)
        pooling = self.pooling(lstm_output)
        scores = self.linear(pooling)

        return scores

model = Classifier(vocab_size=len(TEXT.vocab), num_classes=5,
                   embed_size=100, hidden_size=64, dropout_rate=0.1)

numEpochs = 1
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

"""
total_dev_tags = 0
for instance in valid_it:
    for tags in instance.label:
        total_dev_tags += 1
"""

best_accuracy = None

# Training Loop
for epoch in range(numEpochs):
    # Put model into training mode
    model.train()
    for data in train_it:
        model.zero_grad()
        input_sentence = data.text
        targets = data.label

        scores = model(input_sentence)
        print("TARGET")
        print(targets)
        print("SCORES")
        print(scores)

        loss = criterion(scores, targets)
        print(loss)
        break
        loss.backward()
        optimizer.step()

    """
    # validation 
    with torch.no_grad():
        model.eval()
        true_positives = 0
        for valid_data in valid_it:
            input_sentence = valid_data.text
            input_sentence = torch.LongTensor(input_sentence).to(device)
            tag_scores = model(input_sentence)
            correct = valid_data.label
            correct = torch.LongTensor(correct).to(device)

            preds = [torch.max(x, 0)[1].item() for x in tag_scores]

            correct_tags = LABEL.vocab.itos(correct)
            predicted_tags = LABEL.vocab.itos(preds)

            for i in range(len(predicted_tags)):
                if predicted_tags[i] == correct_tags[i]:
                    true_positives += 1

        #accuracy = true_positives/total_dev_tags
        #print("Validation Accuracy:", accuracy)

        #if best_accuracy is None or best_accuracy < accuracy:
         # best_accuracy = accuracy
          #torch.save(model, F"/content/drive/My Drive/rnn.pth")
          #torch.save(model, args.paramfile+".rnn")
          #print("Saved!")

        true_positives = 0
        model.train()
        """
