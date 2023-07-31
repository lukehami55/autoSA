import pandas as pd
from tkinter import messagebox
from autoindex import createIndex
from calckpi import sum, calc


def autosa(params, index, desc_label):
    if index:
        desc_label.config(text="Running Auto SA with index")
    else:
        desc_label.config(text="Running Auto SA")

    """
    read data.csv and potential index.csv (create index if NA)
    """
    try:
        dataDf = pd.read_csv("C:/Users/LukeHamilton/SA/data.csv")
    except:
        desc_label.config(text="No data.csv file found in directory C:/Users/LukeHamilton/SA")

    if index:
        try:
            indexDf = pd.read_csv("C:/Users/LukeHamilton/SA/index.csv")
        except:
            desc_label.config(text="No index.csv file found in directory C:/Users/LukeHamilton/SA")
        indexDf = indexDf.drop_duplicates(subset=['Campaigns'])
    else:
        indexDf = createIndex(dataDf, params)

    """
    locate currency without user input
    currency needs to be extracted from datafile
    """
    headers = list(dataDf.columns.values)
    for i in range(len(headers)):
        if "Budget(" in headers[i]:
            country = headers[i].replace("Budget(", "").replace(")", "")
    spend = "Spend("+country+")"
    sales = "Sales("+country+")"

    """
    match and sort campaign values with corresponding indexfile values
    """
    for i in range(len(params)):
        if params[i] == "Total":
            dataDf['Total'] = "Total"
        elif params[i] == "Portfolio":
            indexDf['Portfolio'] = dataDf['Portfolio']
        else:
            dataDf[params[i]] = dataDf['Campaigns'].map(indexDf.set_index('Campaigns')[params[i]])

    """
    check and report any missing campaigns
    will only trigger if index is set to yes and compaigns are missing
    """
    missing_campaigns = dataDf[dataDf[params[i]].isna()]['Campaigns']
    if not missing_campaigns.empty:
        messagebox.showinfo("Popup", "Error")
        desc_label.config(text="Missing campaigns from index file")
    """
    assemble main table
    loop over parameters and find kpi values
    cleanup table - transpose, truncate decimals, add symbols
    """
    dataTable = pd.DataFrame()
    for i in range(len(params)):
        groupBy = params[:(i+1)]
        masterdf = pd.DataFrame()
        masterdf = sum('Impressions',dataDf,masterdf,groupBy)
        masterdf = calc(dataDf,masterdf,groupBy,"Clicks","Impressions","CTR",100)
        masterdf = sum('Clicks',dataDf,masterdf,groupBy)
        masterdf = calc(dataDf,masterdf, groupBy, spend, "Clicks", "CPC", 1)
        masterdf = sum('Orders',dataDf,masterdf,groupBy)
        masterdf = calc(dataDf,masterdf, groupBy, "Orders", "Clicks", "CVR", 100)
        masterdf = sum(spend,dataDf,masterdf,groupBy)
        masterdf = sum(sales,dataDf,masterdf,groupBy)
        masterdf = calc(dataDf, masterdf, groupBy, sales, spend, "ROAS", 1)
        masterdf = calc(dataDf, masterdf, groupBy, spend, "Orders", "CPP", 1)
        masterdf = masterdf.T
        dataTable = pd.concat([dataTable, masterdf])
    dataTable = dataTable.reindex(sorted(dataTable.index, key=lambda x: (not isinstance(x, tuple), x)))

    def ascendSales(x):
        vals = x.sort_values(by=sales, ascending=False)
        dataTable.loc[x.index] = vals.values

    """
    shift index
    define sort based on 3rd subcategory
    sort with ascend function
    re-shift index
    """
    dataTable.reset_index(inplace=True)
    m = dataTable['index'].apply(len).eq(3)
    dataTable[m].groupby(dataTable.loc[m, 'index'].str[1], group_keys=False).apply(ascendSales)
    dataTable.set_index('index', inplace=True)

    """
    formatting
    """
    dataTable[['CTR', 'CPC', 'ROAS', 'CPP']] = dataTable[['CTR', 'CPC', 'ROAS', 'CPP']].applymap(lambda x: format(x, '.2f')).astype(float)
    dataTable[['CVR']] = dataTable[['CVR']].applymap(lambda x: format(x, '.1f')).astype(float)
    dataTable[[spend, sales, 'Impressions', 'Clicks', 'Orders']] = dataTable[[spend, sales, 'Impressions', 'Clicks', 'Orders']].astype(int)
    dataTable = dataTable.applymap(lambda x: "{:,}".format(x))
    dataTable[['CTR', 'CVR']] = dataTable[['CTR', 'CVR']] + '%'
    dataTable.to_csv("C:/Users/LukeHamilton/SA/autosa.csv", encoding='Windows-1252')

    if index:
        desc_label.config(text="Ran Auto SA with index")
    else:
        desc_label.config(text="Ran Auto SA")
    return