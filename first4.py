from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

import scipy.stats as stats

brown_ic = wordnet_ic.ic('ic-brown.dat')

print("Choose file (0 or 1):")
print(" >> 0 - 'wordsim_relatedness_goldstandard.txt'")
print(" >> 1 - 'wordsim_similarity_goldstandard.txt'")
MODE = int(input())

FILE = ["wordsim_relatedness_goldstandard.txt", "wordsim_similarity_goldstandard.txt"]
METHOD = ["lch", "wup", "jcn"]
NAME = ["relatedness", "similarity"]

def make_correct_synset(str):
    arr = []
    for synset in wn.synsets(str):
        if (synset.name().split('.')[0] == str and synset.pos() == 'n'):
            arr.append(synset)
    return arr

file = open(FILE[MODE], "r")

F = open("check.txt", "w")

sorted_data = [[], [], []]
data = [[[], []], [[], []], [[], []]]

arr_str = file.readline().split()
while arr_str:

    first = make_correct_synset(arr_str[0])
    second = make_correct_synset(arr_str[1])

    score = [-1, -1, -1]

    for synset1 in first:
        for synset2 in second:
            score[1] = max(score[1], round(synset1.wup_similarity(synset2), 4))
            if (synset1.pos() == synset2.pos()):
                score[0] = max(score[0], round(synset1.lch_similarity(synset2), 4))
                score[2] = max(score[2], round(synset1.jcn_similarity(synset2, brown_ic), 4))

    for i in range (3):
        if score[i] != -1:
            sorted_data[i].append([score[i], arr_str[0], arr_str[1]])
            data[i][0].append(float(arr_str[2]))
            data[i][1].append(score[i])
    F.write(arr_str[0] + ' ' + arr_str[1] + ' ' + arr_str[2] + ' ' + str(score[0]) + ' ' + str(score[1]) + ' ' + str(score[2]) + '\n')
    arr_str = file.readline().split()

# create new files
for i in range (3):
    sorted_data[i].sort(key=lambda x: x[0], reverse=True)
    new_name = NAME[MODE] + '_' + str(METHOD[i]) + ".txt"
    new_file = open(new_name, "w")
    for j in sorted_data[i]:
        new_file.write(j[1] + '    ' + j[2] + '    ' + str(j[0]) + '\n')
    new_file.close()

print("Spearman's measure, " + FILE[MODE] + ':')

for i in range (3):
    rho, p_value = stats.spearmanr(data[i][0], data[i][1])
    print(" >> " + METHOD[i] + ': ' + '%.4f' % rho)

file.close()
F.close()