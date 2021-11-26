import os
from collections import Counter, defaultdict
import string
import math
import random

train_path = "dev"
classes = ["ham", "spam"]

## Extract features for the feature vector and build weight vector
def build_feature_and_weight_vec(train_path):
    all_text = []
    for path, directories, files in os.walk(train_path):
        for file in files:
            with open(os.path.join(path, file), 'r', encoding="latin-1") as text:
                text = text.read()
                all_text += text.split()
    all_text = [tok for tok in all_text if tok not in string.punctuation]
    c = Counter(all_text)
    # from the 100 most common words, skip the first 50 (because meaningless)
    # and use the rest as features
    most_common = c.most_common(100)[-50:]
    features = [token[0] for token in most_common]
    weights = defaultdict(int)
    for cls in classes:
        weights[cls] = [random.randrange(-3, 3) for _ in features]
    return features, weights

# calculates p(c|d)
# each p(c|d) should be a prob. distribution, i.e. sum to 1
def calculate_normalized_probs(cls, file_path, features):
    p_class_mail = defaultdict(int)
    if cls == "ham":
        p_class_mail["spam"] = math.exp(0)
    elif cls == "spam":
        p_class_mail["ham"] = math.exp(0)

    with open(file_path, 'r', encoding="ISO-8859-1") as t:
        text = t.read()
        document = text.split()
        feature_vec = [(" ".join([x, cls]), document.count(x)) for x in features]
        score = sum([weight_vec[cls][i]*feature_vec[i][1] for i in range(len(features))])
        p_class_mail[cls] = math.exp(score)
        Z = sum(p_class_mail.values())

        p_class_mail[cls] = math.exp(score)
        for cls in classes:
            p_class_mail[cls] *= 1/Z

        print(p_class_mail)


features, weight_vec = build_feature_and_weight_vec(train_path)
for cls in classes:
    class_dir = os.path.join(train_path, cls)
    for file in os.listdir(class_dir):
        file_path = os.path.join(class_dir, file)
        calculate_normalized_probs(cls, file_path, features)

