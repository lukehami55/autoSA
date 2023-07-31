import pandas as pd


def sum(kpi,df,masterdf,groupBy):
    try:
        sumdf = df.groupby(groupBy)[kpi].sum().astype(int)
    except:
        sumdf = df[kpi].sum().astype(int)
    masterdf = masterdf.append(sumdf)
    #masterdf = pd.concat([masterdf,sumdf])
    return masterdf


def calc(df,masterdf,groupBy,num,denom,name,mult):
    try:
        calcdf = mult*df.groupby(groupBy)[num].sum().div(df.groupby(groupBy)[denom].sum())
    except:
        calcdf = mult*df[num].sum().div(df[denom].sum())
    calcdf = calcdf.rename(name)
    masterdf = masterdf.append(calcdf)
    #masterdf = pd.concat([masterdf, calcdf])
    return masterdf