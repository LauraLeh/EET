from collections import defaultdict
import itertools
import math

weights = defaultdict(float)  # weight vector


def read_data():
    global tagset
    tagset = {"<s>", "<\s>"}   # all available tags
    tags = ["<s>"]             # a sentence's tags (with the start-tag)
    words = ["<s>"]            # a sentence's words (with the start-token)
    sentences = []             # list of sentences

    with open("Tiger/develop.txt") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                # add end-token and end-tag
                words.append("<\s>")
                tags.append("<\s>")
                sentences.append((words, tags))
                words, tags = ["<s>"], ["<s>"]
            else:
                word, tag = line.split()
                words.append(word)
                tags.append(tag)
                tagset.add(tag)
    return sentences


def get_substrings(string):
  string = " " + string + " "
  min_range, max_range = 3, 6
  substrings = [string[min: min+max] for min in range(len(string) - min_range) for max in range(min_range, max_range+1)]
  return substrings


def get_word_shape(string):
    shape = ""
    for x in string:
        if x.isupper():
            shape = shape + "X"
        elif x.islower():
            shape = shape + "x"
        elif x.isdigit():
            shape = shape + "0"
        else:
            shape = shape + x
    return ''.join(x for x, _ in itertools.groupby(shape))


def get_features(word, tag, prev_tag):
    features = []
    features.append("TT-" + prev_tag + "-" + tag) # context feature: prev_tag + tag
    features.append("TWT-" + prev_tag + "-" + word + "-" + tag) # context feature: prev_tag + word + tag
    features.append("TW-" + tag + "-" + word) # lexical feature: tag + word
    features.append("TSH-" + tag + "-" + get_word_shape(word))  # lexical feature: tag + shape
    for substring in get_substrings(word):
        features.append('TSUB-' + tag + "-" + substring)  # lexical feature: tag + substring (all substrings of the word)
    return features


def log_sum_exp(x1, x2):
    a = max(x1, x2)
    b = min(x1, x2)
    return a + math.log(1 + math.exp(b-a))


def local_score(features):
    return sum([weights[f] for f in features])


def calculate_expected(words: list):
    n = len(words) - 1
    forward = defaultdict(lambda: defaultdict(float))
    backward = defaultdict(lambda: defaultdict(float))
    forward[0]["<s>"] = 0
    backward[n]["<\s>"] = 0

    # collect forward scores
    for i in range(1, n):
        for tag in tagset:
            for prev_tag, prev_score in forward[i-1].items():
                features = get_features(words[i], tag, prev_tag)
                fwd_score = prev_score + local_score(features)
                forward[i][tag] = log_sum_exp(forward[i][tag], fwd_score)
    # collect backward scores
    for j in range(n-1, 0, -1):
        for tag in tagset:
            for prev_tag, prev_score in backward[j+1].items():
                features = get_features(words[j], tag, prev_tag)
                bwd_score = prev_score + local_score(features)
                backward[j][tag] = log_sum_exp(backward[j][tag], bwd_score)
    # calculate estimated feature values
    estimated = defaultdict(float)
    for i in range(1, n):
        for tag, beta_score in backward[i].items():
            for prev_tag, alpha_score in forward[i-1].items():
                f = get_features(words[i], tag, prev_tag)
                gamma = alpha_score + local_score(f) + beta_score - forward[-1]["<\s>"]
                for feature in f:
                    estimated[feature] += 1 * gamma # the value of a feature is its occurrence - which is 1
    return estimated


def calculate_observed(words, tags):
    observed = defaultdict(float)
    n = len(words) - 1
    for i in range(1, n):
        features = get_features(words[i], tags[i], tags[i-1])
        for feature in features:
            observed[feature] += 1
    return observed


if __name__ == "__main__":
    epochs = 2
    learning_rate = 0.001
    sentences = read_data()
    for _ in range(epochs):
        for sentence in sentences[0:5]:
            words, tags = sentence
            estimated = calculate_expected(words)
            observed = calculate_observed(words, tags)
            gradient = defaultdict(float)
            for feature in estimated:
                gradient[feature] = observed[feature] - estimated[feature]
            for feature in weights:
                weights[feature] += learning_rate * gradient[feature]
    print(weights)

