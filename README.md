**METHOD**
I used Python Pandas in order to read the data in the xlsx file into a DataFrame, to which I could add columns for my calculated values of all px(probability of someone aged x surviving until at least age t), and then expected payment per year based on this.
The calculator allows for the user to enter their age, their desired annual payment as well as the interest and inflation rates, and will then output the total expected cost of the annuity, which is the sum of the expected yearly payments.


**EXTRAPOLATION**
The dataset provided by ONS only contained entries for participants up to 100 years old, so just using this would cause my calculations to be a slight underestimate of the official annuity price.
To remedy this, I observed that the mortality rate and age follow a log-linear relationship for ages above ~60 (which is the Gompertz Law of Mortality). This is pictured for males and females in the mortality rate plots.
This allowed me to find polynomial coefficients of the line of best fit, and then use those to create a function for mx based on the age.
I could then use the methods described by ONS to generate extrapolated data for ages above 100, relying on my value of mx.
For completeness, I also then generated values for life expectancy at each age, since this could not be done using solely the mx, and compared it to my data.

View example data for a 60 year old female wanting £10,000 per year at 4% interest and 3% inflation [here](ExampleDataF.csv) (the total cost of this annuity is £1058879.62).

Annuity cost is: £1,037,777.62

**DATA VISUALISATIONS**
<details>
  <summary>
    Scatter plot showing log-linear relationship between mx and age for females over 60
  </summary>
  
  ![](FemaleMortalityPlot.png?raw=True)
</details>
<details>
  <summary>
    Scatter plot showing log-linear relationship between mx and age for males over 60
  </summary>
  
  ![](MaleMortalityPlot.png?raw=True)
</details>
