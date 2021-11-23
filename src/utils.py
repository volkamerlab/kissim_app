"""
Utitlity functions.
"""

import numpy as np


def check_distance_matrix(matrix):
    """
    Check conditions for distance matrix.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.
    """
    print(f"{'Matrix 2D and square?:' : <30}{_check_dimensionality(matrix)}")
    print(f"{'Matrix positive?:' : <30}{_check_positivity(matrix)}")
    print(f"{'Matrix diagonale 0?:' : <30}{_check_null_diagonal(matrix)}")
    print(f"{'Matrix symmetric?:' : <30}{_check_symmetry(matrix)}")
    print(f"{'Triangular inequality?:' : <30}{_check_triangular_inequality(matrix)}")


def _check_dimensionality(matrix):
    """
    Checks whether the input is a 2D array (matrix) and square.
    By @t-kimber.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.

    Returns
    -------
    bool :
        True if the condition is met, False otherwise.
    """
    if len(matrix.shape) != 2:
        raise ValueError(f"The input is not a matrix, but an array of shape {matrix.shape}.")
    elif matrix.shape[0] != matrix.shape[1]:
        raise ValueError("The input is not a square matrix. Failing.")
    else:
        return True


def _check_positivity(matrix):
    """
    Checks whether all values of a matrix are positive.
    By @t-kimber.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.

    Returns
    -------
    bool :
        True if the condition is met, False otherwise.
    """
    return (matrix >= 0).all()


def _check_null_diagonal(matrix):
    """
    Checks whether the diagonal entries of a matrix are all zero.
    By @t-kimber.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.

    Returns
    -------
    bool :
        True if the condition is met, False otherwise.
    """
    return (np.diagonal(matrix) == 0).all()


def _check_symmetry(matrix):
    """
    Checks whether a matrix M is symmetric, i.e. M = M^T.
    By @t-kimber.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.

    Returns
    -------
    bool :
        True if the condition is met, False otherwise.
    """
    return (matrix == matrix.transpose()).all()


def _check_triangular_inequality(matrix, tolerance=0.11):
    """
    Checks whether the triangular inequality is met for a matrix,
    i.e. the shortest distance between two points is the straight line.
    By @t-kimber.

    Parameters
    ----------
    matrix : np.array
        The matrix for which the condition should be checked.
    tolerance : float
        The accepted tolerance for approximation.

    Returns
    -------
    bool :
        True if the condition is met, False otherwise.
    """
    triang_inequality = None
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            for k in range(matrix.shape[0]):
                if matrix[i, j] <= matrix[i, k] + matrix[k, j] + tolerance:
                    triang_inequality = True
                else:
                    return False
    return triang_inequality
