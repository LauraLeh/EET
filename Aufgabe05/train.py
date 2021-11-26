import os
from collections import Counter, defaultdict
import string
import math

train_path = "dev"
classes = [dir for dir in os.listdir(train_path) if not dir.startswith(".")]  # ignore hidden dirs like ".DS_Store"
p_class_mail = defaultdict(lambda: defaultdict(int))


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
        weights[cls] = [1 for _ in features]
    return features, weights

# calculates p(c|d) without normalization
def calculate_non_normalized_probs(features):
    for cls in ['ham']:
        class_dir = os.path.join(train_path, cls)
        for file in os.listdir(class_dir):
            with open(os.path.join(class_dir, file), 'r', encoding="ISO-8859-1") as t:
                text = t.read()
                tokens = text.split()
                feature_vec = [(" ".join([x, cls]), tokens.count(x)) for x in features]
                score = sum([weight_vec[cls][i]*feature_vec[i][1] for i in range(len(features))])
                p_class_mail[cls][file] = math.exp(score)

# calculate p(c|d) with 1/Z factor
def calculate_normalized_probs():
    Z = sum(score for cls in p_class_mail for score in p_class_mail[cls].values())
    for cls in classes:
        for file in p_class_mail[cls]:
            p_class_mail[cls][file] *= 1/Z


features, weight_vec = build_feature_and_weight_vec(train_path)
calculate_non_normalized_probs(features)
calculate_normalized_probs()
print(p_class_mail)

