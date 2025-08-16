import json

with open('Setup_Configrations.json', 'r') as file:
    setupConfigrationData = json.load(file)

global dbName, dbUser, dbPassword, dbHost, dbPort

dbName = setupConfigrationData['dbName']
dbUser = setupConfigrationData['dbUser']
dbPassword = setupConfigrationData['dbPassword']
dbHost = setupConfigrationData['dbHost']
dbPort = setupConfigrationData['dbPort']