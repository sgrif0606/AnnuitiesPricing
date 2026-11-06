import pandas as pd

pd.set_option('display.max_rows', None)     # Print every single row
pd.set_option('display.max_columns', None)  # Print every single column
pd.set_option('display.width', None)

def read_excel_file(cols) -> pd.DataFrame:
    return pd.read_excel(
        io='data/nltuk198020223.xlsx',
        sheet_name='2022-2024',
        usecols=cols,
        skiprows=6,
        header=0,
        nrows=101,
        names=["age", "mx", "qx", "lx", "dx", "ex"]
    )

def annuity_value(a, i, df):
    #Generating the probability of someone living t more years and adding to the dataframe
    df['px'] = (df.loc[a:, 'lx'] / df['lx'].iloc[a])
    df['px'] = df['px'].fillna(0)

    #Generating another column, which will be the annuity per year
    df['annuity_yearly'] = df['px'] * pow(1 / (1 + i), df['age'] - a)

    #Calculating total annuity
    total_annuity = sum(df['annuity_yearly'])

    return df, total_annuity

if __name__ == '__main__':
    dataframe = read_excel_file('A:F') if input("M/F?:").lower() == "m" else read_excel_file('H:M')
    age = int(input("Enter age: "))
    annual_payment = float(input("Enter annual payment: £"))
    interest = float(input("Enter interest rate(%): "))/100
    inflation = float(input("Enter inflation(%): ")) / 100
    dataframe, annuity_price = annuity_value(age, (interest - inflation) / (1 - inflation), dataframe)

    print(f"Annuity price is: £{annuity_price*annual_payment:.2f}")
    input()
    print(dataframe)