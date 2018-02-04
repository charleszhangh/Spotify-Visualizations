import pandas as pd

#convert data from CSV
DIR_INPUT = "C:/Users/cz/Desktop/worldtastes/"
master_data = pd.read_csv(DIR_INPUT + "worldtastes_data.csv",encoding="ISO-8859-1")

master_df = pd.DataFrame(master_data)

def searchValue(val):
    country_dict = {'Argentina': 'ar', 'Australia': 'au', 'Austria': 'at', 'Belgium': 'be', 'Bolivia': 'bo',
                    'Brazil': 'br', 'Bulgaria': 'bg',
                    'Canada': 'ca', 'Chile': 'cl', 'Colombia': 'co', 'Costa Rica': 'cr', 'Cyprus': 'cy',
                    'Czech Republic': 'cz', 'Denmark': 'dk', 'Dominican Republic': 'do', 'Ecuador': 'ec',
                    'Estonia': 'ee', 'Finland': 'fi',
                    'France': 'fr', 'Germany': 'de', 'Global': 'global', 'Greece': 'gr', 'Guatemala': 'gt',
                    'Honduras': 'hn', 'Hong Kong': 'hk', 'Hungary': 'hu',
                    'Iceland': 'is', 'Indonesia': 'id', 'Ireland': 'ie', 'Italy': 'it', 'Japan': 'jp', 'Latvia': 'lv',
                    'Lithuania': 'lt', 'Luxembourg': 'lu',
                    'Malaysia': 'my', 'Malta': 'mt', 'Mexico': 'mx', 'Monaco': 'mc', 'Netherlands': 'nl',
                    'New Zealand': 'nz', 'Nicaragua': 'ni',
                    'Norway': 'no', 'Panama': 'pa', 'Paraguay': 'py', 'Peru': 'pe', 'Philippines': 'ph', 'Poland': 'pl',
                    'Portugal': 'pt',
                    'El Salvador': 'sv', 'Singapore': 'sg', 'Spain' :'es','Slovakia': 'sk', 'Sweden': 'se', 'Switzerland': 'ch',
                    'Taiwan': 'tw', 'Thailand': 'th', 'Turkey': 'tr', 'United States': 'us', 'United Kingdom': 'gb',
                    'Uruguay': 'uy'}

    for country, abr in country_dict.items():  # for name, age in list.items():  (for Python 3.x)
        if abr == val:
            return country

for x, df_rows in master_df.iterrows():
    abr = master_df.loc[x,'region']
    country = searchValue(abr)
    master_df.loc[x,'country_name'] = country

master_df.to_csv('new_output.csv')