import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

l1_data = pd.read_csv('l1-daily-gas.csv')
l2_data = pd.read_csv('l2-daily-gas.csv')

l1_data = l1_data.loc[l1_data['UnixTimeStamp'] >= 1592179200]
l2_data = l2_data.iloc[::-1]

l1_data['date'] = pd.to_datetime(l1_data['Date(UTC)'])
l2_data['date'] = pd.to_datetime(l2_data['dt'])
l1_data['date'] = l1_data['date'].apply(pd.to_datetime, utc=True)

df3 = pd.concat([l1_data.set_index('date'), l2_data.set_index(
    'date')], axis=1, join='inner').reset_index()

combined_data = pd.DataFrame()

combined_data['date'] = df3['date']
combined_data['l1-gas-use'] = df3['Value']
combined_data['l2-gas-use'] = df3['daily_gas_used']

print(combined_data)

# =============== visualise data =========================
visualise = False

if(visualise):
    # entire dataset from 2020
    x = combined_data['l2-gas-use']
    y = combined_data['l1-gas-use']

    line1 = plt.scatter(x, y, label="15-06-2020")
    # plt.show()

    # use data only from mid 2021
    new_data = combined_data.loc[combined_data['date'] >= '2021-06-01']

    x = new_data['l2-gas-use']
    y = new_data['l1-gas-use']

    line2 = plt.scatter(x, y, label="01-06-2021")

    # use data only from 2022
    new_data = combined_data.loc[combined_data['date'] >= '2022-01-01']

    x = new_data['l2-gas-use']
    y = new_data['l1-gas-use']

    line3 = plt.scatter(x, y, label="01-01-2022")
    plt.xlabel("L2 gas usage", fontsize=14)
    plt.ylabel("L1 gas usage", fontsize=14)
    plt.legend([line1, line2, line3], ["15-06-2020 onwards",
                                       "01-06-2021 onwards", "01-01-2022 onwards"], fontsize=14)
    plt.show()

# ========= regression ===============
plot1 = False
if(plot1):
    regr = LinearRegression()

    new_data = combined_data.loc[combined_data['date'] >= '2020-06-15']

    x = new_data['l2-gas-use']
    y = new_data['l1-gas-use']
    x = x.to_numpy().reshape(-1, 1)

    regr.fit(x, y)
    y_pred = regr.predict(x)

    line4 = plt.scatter(x, y, label="15-06-2020")
    plt.xlabel("L2 gas usage", fontsize=14)
    plt.ylabel("L1 gas usage", fontsize=14)
    plt.plot(x, y_pred)
    plt.legend([line4], ["15-06-2020 onwards"])
    plt.show()

    # add constant to predictor variables
    x = sm.add_constant(x)

    # fit linear regression model
    model = sm.OLS(y, x).fit()
    print(model.summary())

plot2 = False
if(plot1):
    regr = LinearRegression()

    new_data = combined_data.loc[combined_data['date'] >= '2021-06-01']

    x = new_data['l2-gas-use']
    y = new_data['l1-gas-use']
    x = x.to_numpy().reshape(-1, 1)

    regr.fit(x, y)
    y_pred = regr.predict(x)

    line4 = plt.scatter(x, y, label="01-06-2021")
    plt.xlabel("L2 gas usage", fontsize=14)
    plt.ylabel("L1 gas usage", fontsize=14)
    plt.plot(x, y_pred)
    plt.legend([line4], ["01-06-2021 onwards"])
    plt.show()

    # add constant to predictor variables
    x = sm.add_constant(x)

    # fit linear regression model
    model = sm.OLS(y, x).fit()
    print(model.summary())

plot3 = False
if(plot3):
    regr = LinearRegression()

    new_data = combined_data.loc[combined_data['date'] >= '2022-01-01']

    x = new_data['l2-gas-use']
    y = new_data['l1-gas-use']
    x = x.to_numpy().reshape(-1, 1)

    regr.fit(x, y)
    y_pred = regr.predict(x)

    line4 = plt.scatter(x, y, label="01-01-2022")
    plt.xlabel("L2 gas usage", fontsize=14)
    plt.ylabel("L1 gas usage", fontsize=14)
    plt.plot(x, y_pred)
    plt.legend([line4], ["01-01-2022 onwards"])
    plt.show()

    # add constant to predictor variables
    x = sm.add_constant(x)

    # fit linear regression model
    model = sm.OLS(y, x).fit()
    print(model.summary())

plot4 = True
if(plot4):
    regr = LinearRegression()

    new_data = combined_data.loc[combined_data['date'] >= '2022-01-01']

    x1 = new_data['l2-gas-use']
    x2 = new_data['l1-gas-use']
    date = new_data['date']
    x1 = x1.to_numpy().reshape(-1, 1)
    x2 = x2.to_numpy().reshape(-1, 1)

    #regr.fit(x, y)
    #y_pred = regr.predict(x)

    ax1 = plt.subplot()
    line4 = ax1.plot(date, x2, label="L1 Gas Usage")
    ax2 = ax1.twinx()
    line5 = ax2.plot(date, x1, color="orange", label="L2 Gas Usage")
    plt.xlabel("L2 gas usage", fontsize=14)
    ax1.set_ylabel("L1 gas usage", fontsize=14)
    ax2.set_ylabel("L2 gas usage", fontsize=14)

    # added these three lines
    lns = line4+line5
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    #plt.plot(x, y_pred)
    #plt.legend([line4, line5], ["L1 Gas Usage", "L2 Gas Usage"])
    plt.show()

    # add constant to predictor variables
    #x = sm.add_constant(x)

    # fit linear regression model
    #model = sm.OLS(y, x).fit()
    print(model.summary())

plot5 = False
if(plot5):
    delta_days = 7  # number of days to lag

    regr = LinearRegression()

    new_data = combined_data.loc[combined_data['date'] >= '2022-01-01']

    new_data['l2-gas-use(t-1)'] = new_data['l2-gas-use'].shift(delta_days)
    new_data = new_data.iloc[delta_days:]
    new_data['l2_delta'] = new_data['l2-gas-use'] - new_data['l2-gas-use(t-1)']

    new_data['l1-gas-use(t-1)'] = new_data['l1-gas-use'].shift(delta_days)
    new_data = new_data.iloc[delta_days:]
    new_data['l1_delta'] = new_data['l1-gas-use'] - new_data['l1-gas-use(t-1)']
    print(new_data)

    x = new_data['l2_delta'].to_numpy().reshape(-1, 1)
    y = new_data['l1_delta']

    regr.fit(x, y)
    y_pred = regr.predict(x)

    line4 = plt.scatter(x, y, label="01-01-2022")
    plt.xlabel("Weekly change in L2 gas usage", fontsize=14)
    plt.ylabel("Weekly change in L1 gas usage", fontsize=14)
    plt.plot(x, y_pred)
    plt.legend([line4], ["01-01-2022 onwards"])
    plt.show()

    model = sm.OLS(y, x).fit()
    print("WEEKLY MODEL SUMMARY")
    print(model.summary())
