from collections import defaultdict, Counter
import json
import sys
import os


def classify(document):
    all_c_prob = defaultdict(float)
    feature_vec = [document.count(feat) for feat in features] # build the feature vec for current document
    for cls in classes:
        # for each class compute the dot product between the feature and weight vec
        score = sum([weights[cls][feat] * feature_vec[feat] for feat in range(len(features))])
        all_c_prob[cls] = score
    label = max(all_c_prob, key=all_c_prob.get) # the class with the highest score is returned
    return label

def test(path):
    pos, neg = 0, 0
    for cls in classes:
        gold = cls
        class_dir = os.path.join(path, cls)
        for file in os.listdir(class_dir):
            with open(os.path.join(class_dir, file), 'r', encoding="ISO-8859-1") as text:
                text = text.read().split()
                label = classify(text)
                if label == gold:
                    pos += 1
                else:
                    neg += 1
                print(f"Label: {label} Gold:{gold} for file {file}")
    print(f"Accuracy:{pos / (pos + neg)}")


if __name__ == "__main__":
    param_file = sys.argv[1]
    test_path = sys.argv[2]

    classes = [dir for dir in os.listdir(test_path) if not dir.startswith(".")]
    with open(param_file, "r") as parameter:
        weights, features = json.load(parameter)

    test(test_path)