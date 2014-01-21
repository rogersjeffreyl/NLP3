__author__ = 'rogersjeffrey'
import  ibm_model_1

import file_utils
import pprint
model_1_instance=ibm_model_1.ibm_model_1("hw3/corpus.de.gz","hw3/corpus.en.gz")

model_1_instance.initialize_t_params()
model_1_instance.run_em()
#pprint.pprint(model_1_instance.t_param)

model_1_instance.translation_for_words_in_file("hw3/devwords.txt")
model_1_instance.get_best_alignment()
#pprint.pprint(t_param)