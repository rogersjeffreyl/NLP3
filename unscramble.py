__author__ = 'rogersjeffrey'
import pprint as pprint
import math
import cPickle as pickle

class unscramble:

    def __init__(self,scrambled_en_file, scrambled_de_file):

        self.english_file=scrambled_en_file
        self.german_file=scrambled_de_file
        self.q=pickle.load(open("ibm_2_q_params.p"))
        self.t=pickle.load(open("ibm_2_t_params.p"))
        self.english_sentences=[]
        self.german_sentences=[]

    def read_files(self):
        ger_file = open(self.german_file)
        eng_file = open(self.english_file)
        self.german_sentences = ger_file.readlines()
        self.english_sentences = eng_file.readlines()

    def get_original_sentences(self):
        corresponding_english_sentences = []
        index = 0
        for german_sentence in self.german_sentences:
            index+= 1
            german_sentence = german_sentence.strip().split()
            max_value = -10000000000
            best_eng_sen = []
            eng_index = 0
            for english_sentence in self.english_sentences:
                eng_index+= 1
                english_sentence = english_sentence.strip().split()
                alignment,computed_product = self.get_alignment(english_sentence,german_sentence)
                if(computed_product > max_value):
                    max_value = computed_product
                    best_eng_sen = english_sentence

            best_eng_sen = (' ').join(best_eng_sen)
            best_eng_sen += '\n'
            corresponding_english_sentences.append(best_eng_sen)
            #pprint.pprint(best_eng_sen)
        # wirting the unscrambled english sentences
        f = open("unscrambled_eng_sentences","w")
        f.writelines(corresponding_english_sentences)
        f.close()


    def get_alignment(self,english_sentence,german_sentence):
            l = len(english_sentence)
            english_sentence = ['NULL'] + english_sentence
            alignment_for_sentence = []
            m = len(german_sentence)
            log_probability = 0
            for i in range(1,m+1):
                max_val = -1000
                max_j = 0
                german_word = german_sentence[i-1]
                # finding the max possible alignment sequence
                # finding the max possible alignment sequence
                for j in range(0,l+1):
                    eng_word = english_sentence[j]
                    german_word_for_eng = self.t.setdefault(eng_word,{})
                    german_word_for_eng.setdefault(german_word,0.0)
                    self.q.setdefault((j,i,l,m),0.0)
                    calc = self.t[eng_word][german_word] * self.q[j,i,l,m]
                    if(calc > max_val):
                        max_val = calc
                        max_j = j

                alignment_for_sentence.append(max_j)
                if(max_val == 0):
                    log_probability+= -99999999
                else:
                    log_probability+=math.log(max_val)
            return alignment_for_sentence,log_probability