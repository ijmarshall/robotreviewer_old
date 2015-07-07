#
#   code for processing rbt model files
#

from scipy.sparse import csr_matrix
import hickle
import numpy as np

class MiniClassifier:
    """
    Lightweight classifier
    Does only binary prediction using externally trained data
    """

    def __init__(self, filename):

        # Models are HDF files via hickle with 4 item tuple
        # (intercept, data, indices, indptr)
        # where the latter three items form a csr_matrix sparse
        # representation of the model coefficients

        raw_data = hickle.load(filename)
        self.coef = csr_matrix((raw_data[1], raw_data[2], raw_data[3]), shape=(1, 67108864))
        self.intercept = raw_data[0]

    def decision_function(self, X):
        # assumes csr_matrix as X

        # print X, X.shape
        # print self.coef, self.coef.shape

        # print "X"
        # print X
        # print X.shape

        # print "coef"
        # print self.coef
        # print self.coef.shape

        scores = X.dot(self.coef.T).todense() + self.intercept
        return scores.flatten()

    def predict(self, X):

        scores = self.decision_function(X)
        return np.sign(scores).astype(int)

        # indices = (scores > 0).astype(np.int)
        # return indices.flatten()
        


def main():
    pass


if __name__ == '__main__':
    main()