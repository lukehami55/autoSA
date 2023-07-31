def defineTargeting(index):
    targetList = []
    for j in range(len(index)):
        if "Views Retargeting" in index['Campaigns'].iloc[j]:
            targetList.append("Views Retargeting")
            continue
        elif "Purchases Retargeting" in index['Campaigns'].iloc[j]:
            targetList.append("Purchases Retargeting")
            continue
        elif "Auto" in index['Campaigns'].iloc[j]:
            targetList.append("Auto")
            continue
        elif "Competitor" in index['Campaigns'].iloc[j]:
            targetList.append("Competitor")
            continue
        elif "Category" in index['Campaigns'].iloc[j]:
            targetList.append("Category")
            continue
        elif "Brand" in index['Campaigns'].iloc[j]:
            targetList.append("Brand")
            continue
        else:
            targetList.append("Invalid")
    index["Targeting"] = targetList


def defineGoal(index):
    goalList = []
    for j in range(len(index)):
        if "Purchases Retargeting" in index['Campaigns'].iloc[j]:
            goalList.append("Loyalty")
            continue
        elif "Brand" in index['Campaigns'].iloc[j]:
            goalList.append("Conversion")
            continue
        elif "Auto" in index['Campaigns'].iloc[j] or "Competitor" in index['Campaigns'].iloc[j] or "Category" in index['Campaigns'].iloc[j]:
            goalList.append("Consideration")
            continue
        else:
            goalList.append("Invalid")
    index["Goal"] = goalList


def defineAdType(index):
    adTypeList = []
    for j in range(len(index)):
        if " SB " in index['Campaigns'].iloc[j]:
            adTypeList.append("SB")
            continue
        elif " SP " in index['Campaigns'].iloc[j]:
            adTypeList.append("SP")
            continue
        elif " SD " in index['Campaigns'].iloc[j]:
            adTypeList.append("SD")
            continue
        elif " SBV " in index['Campaigns'].iloc[j]:
            adTypeList.append("SBV")
            continue
        else:
            adTypeList.append("Invalid")
    index["Goal"] = adTypeList


def defineBrand(index, brandInput):
    brandList = []
    for j in range(len(index)):
        for k in range(len(brandInput)):
            if brandInput[k] in index['Campaigns'].iloc[j]:
                brandList.append(brandInput[k])
    try:
        index["Brand"] = brandList
    except Exception as e:
        print(e)


"""
main function
loops over params to gather needed columns for index file
"""
def createIndex(data, params):
    index = data[['Campaigns']]
    for i in range(len(params)):
        if 'Goal' in params[i]:
            defineGoal(index)
        if 'Targeting' in params[i]:
            defineTargeting(index)
        if 'Ad Type' in params[i]:
            defineAdType(index)
        if 'Brand' in params[i]:
            brandInput = params[i].split("-")[1].split("+")
            defineBrand(index, brandInput)
    return index