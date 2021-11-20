import sys
import os
from collections import Counter
import pickle

spammaildir = sys.argv[1]
hammaildir = sys.argv[2]
paramfile = sys.argv[3]
#spammaildir = './train/spam'
#hammaildir = './train/ham'
#paramfile = 'paramfile'

class Naive_Bayes:
    def __init__(self, spam_dir, ham_dir):
        self.spam_num, self.spam_token = self.read_txt(spam_dir)
        self.ham_num, self.ham_token = self.read_txt(ham_dir)
        self.priori_spam = self.spam_num/(self.spam_num + self.ham_num)
        self.priori_ham = self.ham_num/(self.spam_num + self.ham_num)
        self.spam_word_freq = Counter(self.spam_token)
        self.ham_word_freq = Counter(self.ham_token)
        self.word_prob, self.discount = self.all_word_prob()
        self.spam_relat_prob = self.relative_prob(self.spam_word_freq)
        self.ham_relat_prob = self.relative_prob(self.ham_word_freq)
        self.alpha_spam = 1 - sum(self.spam_relat_prob.values())
        self.alpha_ham = 1 - sum(self.ham_relat_prob.values())
        self.spam_word_prob = self.condition_word_prob(self.spam_relat_prob,self.alpha_spam)
        self.ham_word_prob = self.condition_word_prob(self.ham_relat_prob, self.alpha_ham)

    # read date and return the number of files as well as the tokenized content
    def read_txt(self, directory):
        mail_list = [directory+'/'+file for _, _, files in os.walk(directory) for file in files]
        content = ''
        for mail in mail_list:
            with open(mail, 'r', encoding='ISO-8859-1') as m:
                txt = m.read()
                content += txt
        return len(mail_list), content.split()

    # discount = N1 / (N1 + 2 N2)
    # p(w) = f(w) / \sum_w' f(w')
    def all_word_prob(self):
        all_word_freq = Counter(self.spam_token + self.ham_token)
        n1 = list(self.spam_word_freq.values()).count(1) + list(self.ham_word_freq.values()).count(1)
        n2 = list(self.spam_word_freq.values()).count(2) + list(self.ham_word_freq.values()).count(2)
        discount = n1 / (n1 + 2 * n2) if (n1 + 2 * n2) != 0 else 0
        total_word = sum(all_word_freq.values())
        word_prob = {word: freq / total_word for word, freq in all_word_freq.items()}
        return word_prob, discount

    # r(w,c) = [f(w,c) - discount] / \sum_w' f(w',c)
    def relative_prob(self, word_freq):
        total_word = sum(word_freq.values())
        relat_prob = {word: max(0, (word_freq.get(word,0) - self.discount)/total_word) for word in self.word_prob.keys()}
        return relat_prob

    # p(w|c) = r(w,c) + alpha(c) p(w)
    def condition_word_prob(self, relative_prob, alpha):
        con_word_prob = {word: relative_prob[word] + alpha*self.word_prob[word] for word in relative_prob.keys()}
        return con_word_prob

    def save_parameters(self, filename):
        map_table = dict()
        map_table['priori_spam'] = self.priori_spam
        map_table['priori_ham'] = self.priori_ham
        map_table['spam_word_prob'] = self.spam_word_prob
        map_table['ham_word_prob'] = self.ham_word_prob
        with open(filename, 'wb') as file:
            pickle.dump(map_table, file)



