from enum import Enum
import numpy as np
import scipy as sp
import pandas as pd
def computeNoi(rent, expenseRate=35):
    """ compute net operating income"""
    return rent *12 *(100-expenseRate)/100.
def computeCap(rent, price, expenses=35):
    """
    rent - monthly price
    price
    
    expenses ; 0 to 100 for a rate, otherwise dollar ammount
    return cap rate [%]
    """
    if expenses<100:
        return computeNoi(rent,expenses)/price * 100
    else:
        return (rent-expenses)/price * 100
def computeRoi(rent, price,Ltv,loanRatePer,expenses=.35):
    """
    rent per month
    price     
    ltv loan to value [decimal value]
    loan rate [percentage]
    """
    roi = rent * 12 *(1-expenses) - loanAmount *loanRatePer/100.
    roi = roi/((1-Ltv)*price)
    return roi * 100
def computeDebtServiceIO(price,ltv,loanRatePer):
    """compute debt service interest only for first year"""
    return price * ltv * loanRatePer/100.

def setMonthlyAndAnnual(dfAct:pd.DataFrame):
    """set monthtly and annual based on xor of montly,annual """
    for idx,row in dfAct[~dfAct["Monthly"].isna() ^ ~dfAct["Annual"].isna()].iterrows():
        if np.isnan(row["Monthly"]): dfAct.loc[idx,"Monthly"] = dfAct.loc[idx,"Annual"]/12.
        if np.isnan(row["Annual"]):  dfAct.loc[idx,"Annual"]  = dfAct.loc[idx,"Monthly"]*12.
    return dfAct

class LoanPaymentType(Enum):
    Interest = 0
    Principial=1
    Payment   = 2
def computePmt(df : pd.DataFrame,year=1,ptype=LoanPaymentType.Payment):
    """ 
    compute payment at particular times and types
    dataframe for actual data
    """
    ppmt= np.ppmt(
        df.loc["Loan Rate","%"]/100/12.,(year-1)*12+1,
        360,df.loc["Purchase Price","Value"] *df.loc["LTV","%"]/100)
    ipmt = np.ipmt(
        df.loc["Loan Rate","%"]/100/12.,(year-1)*12+1,
        360,df.loc["Purchase Price","Value"] *df.loc["LTV","%"]/100)
    
    if   ptype == LoanPaymentType.Interest:   return ipmt
    elif ptype == LoanPaymentType.Principial: return ppmt
    elif ptype == LoanPaymentType.Payment: return ipmt+ppmt
    else: assert(0,"illegal payment type")