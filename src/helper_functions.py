# Boilerplate
import pandas as pd

from scipy import stats
import statsmodels as sm

import csv
from IPython.display import display, Math


def true_column_name(filename = 'archive/columns.csv'):
    '''
    The original variable names were shortened in the responses.csv file. The shortened-unshortened name pairs are in the 
    columns.csv file.

    `true_column_name` is a function that returns a dictionary that can be used to convert the shortened column names back to their
    original names.

    Parameters
    ----------
    filename : str, optional
        File path of the columns.csv file. 
        by default 'archive/columns.csv'

    Returns
    -------
    mydict : dictionary
        A dictionary where the keys are the data's shortened column names and the values are the orginal, more descriptive 
        names from the survey.
    '''
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        with open('archive/columns_dict.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[1]:rows[0] for rows in reader}
    
    return mydict

def crosstab_chi2(index, columns, alpha_signif):
    ''' The function will return the chi-squared test statistic, associated p-value,
        degrees of freedom, and the expected freq array given an independent column and potential dependent columns.
        
    Parameters
    -----------
    index : Column 1 of dataframe that is not subject to change. i.e : Gender
    
    columns : Column 2 of dataframe that you want to check if dependent on index.
    
    alpha_signif : The chosen level of signficance to keep in mind.
    
    Returns
    --------
    Tuple(chi2_test_stat, p_val, dof, expec_freq_arr)
    
    '''
    
    crosstab = pd.crosstab(index, columns)
    #display(crosstab) #optional

    (chi2_test_stat, p_val, dof, expec_freq_arr) = stats.chi2_contingency(crosstab)

    return (chi2_test_stat, p_val, dof, expec_freq_arr) 


def bonferroni_adjustment(dataframe, alpha_sig):
    ''' The function will return the Bonferroni-Corrected p-values for multiple tests,
    the corrected alpha for the Bonferroni method, and a boolean for if a hypothesis 
    can be rejected given alpha.
    
    Parameters
    -----------
    dataframe : A data frame with columns[:len(df-1)] of variables you want to test
    versus the last column[:-1].
    alpha_sig : The chosen level of significance.
    
    Returns
    --------
    reject_arr : an array of bool for the hypotheses that can be rejected given alpha
    
    pval_corrected : an array of p-values corrected for multiple tests
    
    alphaC_bonf : corrected alpha for Bonferroni method
    '''
    
    p_val_arr = []
    reject_arr = []
    
    for column in dataframe:
        (chi2_test_stat, p_val, dof, expec_freq_arr) = crosstab_chi2(dataframe.iloc[:, -1], dataframe[column], 0.05)
        p_val_arr.append(p_val)
    
    
    (reject_arr, pval_corrected, alphaC_sidak, alphaC_bonf) = sm.stats.multitest.multipletests(p_val_arr,
                                                                                                alpha=0.05, 
                                                                                                method='bonferroni', 
                                                                                                is_sorted=False, 
                                                                                                returnsorted=False)
    print(reject_arr, pval_corrected, alphaC_bonf)
 
