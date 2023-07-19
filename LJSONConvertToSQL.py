## Convert Json Line to Json
import json
import pandas as pd
from tqdm.notebook import tqdm_notebook
import pyodbc as po
jsonObj = pd.read_json(path_or_buf='torob-search-data_v1.jsonl', lines=True)
df = pd.DataFrame(jsonObj)
df.to_json('torob-search-data_v1.json',orient='records')

## Load Data From Json File
with open('torob-search-data_v1.json',encoding='utf-8-sig') as user_file:
    file_contents = user_file.read()
data = json.loads(file_contents)


print('Server Name : ')
ServerName = input()

print('UserName : ')
Username = input()

print('Password : ')
Password = input()

print('Database Name : ')
DatabaseName = input()

print('Table Name : ')
TableName=input()

print('Column Index : ')
IndexName=input()


## Connect To Database

connectionString = (
    "Driver={ODBC Driver 17 for SQL Server}"
    f";Server={ServerName};UID={Username};PWD={Password}")

conn = po.connect(connectionString)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
rows = cursor.fetchall()
print(rows)

## Create And Insert Data To Database


jsonField = data[0]
fieldsCreateTable = ''
fieldsInsertTable = ''
DataType = ''
PrimaryKey = ''

for key, value in jsonField.items():
    if type(value) == int:
        DataType = 'int'
    elif type(value) == float:
        DataType = 'float'
    elif type(value) == str:
        DataType = 'NVARCHAR(MAX)'
    elif type(value) == list:
        DataType = 'NVARCHAR(MAX)'

    if key == IndexName and type(value) == int:
        PrimaryKey = 'PRIMARY KEY'
    else:
        PrimaryKey = ''

    fieldsCreateTable = fieldsCreateTable + f' {key} {DataType} {PrimaryKey},'
    fieldsInsertTable = fieldsInsertTable + f' {key},'

fieldsCreateTable = fieldsCreateTable[:-1]
result = cursor.execute(f'USE {DatabaseName} CREATE TABLE {TableName}( {fieldsCreateTable} )')

fieldsInsertTable = fieldsInsertTable[:-1]
for item in tqdm_notebook(data):
    dataInsertTable = ''
    for d in list(item.values()):

        if type(d) == list:
            d = ' '.join(str(x) for x in d)
            d = d.replace('\'', '')
        dataInsertTable = dataInsertTable + f"N'{d if d != None else ''}',"
    dataInsertTable = dataInsertTable[:-1]
    query = 'INSERT ' + TableName + '(' + fieldsInsertTable + ') Values (' + dataInsertTable + ')'
    result = cursor.execute(query)

print('Success !')
