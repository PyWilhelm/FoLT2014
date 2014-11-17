from nltk.corpus import wordnet as wn

input_str = '''car-automobile
gem-jewel
journey-voyage
boy-lad
coast-shore
asylum-madhouse
magician-wizard
midday-noon
furnace-stove
food-fruit
bird-cock
bird-crane
tool-implement
brother-monk
lad-brother
crane-implement
journey-car
monk-oracle
cemetery-woodland
food-rooster
coast-hill
forest-graveyard
shore-woodland
monk-slave
coast-forest
lad-wizard
chord-smile
glass-magician
rooster-voyage
noon-string'''

def ue4():
    lines = input_str.split('\n')
    testing_pair_list = []
    for line in lines:
        testing_pair_list.append(line.replace('\n','').split('-') + [0])
    for pair in testing_pair_list:
        first_sets = wn.synsets(pair[0])
        second_sets = wn.synsets(pair[1])
    
        similarity = max([first.path_similarity(second) for first in first_sets for second in second_sets])
        pair[2] = similarity
    resorted_pair_list = sorted(testing_pair_list, key=lambda i: i[2], reverse=True)
    print 'word1-word2:\tOL,NL;\tDIFF\n------------------------------'
    for pair in testing_pair_list:
        print '%s-%s:\t%d,  %d;\t%d' %(pair[0], pair[1], testing_pair_list.index(pair), resorted_pair_list.index(pair), \
                                    testing_pair_list.index(pair) - resorted_pair_list.index(pair))
    
if __name__ == '__main__':
    ue4()
