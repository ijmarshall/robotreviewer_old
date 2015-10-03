"""
the BiasRobot class takes the full text of a clinical trial as
input as a string, and returns bias information as a dict which
can be easily converted to JSON.

    text = "Streptomycin Treatment of Pulmonary Tuberculosis: A Medical Research Council Investigation..."

    robot = BiasRobot()
    annotations = robot.annotate(text)

Implements the models which were validated in the paper:

Marshall IJ, Kuiper J, & Wallace BC. RobotReviewer: evaluation of a system for automatically assessing bias in clinical trials. Journal of the American Medical Informatics Association 2015.doi:10.1093/jamia/ocv044
"""

# Authors:  Iain Marshall <mail@ijmarshall.com>
#           Joel Kuiper <me@joelkuiper.com>
#           Byron Wallce <byron.wallace@utexas.edu>

import json
import uuid
import os

from nltk.tokenize import sent_tokenize
from classifier import MiniClassifier
from vectorizer import ModularVectorizer
from itertools import izip
import numpy as np

class BiasRobot:

    def __init__(self):
        abs_dir = os.path.dirname(__file__) # absolute path to here

        self.sent_clf = MiniClassifier(os.path.join(abs_dir, 'robots/bias_sent_level.npz'))
        self.doc_clf = MiniClassifier(os.path.join(abs_dir, 'robots/bias_doc_level.npz'))

        self.vec = ModularVectorizer(norm=None, non_negative=True, binary=True, ngram_range=(1, 2), n_features=2**26)

        self.bias_domains = ['Random sequence generation', 'Allocation concealment', 'Blinding of participants and personnel', 'Blinding of outcome assessment', 'Incomplete outcome data', 'Selective reporting']


    def annotate(self, doc_text, top_k=3):

        """
        Annotate full text of clinical trial report
        `top_k` refers to 'top-k recall'.

        top-1 recall will return the single most relevant sentence
        in the document, and top-3 recall the 3 most relevant.

        The validation study assessed the accuracy of top-3 and top-1
        and we suggest top-3 as default
        """



        marginalia = []

        doc_sents = sent_tokenize(doc_text)

        for domain in self.bias_domains:


            doc_domains = [domain] * len(doc_sents)
            doc_X_i = izip(doc_sents, doc_domains)

            #
            # build up sentence feature set
            #
            self.vec.builder_clear()

            # uni-bigrams
            self.vec.builder_add_docs(doc_sents)

            # uni-bigrams/domain interactions
            self.vec.builder_add_docs(doc_X_i)

            doc_sents_X = self.vec.builder_transform()
            doc_sents_preds = self.sent_clf.decision_function(doc_sents_X)

            high_prob_sent_indices = np.argsort(doc_sents_preds)[:-top_k-1:-1] # top k, with no 1 first

            high_prob_sents = [doc_sents[i] for i in high_prob_sent_indices]

            high_prob_sents_j = " ".join(high_prob_sents)

            sent_domain_interaction = "-s-" + domain

            #
            # build up document feature set
            #
            self.vec.builder_clear()

            # uni-bigrams
            self.vec.builder_add_docs([doc_text])

            # uni-bigrams/domain interaction
            self.vec.builder_add_docs([(doc_text, domain)])

            # uni-bigrams/relevance interaction
            self.vec.builder_add_docs([(high_prob_sents_j, sent_domain_interaction)])

            X = self.vec.builder_transform()

            bias_pred = self.doc_clf.predict(X)
            bias_class = ["high/unclear", "low"][bias_pred[0]]

            marginalia.append({
                "type": "Risk of Bias",
                "title": domain,
                "annotations": [{"content": sent, "uuid": str(uuid.uuid1())} for sent in high_prob_sents],
                "description": "**Overall risk of bias prediction**: " + bias_class
                })


        return {"marginalia": marginalia}

def main():
    # Sample code to make this run
    import unidecode, codecs, pprint
    # Read in example input to the text string
    with codecs.open('tests/example.txt', 'r', 'ISO-8859-1') as f:
        text = f.read()

    # Make a BiasRobot, and use it to do Risk of Bias predictions
    robot = BiasRobot()
    annotations = robot.annotate(text)

    print "EXAMPLE OUTPUT:"
    print
    pprint.pprint(annotations)


if __name__ == '__main__':
    main()
