import numpy as np


class Perceptron:

    """Perceptron classifier.

    Parameters
    ------------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over the training dataset.

    Attributes
    -----------
    w_ : 1d-array
        Weights after fitting. w[0] = threshold
    errors_ : list
        Number of miss classifications in each epoch.

    """

    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter
        self.b = None
        self.w = None

    def fit(self, X, y):
        """Fit training dat.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.
        """
        self.b = np.zeros(1)
        self.w = np.zeros(X.shape[1])

        for _ in range(self.n_iter):
            for j in range(X.shape[0]):
                f = self.b + np.sum(self.w * X[j])
                self.b = self.b + self.eta * (y[j] - f)
                self.w = self.w + self.eta * (y[j] - f) * X[j]

    def predict(self, X):
        """Return class label.
            First calculate the output: (X * weights) + threshold
            Second apply the step function
            Return a list with classes
        """
        return (self.b + np.sum(self.w * X, axis=-1) >= 0).astype(np.int8)
