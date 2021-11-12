import sys

word1 = sys.argv[1]
word2 = sys.argv[2]
n, m = len(word1), len(word2)

seq_matrix = [[] for _ in range(len(word1)+1)]

for i in range(n+1):
    for k in range(m+1):
        if i == 0 or k == 0:
            seq_matrix[i].append("")
        else:
            diagonal = seq_matrix[i - 1][k - 1]
            if word1[i-1] == word2[k-1]:
                diagonal += word1[i-1]
            compare_words = [seq_matrix[i-1][k], seq_matrix[i][k-1], diagonal]
            seq_matrix[i].append(max(compare_words))

print("Longest Common Sequence: " + seq_matrix[n][m])