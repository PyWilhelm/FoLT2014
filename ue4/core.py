from nltk.corpus import wordnet as wn

with open('testing.txt') as f:
    lines = f.readlines()
testing_pair_list = []
for line in lines:
    testing_pair_list.append(line.replace('\n','').split('-') + [0])

testing_pair_synset = []
for pair in testing_pair_list:
    first_sets = wn.synsets(pair[0])
    second_sets = wn.synsets(pair[1])
    similarity = max([first.path_similarity(second) for first in first_sets for second in second_sets])
    pair[2] = similarity
for pair in testing_pair_list:
    print pair[0] + '-' + pair[1], pair[2]