from collections import defaultdict
import json
import sys
import os
import math

# read probabilities from parameter file
def classifyer(text, p_w_c, p_c):
    all_c_prob = defaultdict(float)
    for c, c_prob in p_c.items():
        score = math.log(c_prob)
        for word in text.split():
            if word in p_w_c[c].keys():
                score += math.log(p_w_c[c][word])
        all_c_prob[c] = score
    label = max(all_c_prob, key=all_c_prob.get)
    max_score = max(all_c_prob.values())
    return label, max_score

# read and classifiy one file after another
def test(path):
    pos, neg = 0, 0
    with open(sys.argv[1], "r") as parameter:
        data = json.load(parameter)
        prob_w_c = data[0]  # {class->{word->prob}}
        prob_c = data[1]  #
        # print(prob_w_c, prob_c)
    for root, dirs, files in os.walk(path):
        for file in files:
            gold = None
            with open(os.path.join(root, file), "r", encoding="ISO-8859-1") as auto:
                text = auto.read()
                for c in prob_c.keys():
                    if c in root:
                        gold = c
                label, max_score = classifyer(text, prob_w_c, prob_c)
                if label == gold:
                    pos += 1
                else:
                    neg += 1
                print("Label: ", label, "Gold:", gold, "for file", os.path.join(root, file))
    print("Accuracy:", pos/(pos+neg))

if __name__ == "__main__":
    test(sys.argv[2])
