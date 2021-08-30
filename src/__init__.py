from helper_functions import bonferroni_adjustment
from helper_functions import crosstab_chi2
from helper_functions import true_column_name

import pandas as pd

import statsmodels as sm
from statsmodels.stats.multitest import multipletests

from IPython.display import display, Math

if __name__ == "__main__":

    # Loading Data and true column names
    responses = pd.read_csv('archive/responses.csv')
    mydict = true_column_name()

    demographics = pd.DataFrame([responses.Age, 
                            responses.Height,
                            responses.Weight,
                            responses['Number of siblings'],
                            responses.Gender,
                            responses['Left - right handed'],
                            responses.Education,
                            responses['Only child'],
                            responses['Village - town'],
                            responses['House - block of flats']]).transpose()
    demographics = demographics.rename(columns = {"Education": "Highest Education Completed", 
                                              "Village - town": "Spend childhood in a ", 
                                              "House - block of flats": "Lived childhood in a"})

    # The Survey answers dataframe.
    preferences = pd.DataFrame([responses[x] for x in list(responses)[:140]]).transpose()
    preferences = preferences.rename(columns = mydict)

    # Generating seperate dataframes for any future hypothesis tests
    music = pd.DataFrame([preferences[x] for x in list(preferences)[:19]]).transpose()
    movies = pd.DataFrame([preferences[x] for x in list(preferences)[19:31]])
    hobbs_and_intrs = pd.DataFrame([preferences[x] for x in list(preferences)[31:63]])
    phobias = pd.DataFrame([preferences[x] for x in list(preferences)[63:73]]).transpose()
    health_habits = pd.DataFrame([preferences[x] for x in list(preferences)[73:76]])
    personality_views_opinions = pd.DataFrame([preferences[x] for x in list(preferences)[76:133]])
    spending_habits = pd.DataFrame([preferences[x] for x in list(preferences)[133:140]]).transpose()


    # Starting Phobias Hypothesis Testing
    phobias1 = phobias.copy()
    phobias1['Gender'] = demographics['Gender']
        # phobias1[['Flying', 'Gender']].sample(5)

    # Crosstabulation
    for column in phobias1:
        print(crosstab_chi2(phobias1.iloc[:, -1], phobias1[column], 0.05))

    # Bonferroni Corrected p-values and Rejection array
    bonferroni_adjustment(phobias1, 0.05)