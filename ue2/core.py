import nltk
import unittest

TESTCASE_TXT = 'austen-emma.txt'

def top_suffixes(words):
    suffix_ls = [w[-2:] for w in words if len(w) > 4]
    dist = nltk.FreqDist(suffix_ls)
    return dist.most_common(10)


class Ue2Test(unittest.TestCase):
    def test_core(self):
        words = nltk.corpus.gutenberg.words(TESTCASE_TXT)
        res = top_suffixes(words)
        print res
        
        
if __name__ == '__main__':
    unittest.main()
    