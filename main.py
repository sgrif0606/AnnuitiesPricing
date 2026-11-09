import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.display.float_format = '{:.7f}'.format
pd.options.display.float_format = lambda x: f'{x:.7f}'.rstrip('0').rstrip('.')

def read_excel_file(cols) -> pd.DataFrame:
    #First reducing the sheet to only the relevant data for the query was the simplest way to begin.
    return pd.read_excel(
        io='data/nltuk198020223.xlsx',
        sheet_name='2022-2024',
        usecols=cols,
        skiprows=5,
        header=0,
        nrows=101,
        names=["age", "mx", "qx", "lx", "dx", "ex"]
    )

def extrapolate(df):

    #Finding polynomial coefficients that determine the line of best fit illustrated in the plot
    over60 = df[df['age'] >= 60]
    a, b = np.polyfit(over60['age'], np.log10(over60['mx']), 1)

    # Apart from life expectancy, the rest of the extrapolated data can be worked out with the formulas provided in the methodology, using only the previous data and current row.
    while df.iloc[-1]['lx'] > 0.1:
        last_row = df.iloc[-1]

        age = last_row['age'] + 1
        mx = 10**(a*age + b)
        qx = 2*mx/(2+mx)
        lx = last_row['lx'] - last_row['dx']
        dx = lx * qx

        df = pd.concat([df, pd.DataFrame(
            {'age': [age], 'mx': [mx], 'qx': [qx], 'lx': [lx], 'dx': [dx]},
            index=[age]
        )])

    #Now calculating life expectancy using the data already extrapolated
    ages = df.index
    years_lived = [(df.loc[i, 'lx'] + df.loc[i + 1, 'lx']) / 2 for i in ages[:-1]]
    years_lived.append(df.loc[ages[-1], 'lx'] / 2)  # Final age, due to the cutoff for the rest of the data, we will assume noone is alive at the end of this year

    total_years_lived = np.cumsum(years_lived[::-1])[::-1]
    df['ex_calc'] = total_years_lived / df['lx'].values
    return df

def annuity_value(a, i, df):
    #Generating the probability of someone living until the cutoff calculated in the sheet and adding to the dataframe
    df['px'] = df.loc[a:, 'lx'] / df['lx'].iloc[a]
    df['px'] = df['px'].fillna(0)

    #Generating another column, which will be the annuity per year
    df['expected_payment'] = df['px'] * pow(1 / (1 + i), df['age'] - a)

    #Calculating total annuity
    total_annuity = sum(df['expected_payment'])

    return df, total_annuity

if __name__ == '__main__':
    dataframe = read_excel_file('A:F') if input("M/F?:").lower() == "m" else read_excel_file('H:M')
    dataframe = extrapolate(dataframe)

    age = int(input("Enter age: "))
    annual_payment = float(input("Enter annual payment: £"))
    interest = float(input("Enter interest rate(%): "))/100
    inflation = float(input("Enter inflation(%): ")) / 100

    dataframe, annuity_price = annuity_value(age, (interest - inflation) / (1 - inflation), dataframe)
    print(f"Annuity price is: £{annuity_price*annual_payment:.2f}")
    input()
    print(dataframe)