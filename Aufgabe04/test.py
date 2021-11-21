from collections import defaultdict
import json
import sys
import os
import math

# read probabilities from parameter file
def classify(text, p_w_c, p_c):
    all_c_prob = defaultdict(float)
    words = text.split()
    for c, c_prob in p_c.items():
        score = math.log(c_prob) + sum(math.log(p_w_c[c][word]) for word in words if word in p_w_c[c])
        all_c_prob[c] = score
    label = max(all_c_prob, key=all_c_prob.get)
    return label

# read and classify one file after another.
# IMPORTANT: no need to pass subdirectories like "test/spam".
# Just "test" is enough - code iterates through the subdirectories itself.
def test(path):
    pos, neg = 0, 0
    with open(sys.argv[1], "r") as parameter:
        data = json.load(parameter)
        prob_w_c, prob_c = data[0], data[1]  # {class->{word->prob}}, {class->freq}

    classes = [dir for dir in os.listdir(path) if not dir.startswith(".")]
    for cls in classes:
        gold = cls
        class_dir = os.path.join(path, cls)
        for file in os.listdir(class_dir):
            file_path = os.path.join(class_dir, file)
            with open(file_path, 'r', encoding="ISO-8859-1") as text:
                text = text.read()
                label = classify(text, prob_w_c, prob_c)
                if label == gold:
                    pos += 1
                else:
                    neg += 1
                print("Label:", label, "Gold:", gold, "for file", file_path)
    print("Accuracy:", pos/(pos+neg))


if __name__ == "__main__":
    test(sys.argv[2])
