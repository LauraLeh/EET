import os
import json
import sys
from collections import defaultdict

freq_w_c = defaultdict(lambda: defaultdict(int))  # {class: {word: freq, word: freq, ...}, class: {word: freq, ...}, ...}
freq_c = defaultdict(int)
freq_w = defaultdict(int)

# calculate p(c)
def calc_prob_c():
    prob_class = {cls: freq_c[cls] / sum(freq_c.values()) for cls in freq_c}
    return prob_class

# calculate discount
def calc_discount():
    N1 = sum(1 for c in freq_w_c for count in freq_w_c[c].values() if count == 1)
    N2 = sum(1 for c in freq_w_c for count in freq_w_c[c].values() if count == 2)
    return N1 / (N1 + 2*N2)

# calculate relative frequency
def calc_rel_freq():
    discount = calc_discount()
    for c in freq_c:
        freq_sum = sum(freq_w_c[c].values())  # sum_w' f(w', c)
        for w in freq_w:
            freq_w_c[c][w] = max(0, freq_w_c[c][w] - discount) / freq_sum
    return freq_w_c

# calculate p(w|c)
def calc_prob_w_c():
    r_w_c = calc_rel_freq()
    p_w_c = defaultdict(lambda: defaultdict(float))
    N = sum(freq_w.values())
    for c, d in r_w_c.items():
        backoff = 1 - sum(d.values())
        for w, f in d.items():
            p_w_c[c][w] = f + backoff * (freq_w[w] / N)
    return p_w_c

# establish class names, read training files
# calculate frequency of classes, words, and words given class
def read_data(train_path):
    classes = [dir for dir in os.listdir(train_path) if not dir.startswith(".")] # ignore hidden dirs like ".DS_Store"
    for cls in classes:
        class_dir = os.path.join(train_path, cls)
        for file in os.listdir(class_dir):
            with open(os.path.join(class_dir, file), 'r', encoding="ISO-8859-1") as text:
                freq_c[cls] += 1
                for word in text.read().split():
                    freq_w_c[cls][word] += 1
                    freq_w[word] += 1


if __name__ == "__main__":
    train_path = sys.argv[1]
    read_data(train_path)
    p_c = calc_prob_c()
    p_w_c = calc_prob_w_c()

    with open(sys.argv[2], 'w', encoding="utf-8") as j_file:
        json.dump([p_w_c, p_c], j_file)