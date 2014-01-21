__author__ = 'rogersjeffrey'
"""
This class  has methods that  use IBM-model 1 for translation

"""
import file_utils
import pprint
from collections import  defaultdict
import cPickle as pickle
class ibm_model_2:

    def __init__(self,de_corpus,en_corpus):


           self.t_param={}
           self.en_sentences=file_utils.read_gzip_files(en_corpus)
           self.de_sentences=file_utils.read_gzip_files(de_corpus)
           self.q_params={}

    def initialize_t_params(self):
        self.t_param=pickle.load(open("ibm_1_params.p","rb"))


    def initialize_q_params(self):
        for k in range(0,len(self.en_sentences)):
                german_sentence = self.de_sentences[k].strip().split(' ')
                english_sentence = self.en_sentences[k].strip().split(' ')
                l=len(english_sentence)
                m=len(german_sentence)

                for i in range(1,m+1):
                    for j in range(0,l+1):
                        self.q_params[j,i,l,m]=1/float(l+1)


    def calc_denominator_for_delta(self,english_sentence,german_word,i,l,m):
        sum_of_t = 0
        for j in range(0,len(english_sentence)):
            eng = english_sentence[j]


            sum_of_t += self.t_param[eng][german_word]*self.q_params[j,i,l,m]
        return sum_of_t

    def run_em(self):

                for t in range(1,6):
                    count_eng_ger_pair = defaultdict(int)
                    count_eng_words = defaultdict(int)
                    count_j_i_l_m = defaultdict(int)
                    count_i_l_m = defaultdict(int)
                    for k in range(0,len(self.en_sentences)):
                        german_sentence = self.de_sentences[k].strip().split(' ')
                        m = len(german_sentence)
                        english_sentence = self.en_sentences[k].strip().split(' ')
                        l = len(english_sentence)
                        english_sentence = ['NULL'] + english_sentence

                        for i in range(1,len(german_sentence)+1):
                            ger = german_sentence[i-1]
                            denominator = self.calc_denominator_for_delta(english_sentence,ger,i,l,m)
                            for j in range(0,len(english_sentence)):
                                eng = english_sentence[j]
                                delta = self.t_param[eng][ger] * self.q_params[j,i,l,m]/ float(denominator)
                                count_eng_ger_pair[ger,eng] = count_eng_ger_pair[ger,eng]  + delta
                                count_eng_words[eng] = count_eng_words[eng] + delta
                                count_j_i_l_m[j,i,l,m] = count_j_i_l_m[j,i,l,m] + delta
                                count_i_l_m[i,l,m] = count_i_l_m[i,l,m] + delta

                    for eng_word in self.t_param.keys():
                        german_words_for_eng = self.t_param[eng_word]
                        for german_word in german_words_for_eng.keys():
                            self.t_param[eng_word][german_word] = count_eng_ger_pair[german_word,eng_word] / count_eng_words[eng_word]

                    for alignment in self.q_params.keys():
                        i = alignment[1]
                        l = alignment[2]
                        m = alignment[3]
                        self.q_params[alignment] = float(count_j_i_l_m[alignment]) / count_i_l_m[i,l,m]

                pickle.dump(self.t_param,open("ibm_2_t_params.p","wb"))
                pickle.dump(self.q_params,open("ibm_2_q_params.p","wb"))


    def get_best_alignment(self):
        count=0
        alignment_sequence={}
        for k in range(0,len(self.en_sentences)):
             if k>19:
                break
             english_words=self.en_sentences[k].strip().split()
             l=len(english_words)
             english_words=["NULL"]+english_words

             german_words=self.de_sentences[k].strip().split()
             m=len(german_words)
             de_word_alignments=[]
             for i in range(1,m+1) :
                 de_word=german_words[i-1]
                 max_t_val=0.0
                 max_en_word=None
                 max_align=0
                 for j in range(0,l+1):
                    en_word=english_words[j]
                    current_t=self.t_param[en_word][de_word] *self.q_params[j,i,l,m]

                    if current_t>max_t_val:
                       max_t_val=current_t
                       max_en_word=en_word
                       max_align=j

                 de_word_alignments.append(str(max_align))
             print "Alignment for the german sentence %s is:" %(self.de_sentences[k])
             print (" ").join(de_word_alignments)



