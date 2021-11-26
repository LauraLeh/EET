import os
from collections import Counter, defaultdict
import string
import math
import random

train_path = "dev"
classes = ["spam", "ham"]
weight_vec = defaultdict(int)

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

    for cls in classes:
        weight_vec[cls] = [random.randrange(-1, 1) for _ in features]
    return features

# calculates p(c|d)
# each p(c|d) should be a prob. distribution, i.e. sum to 1
def calculate_normalized_probs(cls, file_path, features):
    p_class_mail = defaultdict(int)
    # We are looking at a document *given a certain class*.
    # Therefore, the document's (non-exponentiated) score of the other class will be 0 anyways.
    # The actual score for the current class is updated in the following - it won't stay 0.
    for cls in classes:
        p_class_mail[cls] = math.exp(0)

    with open(file_path, 'r', encoding="ISO-8859-1") as t:
        text = t.read()
        document = text.split()
        # for each feature that occurs in the doc, its value in the feature vec is the feature's count in the doc
        feature_vec = [(" ".join([x, cls]), document.count(x)) for x in features]
        # dot product between feature vec and weight vec
        score = sum([weight_vec[cls][i]*feature_vec[i][1] for i in range(len(features))])
        try:
            p_class_mail[cls] = math.exp(score)
        except OverflowError:
            pass
        # only after the scores for both classes (given the doc) are known,
        # we can calculate Z and apply it to the scores.
        Z = sum(p_class_mail.values())
        for cls in classes:
            p_class_mail[cls] *= 1/Z

        return p_class_mail, feature_vec


features = build_feature_and_weight_vec(train_path)
feature_count = len(features)

print(weight_vec)

for _ in range(5):
    for cls in classes:
        class_dir = os.path.join(train_path, cls)
        for file in os.listdir(class_dir):
            file_path = os.path.join(class_dir, file)
            # p(class|mail) and observed feature values
            p_c_d, observed_vec = calculate_normalized_probs(cls, file_path, features)
            # observed counts
            observed = [observed_vec[i][1] for i in range(feature_count)]
            # expected counts
            for cls in classes:
                expected_vec = [p_c_d[cls]*observed_vec[i][1] for i in range(feature_count)]
            expected = [p_c_d[cls]*observed_vec[i][1] for i in range(feature_count)]
            gradient = [observed[i] - expected[i] for i in range(feature_count)]

            for w in range(len(features)):
                weight_vec[cls][w] = weight_vec[cls][w] + 0.01 * gradient[w]

    print(weight_vec)
