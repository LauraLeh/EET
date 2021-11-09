import sys

word1 = sys.argv[1]
word2 = sys.argv[2]

n = len(word1)
m = len(word2)
word1_1 = ' '+ word1 #erste Spalte inizialisieren
word2_2 = ' '+ word2 #erste Zeile inizialisieren
matrix = [['' for _ in range(m+1)] for _ in range(n+1)]

for i in range(1, (n+1)):
    for k in range(1, (m+1)):
        lenth = {(i, k - 1, matrix[i][k - 1]): len(matrix[i][k - 1]),
                 (i - 1, k, matrix[i - 1][k]): len(matrix[i - 1][k]),
                 (i - 1, k - 1, matrix[i - 1][k - 1]): len(matrix[i - 1][k - 1])}
        x, y, str = max(lenth.keys(), key=lenth.get)
        if word1_1[i] == word2_2[k]:
                matrix[i][k] = word1_1[i]
                matrix[i][k] = str + word1_1[i]
        else:
            matrix[i][k] = str

print(matrix[-1][-1])
