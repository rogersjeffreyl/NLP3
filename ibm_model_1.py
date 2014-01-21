__author__ = 'rogersjeffrey'
"""
This class  has methods that  use IBM-model 1 for translation

"""
import file_utils
import pprint
from collections import  defaultdict
import  cPickle as pickle
class ibm_model_1:

    def __init__(self,de_corpus,en_corpus):


           self.t_param={}
           self.en_sentences=file_utils.read_gzip_files(en_corpus)
           self.de_sentences=file_utils.read_gzip_files(de_corpus)

    def word_counts(self):
        self.t_param["NULL"]={}
        english_word_count={}
        for i  in range(0,len(self.en_sentences)):

            english_words=self.en_sentences[i].strip().split()
            english_words=["NULL"]+english_words
            german_words=self.de_sentences[i].strip().split()
            for en_word in english_words:
                for de_word in german_words:

                    if en_word not in self.t_param:
                       self.t_param[en_word]={}
                    de_word_for_en_word=self.t_param[en_word]
                    if de_word in de_word_for_en_word:
                       continue
                    self.t_param[en_word][de_word]=0

        for english_word in self.t_param.keys():
            german_words_list=self.t_param[english_word]
            english_word_count[english_word]=len(german_words_list.keys())
        return english_word_count

    def initialize_t_params(self):

        en_word_count=self.word_counts()
        for words in en_word_count:
            for german_words in self.t_param[words]:
                self.t_param[words][german_words]=1/float(en_word_count[words])



    def calc_denominator_for_delta(self,english_sentence,german_word):
        sum_of_t = 0
        for index in range(0,len(english_sentence)):
            eng = english_sentence[index]
            sum_of_t += self.t_param[eng][german_word]
        return sum_of_t

    def run_em(self):
        for t in range(1,6):
            count_eng_ger_pair = defaultdict(int)
            count_eng_words = defaultdict(int)
            for k in range(0,len(self.en_sentences)):
                german_sentence = self.de_sentences[k].strip().split(' ')
                english_sentence = self.en_sentences[k].strip().split(' ')
                english_sentence = ['NULL'] + english_sentence

                for ger in german_sentence:
                    denominator_for_delta = self.calc_denominator_for_delta(english_sentence,ger)
                    for eng in english_sentence:
                        delta = self.t_param[eng][ger]/float(denominator_for_delta)
                        count_eng_ger_pair[ger,eng] = count_eng_ger_pair[ger,eng]  + delta
                        count_eng_words[eng] = count_eng_words[eng] + delta

            for eng_word in self.t_param.keys():
                german_words_for_eng = self.t_param[eng_word]
                for german_word in german_words_for_eng.keys():
                    self.t_param[eng_word][german_word] = count_eng_ger_pair[german_word,eng_word] / count_eng_words[eng_word]
        pickle.dump(self.t_param,open("ibm_1_params.p","wb"))
    def german_word_with_highest_tparam(self,eng_word):
        german_words_for_eng = self.t_param[eng_word]
        sorted_german = sorted(german_words_for_eng.items(), key=lambda x:x[1], reverse=True)
        return sorted_german[0:10]

    def translation_for_words_in_file(self,file_name):
        dev_file = open(file_name)
        english_words = dev_file.readlines()
        for eng_word in english_words:
            eng_word = eng_word.strip()
            best_german_words = self.german_word_with_highest_tparam(eng_word)
            print "The english word is: %s" %(eng_word)
            print "German Word:"
            print "____________________________________"
            pprint.pprint(best_german_words)
        dev_file.close()

    def get_best_alignment(self):
        count=0
        alignment_sequence={}
        for k in range(0,len(self.en_sentences)):
             if k>19:
                break
             english_words=self.en_sentences[k].strip().split()
             english_words=["NULL"]+english_words
             german_words=self.de_sentences[k].strip().split()
             de_word_alignments=[]
             for de_word in german_words:
                 max_t_val=0.0
                 max_en_word=None
                 max_align=0
                 for en_word in english_words:
                    current_t=self.t_param[en_word][de_word]

                    if current_t>max_t_val:
                       max_t_val=current_t
                       max_en_word=en_word

                 de_word_alignments.append(str(english_words.index(max_en_word)))
             print "Alignment for the german sentence %s is:" %(self.de_sentences[k])
             print (" ").join(de_word_alignments)



