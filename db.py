'''import mysql.connector
db = mysql.connector.connect(
    host= "localhost",
    user= "root",
    passwd = "mamo",
    database = "sirma"
)
cursor = db.cursor()

def f(comp):
    sqlformula = "INSERT INTO companies(company_id, company) VALUES (%s,%s)"
    cursor.execute(sqlformula, (2, comp))
    db.commit()


def insert_comp(company_id = None,
company = None ,
country = None,
important = None,
activity = None ,
email = None,
num = None,
mng_name = None ,
site = None,
person  = None):
    li = ["company_id",
"company"  ,
"country",
"important",
"activity" ,
"email" ,
"num" ,
"mng_name" ,
"site",
"person"]

sqlformula = "INSERT INTO companies(company_id, company) VALUES (%s,%s)"
cursor.execute(sqlformula, (1,"my comany"))
db.commit()'''

import pandas as pd

df = pd.DataFrame({"mamo":[1,2,4,5],"ali":[2,2,3,4]})
df.loc[len(df)] = [200,200]
print(df)







