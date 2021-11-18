import os
import json
import sys
from collections import defaultdict

word_class_freq = defaultdict() #{class:{word:freq, word:freq, word:freq, ...}, class:{word:freq, ...}, ...}
class_freq = defaultdict()
word_freq = defaultdict(int)


# read all files
# calculate frequency of classes
# calculate frequency of words given class
path = './Laura_test' # noch ndern!!
for root, dirs, files in os.walk(path):
    for c in dirs:
        word_class_freq[c] = defaultdict(int)
        class_freq[c] = 0
    for file in files:
        with open(os.path.join(root, file), "r") as auto: #, encoding="ISO-8859-1"
            for c in word_class_freq.keys():
                if c in os.path.join(root, file):
                    text = auto.read()
                    class_freq[c] += 1
                    for word in text.split():
                        word_class_freq[c][word] += 1
                        word_freq[word] += 1

# calculate class probability
prob_class = defaultdict(float)
for c, f in class_freq.items():
    prob_class[c] = f/sum(class_freq.values())

# claculate discount
N1, N2 = 0, 0
for d in word_class_freq.values():
    for f in d.values():
        if f == 1:
            N1 += 1
        elif f == 2:
            N2 += 1
discount = N1/(N1 + 2*N2)

# calculate relative Hufigkeit
for c, d in word_class_freq.items():
    freq_sum = sum(d.values())
    for w in word_freq.keys():
        word_class_freq[c][w] = max(0, word_class_freq[c][w] - discount) / freq_sum

# calculate p(w|c)
prob_word_class = defaultdict()
N = sum(word_freq.values())
for c, d in word_class_freq.items():
    backoff = 1-sum(d.values())
    prob_word_class[c] = defaultdict(float)
    for w, f in d.items():
        prob_word_class[c][w] = f + backoff * ( word_freq[w] / N )


with open(path+"/paramfile", 'w') as j_file:
    json.dump(prob_word_class, j_file)
    json.dump(prob_class, j_file)


print("word_freq: ", word_class_freq)
print("class_freq: ", class_freq)
print("discount: ", discount)
print("prob_word_class: ", prob_word_class)