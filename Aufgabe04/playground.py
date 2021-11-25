import os
import json
import sys
from collections import defaultdict

def calc_prob_c(f_c): # calculate class probability
    prob_class = defaultdict(float)
    for c, f in f_c.items():
        prob_class[c] = f/sum(f_c.values())
    return prob_class

def calc_discount(f_w_c): # claculate discount
    N1 = sum(1 for c in f_w_c for count in f_w_c[c].values() if count == 1)
    N2 = sum(1 for c in f_w_c for count in f_w_c[c].values() if count == 2)
    return N1/(N1 + 2*N2)

def calc_rel_freq(f_w_c, f_w): # calculate relative Hufigkeit
    discount = calc_discount(f_w_c)
    for c, d in f_w_c.items():
        freq_sum = sum(d.values())
        for w in f_w.keys():
            f_w_c[c][w] = max(0, f_w_c[c][w] - discount) / freq_sum
    return f_w_c

def calc_prob_w_c(r_w_c, f_w): # calculate p(w|c)
    p_w_c = defaultdict()
    N = sum(f_w.values())
    for c, d in r_w_c.items():
        backoff = 1-sum(d.values())
        p_w_c[c] = defaultdict(float)
        for w, f in d.items():
            p_w_c[c][w] = f + backoff * (f_w[w] / N)
    return p_w_c

def train(path): # read all files, calculate frequency of classes, calculate frequency of words given class
    freq_w_c = defaultdict()  # {class:{word:freq, word:freq, word:freq, ...}, class:{word:freq, ...}, ...}
    freq_c = defaultdict()
    freq_w = defaultdict(int)
    for root, dirs, files in os.walk(path):
        for c in dirs:
            freq_w_c[c] = defaultdict(int)
            freq_c[c] = 0
        for file in files:
            with open(os.path.join(root, file), "r", encoding="ISO-8859-1") as auto:
                for c in freq_w_c.keys():
                    if c in root:
                        text = auto.read()
                        freq_c[c] += 1
                        for word in text.split():
                            freq_w_c[c][word] += 1
                            freq_w[word] += 1
    p_c = calc_prob_c(freq_c)
    r_w_c = calc_rel_freq(freq_w_c, freq_w)
    p_w_c = calc_prob_w_c(r_w_c, freq_w)
    return p_w_c, p_c


if __name__ == "__main__":
    path = sys.argv[1]
    prob_w_c, prob_c = train(path)
    with open(sys.argv[2], 'w', encoding="utf-8") as j_file:
        json.dump([prob_w_c, prob_c], j_file)