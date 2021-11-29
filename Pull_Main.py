import pandas as pd
import os
from CB_Data import cbdata
from DB_Upload import upload

# Main script for pulling Census Bureau data.

server = os.environ.get('sdoh_con')

# Function to pull variable for both Virginia and West Virginia.
def pull(Year, Level, Variables, TableName, Schema):
    # Virginia data call.
    VATract_var = cbdata(51, Year, Level,  Variables); 
    # West Virginia data call.
    WVTract_var = cbdata(54, Year, Level, Variables);
    # Combines data frames.
    data = pd.concat([VATract_var, WVTract_var]);
    data = data.reset_index(drop=True);
    # Exports data to database.
    upload(TableName, data, server, Schema)
    
    return 1
# Variable calls.
#1
name = 'population'
var =  {name:'B01001_001E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#2
name = 'poverty'
var =  {name:'B17001_002E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#3
name = 'Unemployment'
var =  {name:'B23025_005E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#4
name = 'Social_Security_Supp'
var =  {name:'B19056_002E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#5
name = 'Public_Assistance_Income'
var =  {name:'B19057_002E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#6
name = 'Cash_Public_Assistance_And_Stamps/SNAP'
var =  {name:'B19058_002E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#7
name = 'Allocated_Stamps/SNAP'
var =  {name:'B99221_002E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')
#8
name = 'Not_Allocated_Stamps/SNAP'
var =  {name:'B99221_001E'}
pull(2018, 'tract', var, name+'_tract', 'Census_Bureau')