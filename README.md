# Gender vs Fear
Galvanize Capstone Project: Gender vs Fear 

## Objective
The objecive of this project is to find out if a key demographic of an individual has predictive power. To do this we want to see if a person's gender has a statistical signficance on their phobias. This is accomplished using Chi-Squared Hypothesis Testing. 

## Potential Use-Cases
Finding if/which key demographics have influence over an individual's preferences, opinions, habits, or even fears can be used in advertising. It can also help make certain products more targeted. For example, editing a horror film during post-production to target a certain demographic.

## Data
We will be running a hypothesis test on the [Young People Survey](https://www.kaggle.com/miroslavsabo/young-people-survey?select=responses.csv) dataset which was made available on kaggle. The survey was done by participants found by members of a statistics class from a University in Slovakia. The survey was translated from Slovak into English, and contained over 1000 participants, ages 15 - 30. It was submitted in both electronic and written form. 

The dataset itself contains over 100 columns but for the purposes of the project, I only needed the columns related to Demographics and Phobias. The methodology exhibited in this repo can easily extend to the other topics.

## Data-Cleaning
Since the amount of null values in some columns were at most only 2%, I ended up dropping those entries. It was a long survey so any presence of null values I figured was due to human-error such as skipping a question or data-loss from transferring the electronic or written records.

I also made a subset of the dataframe built from the survey so I can extract certain feature columns more easily and conduct seperate hypothesis tests more efficiently. 

## Feature Selection
The features I chose for the hypothesis test were Gender and Phobias. 

Even though Age is a common demographic to test hypotheses against, I didn't think it would be prudent in this case because the distribution of different ages were not balanced enough. Since the survey was distributed by students to people they know, the vast majority of participants grouped near the mean average of 20. There are so few participants aged near 15 or 30 for example, that it would be unfair to attribute any conclusions to those underrepresented age groups.

_ |_
:-------------------------:|:-------------------------:
![Imgur](https://i.imgur.com/O33bAmX.png) | ![Imgur](https://i.imgur.com/9QKhE8B.png)

The representation between the unique groups in Gender however were similar enough that investigation was actionable. So to keep it simple we will be using Gender vs a list of phobias to test our hypothesis.

![Imgur](https://i.imgur.com/8zgInip.png)

This is a excerpt of the final clean data that is being used. The survey was done using a Likert Scale where each row are a person’s responses. 
For Phobias 1 is (Not afraid at all) and 5 is (Very afraid).

![Imgur](https://i.imgur.com/0w8HGA2.png)

So our process will be to check for independence of Gender to each of the column-phobias.

## Methodology
### Hypothesis Testing
We will tackle our objective by doing a hypothesis test between Gender and Phobias.

###### Null Hypothesis:
```math   
H_0 : Phobias are independent of a person's Gender.
```    

###### Alternate Hypothesis:
```math
H_1 : Phobias and Gender are not independent and there exists a relationship between them.
```

### Chi-Squared Test
Since we are dealing with categorical data, to achieve this, we will be using the chi-squared test of independence with a significance level of 0.05. 

<!-- 
$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$

$\alpha = 0.05 $  -->
![Imgur](https://i.imgur.com/k6rPvFF.png)


### Bonferroni Corrected p-value

<!-- $Bonferroni \ corrected \ p-value = \frac{p_0}{n}$

$$where: \ \ \ \ p_0 = original \ p-value$$ 
$$n = \# \ of \ tests \ performed$$ 
 -->
![Imgur](https://i.imgur.com/3tsAhJA.png)

Since we are comparing multiple categories against each other, the rate of a possible Type 1 Error compound on each test. 

This means our first test at an alpha of .05 has a 5% chance of a false positive. The test after would compound to 10% and so on, with each test increasing our error rate by 5%. 

To make sure this doesn’t get out of hand, we will use the Bonferroni-adjusted method that adjusts the p-value by how many comparisons are being conducted. The formula is given here where p-zero is the original p-value and n is the # of tests performed. 

## Analysis
The first chi-squared test will focus on the Gender column and the Fear of Flying category.

To begin the test we need to start with a cross tabulation between the Gender Column demographic and the Fear of Flying category. 

_ |_
:-------------------------:|:-------------------------:
![Imgur](https://i.imgur.com/IfMXRxj.png) |![Imgur](https://i.imgur.com/eqLbPEA.png)

This graph shows the number of Males and Females that picked each Likert scale choice for Fear of Flying, where 1 is not afraid at all, and 5 is very afraid. 
 
Now with that visual in mind, we use the `crosstab_chi2` function that does the cross tabulation and the chi-squared in tandem.


```python
def crosstab_chi2(index, columns, alpha_signif):
    ''' The function will return the chi-squared test statistic, associated p-value,
        degrees of freedom, and the expected freq array.
        
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

    (chi2_test_stat, p_val, dof, expec_freq_arr) = stats.chi2_contingency(crosstab)

    return (chi2_test_stat, p_val, dof, expec_freq_arr) 
```  

From it, one of our returns is the p-value. We can see our p-value is less than our alpha. However we cannot reject the null hypothesis yet without computing the Bonferroni Correction.

Since the Bonferroni Correction penalizes the testing process as a whole we need to first do the other multiple hypotheses.

Using the `bonferroni_adjustment` function; what we did to Fear of Flying we’ll do to every other phobia with the addition of getting the bonferroni-adjustment.

```python
def bonferroni_adjustment(dataframe, alpha_sig):
    ''' The function will return the Bonferroni-Corrected p-values for multiple tests,
    the corrected alpha for the Bonferroni method, and the boolean for if a hypothesis 
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
    
    
    
    (reject_arr, pval_corrected, alphaC_sidak, 
     alphaC_bonf) = sm.stats.multitest.multipletests(p_val_arr,
                                                     alpha=0.05, 
                                                     method='bonferroni', 
                                                     is_sorted=False, 
                                                     returnsorted=False)
    print(reject_arr, pval_corrected, alphaC_bonf)

```

## Results
The results of the Bonferroni Correction are shown in the table below:


|  Original Alpha | Corrected Alpha for Bonferroni method |
| :---: | :---: |
| 0.05 | 0.004545454545454546 |

| Gender vs Phobia | Original p-val | Bonferroni Corrected p-val| Reject Null? |
| :---: | :---: | :---: | :---: |
| Flying             | 7.208e-04  | 7.93e-03 | True |
| Thunder, Lightning | 4.6241𝑒−22 | 5.09e-21 | True |
| Darkness           | 9.9074𝑒−23 | 1.09e-21 | True |
| Heights            | 0.0989     | 1.0      | False|
| Spiders            | 6.432𝑒−24  | 7.08e-23 | True |
| Snakes             | 1.531𝑒−11  | 1.68e-10 | True |
| Rats, Mice         | 2.724𝑒−15  | 2.99e-14 | True |
| Ageing             | 1.289𝑒−05  | 1.42e-04 | True |
| Dangerous Dogs     | 6.972𝑒−10  | 7.67e-09 | True |
| Public Speaking    | 2.502e-04  | 2.75e-03 | True |


As we can see from the right-most column, after the correction, out of all the phobias, the only null hypothesis we fail to reject is related to the Fear of Heights. 

That is to say, every other phobia is somehow dependent on a person’s gender. 

And for height, we fail to reject that a person’s Fear of Heights is independent of their gender.

## Conclusions / Future-Steps
Out of 10 different phobias surveyed, 9 of them show us that there is a relationship between a person’s gender and their phobias. 
<!-- 
Future Steps - Would be to go back to the beginning and impute those 2% of missing values I dropped and see if there is a significant difference. 

Post-Hoc Testing- Pair-wise comparisons. 
To see which gender is more afraid of those phobias and where the relationship is between the levels of the variables. -->
