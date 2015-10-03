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
#           Byron Wallce <byron.wallace@utexas.edu>

from scipy.sparse import csr_matrix
import hickle
import numpy as np
import scipy

class MiniClassifier:
    """
    Lightweight classifier
    Does only binary prediction using externally trained data
    """

    def __init__(self, filename):

        # Models are compressed numpy files
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.savez_compressed.html
        # with the following keys:
        #   intercept, data, indices, indptr
        # where the latter three items form a csr_matrix sparse
        # representation of the model coefficients
        # This is immediately converted to the dense representation
        # to speed up prediction (the .A1 bit returns the data
        # contents of the numpy matrix as a numpy array, making
        # calculations much quicker)

        raw_data = np.load(filename)

        self.coef = csr_matrix((raw_data['data'], raw_data['indices'], raw_data['indptr']), shape=(1, 67108864)).todense().A1
        self.intercept = raw_data['intercept']


    def decision_function(self, X):
        scores = X.dot(self.coef.T) + self.intercept
        return scores

    def predict(self, X):
        scores = self.decision_function(X)
        return (scores>0).astype(np.int)

def main():
    pass


if __name__ == '__main__':
    main()
