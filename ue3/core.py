#-*- coding: utf-8 -*-

from nltk.corpus import udhr
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk import word_tokenize
import re
from nltk.util import bigrams
import unittest

languages = ['English', 'German_Deutsch', 'French_Francais', 'Spanish']
ignores = '.,-\'""0123456789;?!:'

strip_ignores = lambda ls: [i for i in ls if len(i) > 1 or i not in ignores]

class LanguageDeterminator(object):
    def __init__(self, languages):
        self._langs = languages
        self._language_base = dict((language, udhr.words(language + '-Latin1')) for language in languages)
        self._language_model_cfd = self.build_language_models()
    
    def build_language_models(self):
        return ConditionalFreqDist()
    
    def generate_ds(self, words):
        return None, None
    
    def _algo(self, learning_info_dict, testing_info_dict):
        amount = sum(testing_info_dict.values())
        testing_info_dict = {w: testing_info_dict[w] / amount * 100 for w in testing_info_dict}
        for lang in learning_info_dict.keys():
            amount = sum(learning_info_dict[lang].values())
            learning_info_dict[lang] = {w: learning_info_dict[lang][w] / amount * 100 for w in learning_info_dict[lang]}
        evaluation_dict = {}
        for lang in learning_info_dict.keys():
            value = 0
            for subkey in learning_info_dict[lang].keys():
                value += learning_info_dict[lang][subkey] * testing_info_dict.get(subkey, 0)
            evaluation_dict[lang] = value
        return sorted(evaluation_dict.iteritems(), key=lambda item: item[1], reverse=True)
    
    def guess_language(self, text):
        test_words = word_tokenize(text)
        learning_info_dict, testing_info_dict = self.generate_ds(test_words)
        manhattan_distances_list = self._algo(learning_info_dict, testing_info_dict)
        if len(manhattan_distances_list) == 0:
            raise Exception('Function evaluate must be implemented in sub class')
        return manhattan_distances_list[0][0]
    
    
class LDChar(LanguageDeterminator):
    def build_language_models(self):
        condition = [(language, char.lower()) 
                     for language in self._langs for word in (self._language_base[language]) for char in word]
        return ConditionalFreqDist(condition)
    
    def generate_ds(self, words):
        
        learning_info_dict = {lang: {w: float(t) 
                              for w, t in [(w, _) for (w, _) in self._language_model_cfd[lang].most_common() 
                                           if w not in ignores]} for lang in self._language_model_cfd.keys()}
        testing_info_dict = {w: float(t) 
                             for w, t in [(w, _) 
                                          for (w, _) in FreqDist([c for word in words for c in word.lower()]).most_common() 
                                          if w not in ignores]}
        return learning_info_dict, testing_info_dict

    
class LDToken(LanguageDeterminator):
    def build_language_models(self):
        condition = [(lang, word.lower()) for lang in self._langs for word in self._language_base[lang]]
        return ConditionalFreqDist(condition)
    
    def generate_ds(self, words):
        learning_info_dict = {lang: {w: float(t) 
                              for w, t in [(w, _) for (w, _) in self._language_model_cfd[lang].most_common() 
                                           if w not in ignores]} for lang in self._language_model_cfd.keys()}
        testing_info_dict = {w: float(t) 
                             for w, t in [(w, _) 
                                          for (w, _) in FreqDist([word.lower() for word in words]).most_common() 
                                          if w not in ignores]}
        return learning_info_dict, testing_info_dict


class LDCharBigram(LanguageDeterminator):
    def build_language_models(self):
        condition = [(lang, tpl) for lang in self._langs for word in self._language_base[lang] for tpl in bigrams(word.lower())]
        return ConditionalFreqDist(condition)
    
    def generate_ds(self, words):
        learning_info_dict = {lang: {w: float(t) 
                              for w, t in self._language_model_cfd[lang].most_common()} 
                              for lang in self._language_model_cfd.keys()}
        testing_info_dict = {w: float(t) 
                             for w, t in FreqDist([tpl for word in words for tpl in bigrams(word)]).most_common()}
        return learning_info_dict, testing_info_dict

    
class LDTokenBigram(LanguageDeterminator):
    def build_language_models(self):
        condition = [(lang, tpl) for lang in self._langs for tpl in bigrams([w.lower() for w in self._language_base[lang]])]
        return ConditionalFreqDist(condition)
    
    def generate_ds(self, words):
        learning_info_dict = {lang: {w: float(t) 
                              for w, t in self._language_model_cfd[lang].most_common()} 
                              for lang in self._language_model_cfd.keys()}
        testing_info_dict = {w: float(t) 
                             for w, t in FreqDist(bigrams([w.lower() for w in words])).most_common()}
        return learning_info_dict, testing_info_dict

class MainTest(unittest.TestCase):
    def setUp(self):
        self.text1 = "these functions can return any value, which may or may not be interpretable as a Boolean value. See Comparisons for more information about rich comparisons."
        self.text2 = "Il dispute ses premiers matchs au sein de la Ligue d'Alsace de football, atteint la DH en 1924 et obtient le statut professionnel "
        self.text3 = "Sie moechten die Attraktivitaet Ihres Internet-Portales erhoehen und Ihren Kunden DB-Fahrkarten rund um die Uhr anbieten? Sie moechten Ihr Produktportfolio um Services rund um die Bahn erweitern? Dann arbeiten Sie mit der Deutschen Bahn zusammen und profitieren Sie von unseren attraktiven Angeboten!"
        #self.text1 = "Peter had been to the office before they arrived."
        #self.text2 = "Si tu finis tes devoirs, je te donnerai des bonbons."
        #self.text3 = "Das ist ein schon recht langes deutsches Beispiel."
        print ''
    
    def test_based_char(self):
        print '---START: Testing: based on the frequency of characters---'
        ld = LDChar(languages)
        print 'guess for english text is', ld.guess_language(self.text1)
        print 'guess for french text is', ld.guess_language(self.text2)
        print 'guess for german text is', ld.guess_language(self.text3)
        print '---FINISH: Testing: based on the frequency of characters---'
        
    def test_based_token(self):
        print '---START: Testing: based on the frequency of tokens---'
        ld = LDToken(languages)
        print 'guess for english text is', ld.guess_language(self.text1)
        print 'guess for french text is', ld.guess_language(self.text2)
        print 'guess for german text is', ld.guess_language(self.text3)
        print '---FINISH: Testing: based on the frequency of tokens---'
        
    def test_based_charbigrams(self):
        print '---START: Testing: based on the frequency of character bigrams---'
        ld = LDCharBigram(languages)
        print 'guess for english text is', ld.guess_language(self.text1)
        print 'guess for french text is', ld.guess_language(self.text2)
        print 'guess for german text is', ld.guess_language(self.text3)
        print '---FINISH: Testing: based on the frequency of character bigrams---'
        
    def test_based_tokenbigrams(self):
        print '---START: Testing: based on the frequency of tokens bigrams---'
        ld = LDTokenBigram(languages)
        print 'guess for english text is', ld.guess_language(self.text1)
        print 'guess for french text is', ld.guess_language(self.text2)
        print 'guess for german text is', ld.guess_language(self.text3)
        print '---FINISH: Testing: based on the frequency of tokens bigrams---'
        
    def test_lang_similar(self):
        print 'lang_similar'
        ld = LDChar(languages)
        t_ls = [udhr.raw(language + '-Latin1') for language in languages]
        for t in t_ls:
            print ld.guess_language(t)
        print 'lang_similar FINISH'

if __name__ == '__main__':
    unittest.main()
