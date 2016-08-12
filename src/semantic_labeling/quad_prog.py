from collections import defaultdict

import numpy as np
import pandas as pd
from cvxpy import Minimize
from cvxpy import Problem, quad_form
from cvxpy import Variable
from sklearn import manifold, mixture
from sklearn.cluster import DBSCAN


def multi_dim_scale(similarity_matrix):
    mds = manifold.MDS(n_components=2, max_iter=3000, dissimilarity="precomputed",
                       random_state=np.random.RandomState(seed=3),
                       n_jobs=1)

    coordinates = mds.fit_transform(similarity_matrix)
    return coordinates


def gmm_cluster(coordinate_matrix):
    dpgmm = mixture.DPGMM(n_components=2, covariance_type='full')
    dpgmm.fit(coordinate_matrix)
    prob_matrix = dpgmm.predict_proba(coordinate_matrix)
    return prob_matrix


def hierarchical_cluster(similarity_matrix):
    distance_matrix = [[1 - x for x in y] for y in similarity_matrix]
    dbscan = DBSCAN(metric="precomputed")
    clusters = dbscan.fit_predict(distance_matrix).tolist()
    encoded_matrix = []
    for value in set(clusters):
        encoded_matrix.append([1 if x == value else 0 for x in clusters])
    return np.asarray(encoded_matrix)


def prepare_parameters(coocurence_map, prediction_map):
    likelihood_df = pd.DataFrame(prediction_map).transpose()

    likelihood_df = pd.DataFrame(likelihood_df,
                                 columns=coocurence_map.columns.values.tolist())
    likelihood_df = likelihood_df.fillna(0)

    cooccurence_df = pd.DataFrame(coocurence_map, columns=likelihood_df.columns.values.tolist())

    type_names = likelihood_df.columns.values
    attr_names = list(likelihood_df.index)

    print type_names
    print likelihood_df

    num_attrs = len(prediction_map)
    num_types = len(cooccurence_df.columns.values.tolist())

    likelihood_matrix = likelihood_df.stack().values
    cooccurence_matrix = cooccurence_df.values.tolist()

    cooccurence_matrix = hierarchical_cluster(np.asarray(cooccurence_matrix))

    cooccurence_matrix = np.dot(cooccurence_matrix.transpose(), cooccurence_matrix)

    cooccurence_matrix = cooccurence_matrix.tolist()

    co_diagonal_matrix = [0] * (num_attrs * num_types)

    print num_types, num_attrs

    for j in range(num_attrs):
        for i in range(num_types):
            co_diagonal_matrix[j * num_types + i] = [0.0] * (j * num_types) + cooccurence_matrix[i] + [
                                                                                                          0.0] * num_types * (
                                                                                                          num_attrs - j - 1)
    sum_matrix = [0] * num_attrs

    for j in range(num_attrs):
        sum_matrix[j] = [0.] * (j * num_types) + [1.] * num_types + [0.] * num_types * (
            num_attrs - j - 1)

    return np.asarray(co_diagonal_matrix), likelihood_matrix.transpose(), np.asarray(
        sum_matrix), num_attrs, num_types, type_names, attr_names


def quad_prog(coocurence_map, prediction_map):
    P, q, A, num_attrs, num_types, types_name, attr_names = prepare_parameters(coocurence_map, prediction_map)

    G = np.identity(num_attrs * num_types)

    x = Variable(num_attrs * num_types)
    objective = Minimize(quad_form(x, P) + q * x)

    constraint = [G * x >= 0, A * x == 1]

    Problem(objective, constraint).solve()

    result_matrix = x.value.reshape(num_types, num_attrs).transpose().tolist()

    prediction_map = defaultdict(lambda: {})

    for idx1 in range(len(result_matrix)):
        for idx2 in range(len(result_matrix[0])):
            prediction_map[attr_names[idx1]][types_name[idx2]] = result_matrix[idx1][idx2]

    return prediction_map
