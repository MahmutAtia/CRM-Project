

import gspread
import pandas as pd


def set_work_sheet(user):
    sa = gspread.service_account()
    if user == "ma":
        sh = sa.open("(MA) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
    elif user == "amir":
        sh = sa.open("(MOUSTAPHA) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
    elif user == "ali":
        sh = sa.open("(AL) SIRMA METAL  - İhracat Sistemi - Made by Muhammet AKMAN")
    return sh.worksheet("ARAMA LİSTELERİ V.2")

#todo 1 : get all companies information

def get_all_companies(wk):
    comp_info = wk.batch_get(['C3:C','D3:D',"I3:I",'H3:H',"J3:J","K3:K"])
    imp_or_not = wk.batch_get(['E3:E','F3:F'])
    df1 = pd.DataFrame(comp_info)
    df2 = pd.DataFrame(imp_or_not)
    # clean values in columns
    li = []
    for column in df1:
       li.append(df1[column].apply(lambda x: x[0].strip() if(x) else " "))
    df1 = pd.concat(li,1)
    li2=[]
    for column in df2: #make the lists  0 or 1
       li2.append( df2[column].apply(lambda x: x[0] if(x) else " "))
    df2= pd.concat(li2,1)
    return df1.transpose(),df2.transpose()[:df1.shape[1]]




#todo 2 : get all information of a certen company ?

#todo 3 : find a comany with compyny name or manager name or email or website

#todo 4 : get compynies in certen country

#Add New Companies
def add(row, where, wk,df_company,add= False):
    i = int(where)
    if add:
    #adding to pandas
        df_company.loc[i] = row
        i = i+3

    else:
        df_company.loc[i-1]
        i=i+2 # spread index
    #adding to spreedsheet
    wk.update("C{}".format(i),row[0])
    wk.update("D{}".format(i),row[1])
    wk.update("I{}".format(i),row[2])
    wk.update("H{}".format(i),row[3])
    wk.update("J{}".format(i),row[4])
    wk.update("K{}".format(i),row[5])

# ger history of contacts
def history(i,wk):
    return wk.batch_get([f"O{i}:T{i}",f"V{i}:AA{i}",f"AC{i}:AH{i}",f"AJ{i}:AO{i}", f"AQ{i}:AV{i}",f"AX{i}:BC{i}",f"BD{i}:BI{i}",f"BJ{i}:BO{i}"] )

# update contacts
i = 3

def update_c(indxOfCompany,whichContact,row,wk):
    i = indxOfCompany
    j = whichContact-1
    print(i)
    print(j)
    li = [[f"O{i}:T{i}",f"V{i}:AA{i}",f"AC{i}:AH{i}",f"AJ{i}:AO{i}", f"AQ{i}:AV{i}",f"AX{i}:BC{i}",f"BD{i}:BI{i}",f"BJ{i}:BO{i}"]]
    wk.batch_update([
            {
                'range': li[0][j], # head
                'values': [row]
            }] )
    print(li[0][j])


wk = set_work_sheet("ma")
print(history(474,wk))
