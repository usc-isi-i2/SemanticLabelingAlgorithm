from cvxopt import solvers
from cvxopt.base import matrix, spmatrix

# P = 2 * matrix([[0.2, 0.3, 0.5, 0, 0, 0], [0.4, 0.5, 0.1, 0, 0, 0], [0.1, 0.3, 0.2, 0, 0, 0], [0, 0, 0, 0.2, 0.3, 0.5],
#                 [0, 0, 0, 0.4, 0.5, 0.1], [0, 0, 0, 0.1, 0.3, 0.2]])
# q = matrix([0.1, 0.6, 0.7, 0.3, 0.8, 0.2])
# G = spmatrix(-1.0, range(6), range(6))
# h = matrix([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
# A = matrix([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
# b = matrix([1.0, 1.0])
#
# sol = solvers.qp(P, q, G=G, h=h, A=A, b=b)
#
# print sol['x']
