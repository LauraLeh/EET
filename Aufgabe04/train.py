import os
from collections import defaultdict
freq = defaultdict()

# read all files
path = './dev' # noch ändern!!
for root, dirs, files in os.walk(path):
    for c in dirs:
        freq[c] = defaultdict(int)
    for file in files:
        with open(os.path.join(root, file), "r", encoding="utf-8") as auto:
            for c in freq.keys():
                if c in os.path.join(root, file):
                    try:
                        text = auto.read()
                        for word in text.split():
                            freq[c][word] += 1
                    except:
                        print(os.path.join(root, file), " could not be read")

print(freq)
