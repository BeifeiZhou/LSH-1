# -*- coding: utf-8 -*-
__author__ = "Matti Lyra"

import numpy as np

from .cMinhash import minhash_32, minhash_64

class MinHasher(object):
    def __init__(self, seeds, char_ngram=8, random_state=None, hashbytes=8):
        """The MinHasher creates fingerprints from raw documents.

        The MinHasher facilitates the creation of MinHash document
        fingerprints. It creates overlapping character ngram shingles of length
        `char_ngram` using a sliding window over the document. To preprocessing
        to the documents is done, they are shingled as is.

        Parameters:
        -----------
        seeds: np.ndarray, int
            A Numpy array of 32bit unsigned integers to use as seeds to
            initialise hash functions, or a single integer for the number of
            seeds to create. A minhash is computed for each hash function
            derived from seeds.

        char_ngram: int
            The number of consecutive characters to include in a sliding window
            when creating the document shingles.

        random_state: None, int, np.random.RandomState
            A random state to initialise the random number generator with.
        """
        self.ngram  = char_ngram
        random_state = np.random.RandomState(random_state)
        if hashbytes not in set([4, 8, 16]):
            raise ValueError('Hash has to be 4, 8 or 16 bytes.')

        if hashbytes == 16:
            raise NotImplementedError()

        self.hashbytes = hashbytes
        if isinstance(seeds, np.ndarray):
            self._seeds = seeds
        else:
            self._seeds = np.array(random_state.randint(0, 1e6, seeds),
                                   dtype=np.uint32)
    @property
    def seeds(self):
        return len(self._seeds)

    def fingerprint(self, text):
        if self.hashbytes == 4:
            fingerprint = minhash_32(text, len(text), self._seeds, self.ngram)
        elif self.hashbytes == 8:
            fingerprint = minhash_64(text, len(text), self._seeds, self.ngram)
        return fingerprint
