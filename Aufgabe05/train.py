import os
import sys
from collections import Counter, defaultdict
import string
import math
import random
import json

train_path = sys.argv[1]
classes = [dir for dir in os.listdir(train_path) if not dir.startswith(".")]
weight_vec = defaultdict(int)

def read_stopwords():
    with open("stopwords.txt") as s:
        return s.read().split()

## Extracts features for the feature vector and builds weight vector
def build_features_and_weight_vec(train_path):
    all_text = []
    stopwords = read_stopwords()
    for path, directories, files in os.walk(train_path):
        for file in files:
            with open(os.path.join(path, file), 'r', encoding="latin-1") as text:
                all_text = text.read().split()
    # The 100 most common words, which aren't stopwords or punctuation, become the features
    filtered_text = [tok for tok in all_text if tok not in string.punctuation and tok not in stopwords]
    most_common = Counter(filtered_text).most_common(100)
    features = [token[0] for token in most_common]

    for cls in classes:
        weight_vec[cls] = [random.random() for _ in features] # initialize weight vector with the length of the features
    return features

# Calculates p(c|d)
def calculate_normalized_probs(cls, file_path, features):
    p_class_mail = defaultdict(int)
    # The document's (non-exponentiated) score of the other class will be 0 anyways.
    # The actual score for the current class is calculated in the following - it won't stay 0.
    for c in classes:
        p_class_mail[c] = math.exp(0)

    with open(file_path, 'r', encoding="ISO-8859-1") as text:
        document = text.read().split()
        # for each feature that occurs in the doc, its value in the feature vec is the feature's count in the doc
        feature_vec = [document.count(feat) for feat in features]
        # dot product between feature vec and weight vec
        score = sum([weight_vec[cls][feat] * feature_vec[feat] for feat in range(len(features))])
        p_class_mail[cls] = math.exp(score)
        # only after the (primary) scores for both classes are known, we can calculate Z and normalize.
        Z = sum(p_class_mail.values())
        for c in classes:
            p_class_mail[c] *= 1/Z

    return p_class_mail, feature_vec


if __name__ == "__main__":
    features = build_features_and_weight_vec(train_path)
    feature_count = len(features)
    epochs = 3
    eta = 0.2
    mu = 0.01

    for _ in range(epochs):
        for cls in classes:
            class_dir = os.path.join(train_path, cls)
            for file in os.listdir(class_dir):
                file_path = os.path.join(class_dir, file)
                # p(class|mail) and observed counts
                p_c_d, observed = calculate_normalized_probs(cls, file_path, features)
                # expected counts
                expected = [p_c_d[cls] * observed[feat] for feat in range(feature_count)]
                gradient = [observed[feat] - expected[feat] for feat in range(feature_count)]
                # update weights with L2 regularization
                for weight in range(len(features)):
                    weight_vec[cls][weight] = weight_vec[cls][weight] * (1-eta*mu) + eta * gradient[weight]


    with open(sys.argv[2], 'w', encoding="utf-8") as paramfile:
        json.dump([weight_vec, features], paramfile)
