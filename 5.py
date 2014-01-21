import  ibm_model_2

import file_utils
import pprint

model_2_instance=ibm_model_2.ibm_model_2("hw3/corpus.de.gz","hw3/corpus.en.gz")
model_2_instance.initialize_t_params()
model_2_instance.initialize_q_params()
model_2_instance.run_em()
model_2_instance.get_best_alignment()
