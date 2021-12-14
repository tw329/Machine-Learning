class SelectKBest(_BaseFilter):
    """Select features according to the k highest scores.
    Read more in the :ref:`User Guide <univariate_feature_selection>`.
    Parameters
    ----------
    score_func : callable
        Function taking two arrays X and y, and returning a pair of arrays
        (scores, pvalues) or a single array with scores.
        Default is f_classif (see below "See also"). The default function only
        works with classification tasks.
    k : int or "all", optional, default=10
        Number of top features to select.
        The "all" option bypasses selection, for use in a parameter search.
    Attributes
    ----------
    scores_ : array-like of shape (n_features,)
        Scores of features.
    pvalues_ : array-like of shape (n_features,)
        p-values of feature scores, None if `score_func` returned only scores.
    Examples
    --------
    >>> from sklearn.datasets import load_digits
    >>> from sklearn.feature_selection import SelectKBest, chi2
    >>> X, y = load_digits(return_X_y=True)
    >>> X.shape
    (1797, 64)
    >>> X_new = SelectKBest(chi2, k=20).fit_transform(X, y)
    >>> X_new.shape
    (1797, 20)
    Notes
    -----
    Ties between features with equal scores will be broken in an unspecified
    way.
    See also
    --------
    f_classif: ANOVA F-value between label/feature for classification tasks.
    mutual_info_classif: Mutual information for a discrete target.
    chi2: Chi-squared stats of non-negative features for classification tasks.
    f_regression: F-value between label/feature for regression tasks.
    mutual_info_regression: Mutual information for a continuous target.
    SelectPercentile: Select features based on percentile of the highest scores.
    SelectFpr: Select features based on a false positive rate test.
    SelectFdr: Select features based on an estimated false discovery rate.
    SelectFwe: Select features based on family-wise error rate.
    GenericUnivariateSelect: Univariate feature selector with configurable mode.
    """

    def __init__(self, score_func=f_classif, k=10):
        super().__init__(score_func)
        self.k = k

    def _check_params(self, X, y):
        if not (self.k == "all" or 0 <= self.k <= X.shape[1]):
            raise ValueError("k should be >=0, <= n_features = %d; got %r. "
                             "Use k='all' to return all features."
                             % (X.shape[1], self.k))

    def _get_support_mask(self):
        check_is_fitted(self)

        if self.k == 'all':
            return np.ones(self.scores_.shape, dtype=bool)
        elif self.k == 0:
            return np.zeros(self.scores_.shape, dtype=bool)
        else:
            scores = _clean_nans(self.scores_)
            mask = np.zeros(scores.shape, dtype=bool)

            # Request a stable sort. Mergesort takes more memory (~40MB per
            # megafeature on x86-64).
            mask[np.argsort(scores, kind="mergesort")[-self.k:]] = 1
            return mask