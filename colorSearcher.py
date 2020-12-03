__author__ = "Dale Hartman"
__date__ = "July 21, 2016 3:38:40 PM$"

# Many implementation details for the color search process were learned from
# the PyImageSearch blog at https://www.pyimagesearch.com/

import numpy as np

class ColorSearcher:
    def __init__(self, index, sorting):
        # store the index we are reading through
        self.index = index
        # store boolean telling us if we should sort the results
        self.sorting = sorting

    def search(self, queryFeatures):
        """
        Take the descriptor of our search image and compute
        the best matching images from the index
        """

        # initialize the dictionary of results
        results = {}

        # loop over the index
        for (k, features) in self.index.items():
            # compute the chi-squared distance between the features
            # in our index and our query features
            d = self.chi2_distance(features, queryFeatures)

            # now update the results dictionary with that result
            results[k] = d

        # sort the results, so that the more relevant results
        # (smaller numbers) are at the front of the list
        if self.sorting == True:
            results = sorted([(v, k) for (k,v) in results.items()])

        # return the results
        return results

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a-b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d


class OptimizedColorSearcher:
    def __init__(self, index, revIndex, sorting):
        # store the index we are reading through
        self.index = index
        # store the reverse index for this film
        self.revIndex = revIndex
        # store boolean telling us if we should sort the results
        self.sorting = sorting

    def search(self, queryFeatures, queryTop):
        """
        Take the descriptor of our search image and compute
        the best matching images from the index
        """

        # first, generate a list of all other screenshots that our query image matches with
        # discarding duplicates
        # If you have fewer or more top colors tracked in the reverse index, you must change the number of indices pulled from here
        optimalList = list( set( self.revIndex[queryTop[0]] + self.revIndex[queryTop[1]] ) )

        # initialize the dictionary of results
        results = {}

        # loop over each key in the reverse index list
        for k in optimalList:
            # grab the features from the full index
            features = self.index[k]
            # compute the chi-squared distance between the features
            # in our index and our query features
            d = self.chi2_distance(features, queryFeatures)

            # now update the results dictionary with that result
            results[k] = d

        # sort the results, so that the more relevant results
        # (smaller numbers) are at the front of the list
        if self.sorting == True:
            results = sorted([(v, k) for (k,v) in results.items()])

        # return the results
        return results

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a-b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d