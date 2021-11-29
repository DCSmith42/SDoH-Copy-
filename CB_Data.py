# Imports.
import pandas as pd
import censusdata
# Pandas options.
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
pd.options.mode.chained_assignment = None

# StateNum is the number of the state.
# Year of the data to be pulled.
# Level is the granularity, e.g. county or tract.
# Variables is a dictionary that takes in the names and variables that will be pulled.
# Example: {'population':'DP05_0001E', 'poverty_percent':'DP03_0119PE'}
def cbdata (StateNum, Year, Level, Variables):
        num = str(StateNum)
        y = int(Year)
        level = Level
        dictionary = Variables
        codes = list(dictionary.values())
        names = list(dictionary.keys())
        
        if (level is "county" or level is "County"):
            data=censusdata.download('acs5', y, censusdata.censusgeo([('state', num),('county', '*')]), codes, tabletype='profile')
            
            niter = len(codes)
            for i in range(niter):
                data[names[i]]=data[codes[i]] 
            
            # Adds column names.
            data = data[names]
            
            # Parsing
            t = data
            t.reset_index(inplace=True)
            t.rename(columns={'index': 'longform'}, inplace=True)
            index = t.index
            # Parsing each counties information into a list of three strings: County, State, State and County Code.
            nrows = len(index)
            temp = []
            for i in index:
                a = t.iloc[i]['longform']
                b = str(a).split(',')
                
                a = t.iloc[i]['longform']
                b = str(a).split(',')
                # State cleaning.
                d = b[1]
                d = d.split(':' )[0]
                b[1]=d
                # Splits state number and county number.
                d = b[2]
                d1 = d.split('>')[0] 
                d2 = d.split('>')[1]
                d1 = d1.split(':')[1] # State number
                d2 = (d2.split(':')[1]) # County number
                b[2]=d2
                b.append(d1)
                #
                c = map(str.strip, b) # Removes whitespaces.
                temp.append(c)
            # Convert list into dataframe
            df = pd.DataFrame(temp, columns=['County','State','County_Number','State_Number'])
            # Combine dataframes.
            result = pd.concat([df, t], axis=1, sort=False)
            temp = result.drop(columns=['longform'])
            # Sorting
            s = temp.sort_values(['County'])
            # Adds extra columns (County)
            # ID
            s['GEOID'] = s["State_Number"] + s["County_Number"]
            # Year
            s['Year'] = Year
            # Source
            s['Source'] = 'Census Bureau'
            # Subsource
            s['Subsource']='ACS 5 Year'
            # Variables
            if (len(codes) != 1):
                for i in range(len(codes)):
                    s['Variable_'+str(i+1)]=codes[i]
            else:
                s['Variable']=codes[0]
            
            final = s.reset_index(drop=True)
            
        elif (level is "tract" or level is "Tract"):
            data=censusdata.download('acs5', y,
            censusdata.censusgeo([('state', num),('county', '*'),('tract','*')]),codes)
            
            niter = len(codes)
            for i in range(niter):
                data[names[i]]=data[codes[i]]
            
            # Adds column names
            data = data[names]
            
            # Parsing
            t = data
            t.reset_index(inplace=True)
            t.rename(columns={'index': 'longform'}, inplace=True)
            index = t.index
            # Parsing each counties information into a list of three strings: Tract, County, State, State and County Code.
            nrows = len(index)
            temp = []
            for i in index:
                a = t.iloc[i]['longform']
                b = str(a).split(',')
                # Tract cleaning.
                d = b[0]
                d = d.split(' ')[2]
                b[0]=d
                # State cleaning.
                d = b[2]
                d = d.split(':' )[0]
                b[2]=d
                # Splits state number and county number.
                d = b[3]
                d1 = d.split('>')[0] 
                d2 = d.split('>')[1]
                d1 = d1.split(':')[1] # State number
                d2 = d2.split(':')[1] # County number
                b[3]=d2
                b.append(d1)
                #
                c = map(str.strip, b) # Removes whitespaces.
                temp.append(c)
            # Convert list into dataframe
            df = pd.DataFrame(temp, columns=['Tract','County','State','County_Number','State_Number'])
            # Combine dataframes.
            result = pd.concat([df, t], axis=1, sort=False)
            #
            temp = result.drop(columns=['longform'])
            # Sorting
            s = temp.sort_values(by=['County'])
            s["Tract"]= s["Tract"].str.replace(".", "") 
            # Adds extra columns (Tract)
            # ID
            s['GEOID'] = s["State_Number"] + s["County_Number"]
            for i in range(len(s)):
                temp = s['GEOID'][i]
                s['GEOID'][i]= temp + '0'*(6-len(s["Tract"][i])) + s["Tract"][i]
            # Year
            s['Year'] = Year
            # Source
            s['Source'] = 'Census Bureau'
            # Subsource
            s['Subsource']='ACS 5 Year'
            # Variables
            if (len(codes) != 1):
                for i in range(len(codes)):
                    s['Variable_'+str(i+1)]=codes[i]
            else:
                s['Variable']=codes[0]
            
            final = s.reset_index(drop=True)
        
        return final