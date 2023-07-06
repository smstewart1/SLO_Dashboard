#libraries
import pandas as pd 
import numpy as np

#definitions

#Question descritions
KB = [[1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0]]
CT = [[0, 0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0]]
QL = [[0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 0, 0]]
SL = [[0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1]]
PS = [[0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0]]

#campus code 0 = online, 1 = SWC, 2 = NWC, 3 = RTP

#main function
def main():
    
    #read in data set
    df = pd.read_csv("CHM152.csv")
    
    #clear out missing data and process
    df.dropna(inplace = True)
    df = delivery(df)
    df = subcounts(df)
    df = year_clean(df)
    
    #build up the semester metrics
    calc_df = compressed_array(df)
    calc_df.to_csv("SummaryStats152.csv")
    
    #saves cleaned file
    df.to_csv("DashboardData152.csv")
    return 0

#functions
#converts the delivery to campus by course number
def delivery(df):
    df_temp = pd.get_dummies(df, columns = ["Code"], dtype = float)
    df_temp["Campus"] = 1 * (df_temp["Code_41"] + df_temp["Code_21"]) + 2 * (df_temp["Code_42"] + df_temp["Code_22"])+ 3 * (df_temp["Code_48"] + df_temp["Code_28"])
    df_temp.drop(columns = ["Code_41", "Code_0", "Code_42", "Code_22", "Code_21", "Code_28", "Code_48"], inplace = True)
    return df_temp

#converts the year/term into a continuum with FA as 0.5 and spring as 0.0
def year_clean(df):
    df_temp = pd.get_dummies(df, columns = ["Term"], dtype = float)
    df_temp["Date Taken"] = 0.5 * df_temp["Term_FA"] + df_temp["Year"].astype(int) + 2000
    df_temp.drop(columns = ["Term_FA", "Term_SP"], inplace = True)
    return df_temp

#breaks the data frame into the five SLO areas
def subcounts(df):
    # break into the five areas
    df1 = row_update(df, 1)
    df2 = row_update(df, 2)
    df3 = row_update(df, 3)
    df4 = row_update(df, 4)
    df5 = row_update(df, 5)
    dffinal = pd.concat([df1, df2, df3, df4, df5])    
    return dffinal

#breaks the questions into their other measured areas, e.g., knowledge based
def row_update(dffull, i):  
    pd.set_option('mode.chained_assignment', None) #clear warnings on chaining
    df = dffull.loc[dffull["Area"] == i]
    KBN = sum(KB[i - 1])
    CTN = sum(CT[i - 1])
    QLN = sum(QL[i - 1])
    SLN = sum(SL[i - 1])
    PSN = sum(PS[i - 1])
    df["KB"] = (df["Q1"] * KB[i - 1][0] +  df["Q2"] * KB[i - 1][1] + df["Q3"] * KB[i - 1][2] + df["Q4"] * KB[i - 1][3] + df["Q5"] * KB[i - 1][4] + df["Q6"] * KB[i - 1][5] +  df["Q7"] * KB[i - 1][6]) / KBN
    df["CT"] = (df["Q1"] * CT[i - 1][0] +  df["Q2"] * CT[i - 1][1] + df["Q3"] * CT[i - 1][2] + df["Q4"] * CT[i - 1][3] + df["Q5"] * CT[i - 1][4] + df["Q6"] * CT[i - 1][5] +  df["Q7"] * CT[i - 1][6]) / CTN
    df["QL"] = (df["Q1"] * QL[i - 1][0] +  df["Q2"] * QL[i - 1][1] + df["Q3"] * QL[i - 1][2] + df["Q4"] * QL[i - 1][3] + df["Q5"] * QL[i - 1][4] + df["Q6"] * QL[i - 1][5] +  df["Q7"] * QL[i - 1][6]) / QLN
    df["SL"] = (df["Q1"] * SL[i - 1][0] +  df["Q2"] * SL[i - 1][1] + df["Q3"] * SL[i - 1][2] + df["Q4"] * SL[i - 1][3] + df["Q5"] * SL[i - 1][4] + df["Q6"] * SL[i - 1][5] +  df["Q7"] * SL[i - 1][6]) / SLN
    df["PS"] = (df["Q1"] * PS[i - 1][0] +  df["Q2"] * PS[i - 1][1] + df["Q3"] * PS[i - 1][2] + df["Q4"] * PS[i - 1][3] + df["Q5"] * PS[i - 1][4] + df["Q6"] * PS[i - 1][5] +  df["Q7"] * PS[i - 1][6]) / PSN
    return df

#creates a year by year breakdown of the data by campus
def compressed_array(dfin):
    date_index = dfin["Date Taken"].unique()
    totalarray = []
    Oarray = []
    Sarray = []
    Narray = []
    Rarray = []
    for j in range(0, 5):
        df = dfin.loc[dfin["Area"] == j + 1]
        for i in date_index:
            dftsub = df.loc[df["Date Taken"] == i]
            dfosub = dftsub.loc[df["Campus"] == 0.0]
            dfnsub = dftsub.loc[df["Campus"] == 2.0]
            dfssub = dftsub.loc[df["Campus"] == 1.0]
            dfrsub = dftsub.loc[df["Campus"] == 3.0]
            totalarray.append(compression_wrap(dftsub, i, j, "Total"))
            Oarray.append(compression_wrap(dfosub, i, j, "Online"))
            Narray.append(compression_wrap(dfnsub, i, j, "Northern Wake Campus"))
            Sarray.append(compression_wrap(dfssub, i, j, "Southern Wake Campus"))
            Rarray.append(compression_wrap(dfrsub, i, j, "RTP Campus"))
    tdf = pd.DataFrame(totalarray, columns = ["Year Taken", "SLO Area", "Campus", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "KB", "CT", "QL", "SL", "PS", "Proficiency", "Number of Students"])
    odf = pd.DataFrame(Oarray, columns = ["Year Taken", "SLO Area", "Campus", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "KB", "CT", "QL", "SL", "PS", "Proficiency", "Number of Students"])
    ndf = pd.DataFrame(Narray, columns = ["Year Taken", "SLO Area", "Campus", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "KB", "CT", "QL", "SL", "PS", "Proficiency", "Number of Students"])
    sdf = pd.DataFrame(Sarray, columns = ["Year Taken", "SLO Area", "Campus", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "KB", "CT", "QL", "SL", "PS", "Proficiency", "Number of Students"])
    rdf = pd.DataFrame(Rarray, columns = ["Year Taken", "SLO Area", "Campus", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "KB", "CT", "QL", "SL", "PS", "Proficiency", "Number of Students"])
    outputarray = pd.concat([tdf, odf, ndf, sdf, rdf])
    return outputarray


#finds the percents per question
def compression_wrap(df, i, j, delivery):
    students = df["Students"].sum()
    if students > 0:
        array = [i, j + 1, delivery, df["Q1"].sum()/students, df["Q2"].sum()/students, df["Q3"].sum()/students, df["Q4"].sum()/students, df["Q5"].sum()/students, df["Q6"].sum()/students, df["Q7"].sum()/students, df["KB"].sum()/students, df["CT"].sum()/students, df["QL"].sum()/students, df["SL"].sum()/students, df["PS"].sum()/students, df["Proficient"].sum()/students, students] 
    else:
        array = [i, j + 1, delivery, "", "", "", "", "", "", "", "", "", "", "", ""]
    return array

#execute 
main()