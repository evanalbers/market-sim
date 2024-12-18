"""
Author: Evan Albers
Version Date: 29 December 2022
Summary: series of functions to aid with portfolio calculation, to isolate
         and help with debugging

         Notes: 

         - portfolio weights should be stored as a 2d array, 1st row is
         the ticker of the asset, 2nd is the weight in the portfolio, 
         can be negative, allowing for short selling

         - should store tickers in alphabetical order, keep it consistent
         They will be mapped to floats on such a basis, very important to
         avoid confusion


"""

import json
from maxe.simulation import numpy as np
from numpy.linalg import inv


def getExpPriceData(tickers, file):
    """
    Returns the expected price data associated with the given tickers 
    as a numpy array

    Parameters
    ----------
    tickers : list
        a list of numbers representing the index of sought after assets

    file : string
        file containing mean-variance data about assets

    Returns
    -------
    exp_rets : nparray
        an array of the corresponding expected returns    
    """

    with open(file) as f:

        data = json.load(f)
    
    all_prices = data["exp_prices"]

    # retrieve indices of tickers, append returns to list
    exp_price = []
    for t in tickers:
        exp_price.append(all_prices[t])

    return np.asarray(exp_price)
    
def getRiskMatrix(tickers, file):
    """
    returns the risk matrix for given tickers
    
    Parameters
    ----------
    tickers : list
        list of ints representing indices of sought after assets

    file : string
        file containing mean-variance data about assets
    
    Returns
    -------
    risk_matrix : nparray
        array of arrays, representing the variances, covariances of assets 
        detailed in ticker
    """

    # retrieving data
    with open(file) as f:

        data = json.load(f)

    all_asset_risk = data["variances"]
    matrix = []

    # subsetting overarching matrix
    for i in tickers:
        row = []
        for j in tickers:
            row.append(all_asset_risk[i][j])
        matrix.append(row)
    
    risk_matrix = np.array(matrix)

    return risk_matrix



def getExpRetData(tickers, current_price_data, file):
    """Returns the expected return data associated with the given tickers 
    as a numpy array

    Parameters
    ----------
    tickers : list
        a list of tickers sorted in alphabetical order

    current_price_data : list
        a list of numbers corresponding to sorted ticker order representing price data

    file : string
        file containing mean-variance data about assets

    Returns
    -------
    exp_rets : nparray
        an array of the corresponding expected returns """
    
    exp_prices = getExpPriceData(tickers, file)

    exp_returns = [0] * len(exp_prices)

    ## dividing exp price at end of period by current price 
    for num in range(len(exp_prices)):
        exp_returns[num] = exp_prices[num] / current_price_data[num]

    return np.array(exp_returns)

def calculate_expected_return(tickers, weights, current_prices, file):
    """
    Returns the expected return of the given portfolio weights

    Parameters
    ----------
    tickers : list of strings
        list of the tickers in the portfolio
    
    weights : nparray
        a 2D array in which the first row is the tickers, 2nd row is
        corresponding weight in the portfolio

    current_prices : list of floats
        current prices of each security in the portfolio

    file : string
        file containing mean-variance data about assets
    
    Returns
    -------
    expected return : float
        float representing the expected return of the portfolio
    """

    ## need to add a bit calculating the expected return here, should be just dividing elements in 
    ## the given current price by those in the expected price one, given by exp. price function

    exp_return_data = getExpRetData(tickers, current_prices, file)

    expected_return = np.matmul(np.array(weights).T, exp_return_data)

    return expected_return


def calculate_optimal_portfolio(tickers, rfr, current_price_data, file):
    """
    Returns a set of weights that represent the optimal portfolio weights for 
    the given asset

    Parameters
    ----------
    tickers : array of floats 
        representing the tickers to be assessed
    
    rfr : float
        the risk free rate
    
    current_price_data : list of floats 
        ordered list of current price data of assets in tickers

    file : string
        filename to be opened, contains risk and return data

    Returns 
    -------
    weights : nparray
        a 2D array in which the first row is the tickers, 2nd row is
        corresponding weight in the portfolio
    """

    risk_matrix = getRiskMatrix(tickers, file)

    exp_return_data = getExpRetData(tickers, current_price_data, file)

    risk_free_vec = np.ones(exp_return_data.shape) * rfr

    numerator = np.matmul(inv(risk_matrix),(exp_return_data - risk_free_vec))

    denom = np.matmul(np.ones(risk_matrix.shape[0]).T, np.matmul(inv(risk_matrix),(exp_return_data - risk_free_vec)))

    t = numerator / denom

    return t

def calcPortfolioRisk(tickers, weights, file):
    """ calculates the risk of a given portfolio
    
    Parameters
    ----------
    tickers : list of strings
        list of tickers of assets in portfolio

    weights : list of floats
        the corresponding weights of each asset in the portfolio

    Returns
    -------
    risk : float
        the risk of the portfolio    
    """

    risk_matrix = getRiskMatrix(tickers, file)

    risk = np.matmul(np.matmul(np.array(weights).T, risk_matrix), np.array(weights))

    return risk

def calculate_current_weights(current_price_data, shares):
    """ calculate the current weights of a given portfolio 
    
    Parameters
    ----------
    current_price_data : list
        list of current prices of stocks owned in portfolio

    shares : list
        list of number of shares held in corresponding index

    Returns
    -------
    curr_weights : list
        the current weight of each asset in submitted portfolio  

    """

    curr_weights = []
    total_value = 0

    for num in range(len(current_price_data)):
        total_value += current_price_data[num] * shares[num]

    for num in range(len(current_price_data)):

        if shares[num] > 0:
            curr_weights.append((current_price_data[num] * shares[num]) / total_value)
        else:
            curr_weights.append(0)
    
    return curr_weights

