#
#   takes string as input, returns bias information as JSON
#

import json
from nltk.tokenize import sent_tokenize
from classifier import MiniClassifier
from vectorizer import ModularVectorizer


class BiasRobot:

    def __init__(self):
        
        self.sent_clf = MiniClassifier('robots/sent_bias_model.rbt')
        self.doc_clf = MiniClassifier('robots/doc_bias_model.rbt')
        self.vec = ModularVectorizer(norm=None, non_negative=True, binary=True, ngram_range=(1, 2), n_features=2**26)

        self.bias_domains = ['Random sequence generation', 'Allocation concealment', 'Blinding of participants and personnel', 'Blinding of outcome assessment', 'Incomplete outcome data', 'Selective reporting']

    def annotate(self, doc_text, domain=None):

        if domain is None:
            domain = self.bias_domains

        # allow domain to be either a domain itself or index of one
        if isinstance(domain, int):
            domain = self.bias_domains[domain]
        else:
            assert domain in self.bias_domains



        doc_sents = sent_tokenize(doc_text)
        doc_domains = [domain] * len(doc_sents)
        doc_X_i = zip(doc_sents, doc_domains)



        self.vec.builder_clear()

        self.vec.builder_add_docs(doc_sents)
        self.vec.builder_add_docs(doc_X_i)
        doc_sents_X = self.vec.builder_transform()
        doc_sents_preds = self.sent_clf.predict(doc_sents_X).A1

        high_prob_sents = [sent for sent, sent_pred in 
                                    zip(doc_sents, doc_sents_preds) if sent_pred==1]

        high_prob_sents_j = " ".join(high_prob_sents)

        sent_domain_interaction = "-s-" + domain

        # build up test vector
        self.vec.builder_clear()
        self.vec.builder_add_docs([doc_text]) # add base features
        self.vec.builder_add_docs([(doc_text, domain)]) # add interactions
        self.vec.builder_add_docs([(high_prob_sents_j, sent_domain_interaction)]) # sentence interactions
    
        X = self.vec.builder_transform()

        bias_class = ["HIGH/UNCLEAR", "LOW"]
        bias_pred = bias_class[(self.doc_clf.predict(X).A1[0] + 1) / 2]

        return {"domain": domain,
                "bias level": bias_pred,
                "justification": high_prob_sents}

def main():

    import unidecode, codecs

    with codecs.open('tests/example.txt', 'r', 'ISO-8859-1') as f:
        text = f.read()


    robot = BiasRobot()
    print robot.annotate(text, 0)


if __name__ == '__main__':
    main()