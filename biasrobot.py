#
#   takes string as input, returns bias information as JSON
#

import json
import uuid
from nltk.tokenize import sent_tokenize
from classifier import MiniClassifier
from vectorizer import ModularVectorizer
from itertools import izip

class BiasRobot:

    def __init__(self):
        
        self.sent_clf = MiniClassifier('robots/sent_model_o.rbt')
        # print self.sent_clf.intercept
        self.doc_clf = MiniClassifier('robots/doc_model_o.rbt')
        # print self.doc_clf.intercept
        self.vec = ModularVectorizer(norm=None, non_negative=True, binary=True, ngram_range=(1, 2), n_features=2**26)
    

        self.bias_domains = ['Random sequence generation', 'Allocation concealment', 'Blinding of participants and personnel', 'Blinding of outcome assessment', 'Incomplete outcome data', 'Selective reporting']

    def annotate(self, doc_text, domains=None):

        # Some processing to allow flexibility of domains parameter

        # check all domains by default
        if domains is None: 
            domains = self.bias_domains
        
        # make into a list if a single item passed
        if isinstance(domains, list)==False:
            domains = [domains]

        # allow domain to be either a domain itself or index of one
        # (first element checked)
        if isinstance(domains[0], int):
            domains = [self.bias_domains[domain] for domain in domains]

        marginalia = []
        
        doc_sents = sent_tokenize(doc_text)

        for domain in domains:

            
            doc_domains = [domain] * len(doc_sents)
            doc_X_i = izip(doc_sents, doc_domains)



            self.vec.builder_clear()

            self.vec.builder_add_docs(doc_sents)
            self.vec.builder_add_docs(doc_X_i)
            doc_sents_X = self.vec.builder_transform()
            doc_sents_preds = self.sent_clf.predict(doc_sents_X)

            high_prob_sents = [sent for sent, sent_pred in 
                                        izip(doc_sents, doc_sents_preds) if sent_pred==1]

            high_prob_sents_j = " ".join(high_prob_sents)

            sent_domain_interaction = "-s-" + domain

            # build up test vector
            self.vec.builder_clear()
            self.vec.builder_add_docs([doc_text]) # add base features
            self.vec.builder_add_docs([(doc_text, domain)]) # add interactions
            self.vec.builder_add_docs([(high_prob_sents_j, sent_domain_interaction)]) # sentence interactions
        
            X = self.vec.builder_transform()

            print X.shape

            

            bias_pred = self.doc_clf.predict(X)
            bias_class = ["high/unclear", "low"][bias_pred[0]]


            
            marginalia.append({"type": "Risk of Bias",
                               "title": domain,
                "annotations": [{"content": sent, "uuid": str(uuid.uuid1())} for sent in high_prob_sents],
                "description": "**Overall risk of bias prediction**: " + bias_class})

        return {"marginalia": marginalia}

def main():

    import unidecode, codecs

    with codecs.open('tests/example.txt', 'r', 'ISO-8859-1') as f:
        text = f.read()

    robot = BiasRobot()
    print robot.annotate(text)


if __name__ == '__main__':
    main()