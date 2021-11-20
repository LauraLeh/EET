import sys
import pickle
import math
import os

spammaildir = sys.argv[1]
hammaildir = sys.argv[2]
paramfile = sys.argv[3]
#spammaildir = './test/spam'
#hammaildir = './test/ham'
#paramfile = 'paramfile'

with open(paramfile, 'rb') as file:
    map_table = pickle.load(file)

priori_spam = map_table['priori_spam']
priori_ham = map_table['priori_ham']
spam_word_prob = map_table['spam_word_prob']
ham_word_prob = map_table['ham_word_prob']


def predict_label(tokens):
    spam_prob,ham_prob = 0,0
    for word in tokens:
        spam_prob += math.log(spam_word_prob.get(word,1))
        ham_prob += math.log(ham_word_prob.get(word,1))
    spam_prob += math.log(priori_spam)
    ham_prob += math.log(priori_ham)
    label = 'spam' if spam_prob > ham_prob else 'ham'
    return label


spam_list = [spammaildir+'/'+file for _, _, files in os.walk(spammaildir) for file in files]
ham_list = [hammaildir+'/'+file for _, _, files in os.walk(hammaildir) for file in files]
mail_list = spam_list + ham_list

correct = 0
for mail in mail_list:
    with open(mail, 'r', encoding='ISO-8859-1') as m:
        txt = m.read().split()
        pred_label = predict_label(txt)
        print(mail,pred_label)
        if pred_label in mail:
            correct += 1

print('total files: {}; correct classified: {}'.format(len(spam_list+ham_list), correct))
print('precision: {}'.format(correct/len(spam_list+ham_list)))
