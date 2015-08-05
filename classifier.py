"""
Lightweight classifier class for linear models trained elsewhere
Requires use of 2^26 (sparse) hashing vectorizer, which (at the
moment) is used for all RobotReviewer models.

Loads 'rbt' model files, which are custom for RobotReviewer. These
are gzipped HDF-5 files which contain the model coefficients and
intercepts in sparse (csr) format. This allows very large models
(often several gigabytes in memory uncompressed) to be loaded
reasonably quickly, and makes for feasible memory usage.
"""

# Authors:  Iain Marshall <mail@ijmarshall.com>
#           Joel Kuiper <me@joelkuiper.com>
#           Byron Wallace <byron.wallace@utexas.edu>
import pdb

from scipy.sparse import csr_matrix
import hickle
import numpy as np
import scipy

class MiniClassifier:
    """
    Lightweight classifier
    Does only binary prediction using externally trained data
    """

    def __init__(self, filename, coef_dim=2**26):
        '''
        Models are HDF files via hickle with 4 item tuple
                (intercept, data, indices, indptr)
        where the latter three items form a csr_matrix sparse
        representation of the model coefficients.
        This is immediately converted to the dense representation
        to speed up prediction (the .A1 bit returns the data
        contents of the numpy matrix as a numpy array, making
        calculations much quicker). 

        Note that the model coefficients must be explicitly
        specified (coef_dim); the 2**26 is for the multi-task
        model, which comprises 67108864 predictors (!)
        '''
        raw_data = hickle.load(filename)
        
        self.coef = csr_matrix((raw_data[1], raw_data[2], raw_data[3]), shape=(1, coef_dim)).todense().A1

        self.intercept = raw_data[0]

    def decision_function(self, X):
        scores = X.dot(self.coef.T) + self.intercept
        return scores

    def predict(self, X):
        scores = self.decision_function(X)
        return (scores>0).astype(np.int)

    def predict_proba(self, X):
        '''
        Note! This really only makes sense if the objective 
        for estimating w included a log-loss! Otherwise need 
        to calibrate.
        '''
        def sigmoid(z):
            s = 1.0 / (1.0 + np.exp(-1.0 * z))
            return s
        scores = self.decision_function(X)
        return sigmoid(scores)


def main():
    pass


if __name__ == '__main__':
    main()
