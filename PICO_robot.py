"""
the PICORobot class takes the full text of a clinical trial as
input as a string, and returns Population, Comparator/Intervention
Outcome information as a dict which can be easily converted to JSON.

    text = "Streptomycin Treatment of Pulmonary Tuberculosis: A Medical Research Council Investigation..."

    robot = PICORobot()
    annotations = robot.annotate(text)

The model was derived using the "Supervised Distant Supervision" strategy
introduced in our paper "Extracting PICO Sentences from Clinical Trial Reports
using Supervised Distant Supervision".
"""

# Authors:  Iain Marshall <mail@ijmarshall.com>
#           Joel Kuiper <me@joelkuiper.com>
#           Byron Wallce <byron.wallace@utexas.edu>


import pdb
import bz2
import cPickle as pickle
import json
import uuid
from nltk.tokenize import sent_tokenize
from classifier import MiniClassifier
from itertools import izip
import numpy as np
import pico_vectorizer
import drugbank
import sys
import os

###
# a little bit dirty, sorry.
sys.modules['cochranenlp.ml.pico_vectorizer'] = pico_vectorizer
sys.modules['cochranenlp.textprocessing.drugbank'] = drugbank

from pico_vectorizer import PICO_vectorizer

class PICORobot:

    def __init__(self):
        '''
        Note: we group Intervention and Comparator together
        '''

        ### @TODO!
        '''
        self.P_clf = MiniClassifier("robots/PICO/P_model.rbt", coef_dim=50019)
        P_vec_f = bz2.BZ2File("robots/PICO/P_vectorizer.pbz2", 'r')
        ###
        # this is a bit slow. sorry.
        print "unpickling P vectorizer..."
        self.P_vec = pickle.load(P_vec_f)
        print "ok!"
        '''
        self.P_clf, self.P_vec = PICORobot._load_model_and_v(
            "robots/PICO/P_model.rbt", "robots/PICO/P_vectorizer.pbz2")
        self.I_clf, self.I_vec = PICORobot._load_model_and_v(
            "robots/PICO/I_model.rbt", "robots/PICO/I_vectorizer.pbz2")
        self.O_clf, self.O_vec = PICORobot._load_model_and_v(
            "robots/PICO/O_model.rbt", "robots/PICO/O_vectorizer.pbz2")

        self.models = [self.P_clf, self.I_clf, self.O_clf]
        self.domain_vectorizers = [self.P_vec, self.I_vec, self.O_vec]
        self.PICO_domains = ["Population", "Intervention", "Outcomes"]

    @staticmethod
    def _load_model_and_v(m_path, v_path, coef_dim=50019):
        abs_dir = os.path.dirname(__file__) # absolute path to here
        m = MiniClassifier(os.path.join(abs_dir, m_path), coef_dim=50019)
        print "loading vectorizer: %s ..." % v_path
        v_file = bz2.BZ2File(os.path.join(abs_dir, v_path), 'r')
        print "ok."
        v = pickle.load(v_file)
        return m, v


    def annotate(self, doc_text, top_k=10, min_k=3, alpha=.7):

        """
        Annotate full text of clinical trial report
        `top_k` refers to 'top-k recall'.

        Default alpha was totally scientifically set.
        """
        marginalia = []

        doc_sents = sent_tokenize(doc_text)
        # quintile indicators (w.r.t. document) for sentences
        positional_features = PICORobot._get_positional_features(doc_sents)

        ###
        # @TODO just population (P) for now
        for domain, model, vectorizer in zip(
            self.PICO_domains, self.models, self.domain_vectorizers):

            doc_sents_X = vectorizer.transform(doc_sents, extra_features=positional_features)
            doc_sents_preds = model.predict_proba(doc_sents_X)
            high_prob_sent_indices = np.argsort(doc_sents_preds)[:-top_k-1:-1]

            # filter
            filtered_high_prob_sent_indices = \
                high_prob_sent_indices[doc_sents_preds[high_prob_sent_indices] >= alpha]

            #pdb.set_trace()
            if len(filtered_high_prob_sent_indices) < min_k:
                high_prob_sent_indices = high_prob_sent_indices[:min_k]
            else:
                high_prob_sent_indices = filtered_high_prob_sent_indices

            high_prob_sents = [doc_sents[i] for i in high_prob_sent_indices]


            '''
            doc_sents_preds = model.decision_function(doc_sents_X)
            high_prob_sent_indices = np.argsort(doc_sents_preds)[:-top_k-1:-1] # top k, with no 1 first

            '''
            marginalia.append({
                "type": "PICO",
                "title": domain,
                "annotations": [{"content": sent, "uuid": str(uuid.uuid1())} for sent in high_prob_sents],
                })

        return {"marginalia": marginalia}

    @staticmethod
    def _get_positional_features(sentences):
        ''' generate positional features here (quintiles) for doc sentences. '''
        num_sents = len(sentences)
        quintile_cutoff = num_sents / 5

        if quintile_cutoff == 0:
            sentence_quintiles = [{"DocTooSmallForQuintiles" : 1} for ii in xrange(num_sents)]
            print "tiny file encountered... len=%d" % num_sents
        else:
            sentence_quintiles = [{"DocumentPositionQuintile%d" % (ii/quintile_cutoff): 1} for ii in xrange(num_sents)]
        return sentence_quintiles

def main():
    # Sample code to make this run
    import unidecode, codecs, pprint
    # Read in example input to the text string
    with codecs.open('tests/example.txt', 'r', 'ISO-8859-1') as f:
        text = f.read()

    # make a PICO robot, use it to make predictions
    robot = PICORobot()
    annotations = robot.annotate(text)

    print "EXAMPLE OUTPUT:"
    print
    pprint.pprint(annotations)


if __name__ == '__main__':
    main()
