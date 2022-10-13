## Doubt:- What is ts?
## Api Doc:- https://developer.marvel.com/docs#!/public/getComicsCharacterCollection_get_2

from cmath import nan
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import hashlib
import pandas as pd
import string

def create_marvel_df(api_key, hash_key, startsWithLetter='a'):
    ## declare the variables
    name = []
    id = []
    comics_avail = []
    series_avail = []
    stories_avail = []
    events_avail = []
    offset=0
    for i in range(3):
        nameStartsWith = startsWithLetter
        limit = 100

        
        response = requests.get(f'http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={api_key}&hash={hash_key}&nameStartsWith={nameStartsWith}&limit={limit}&offset={offset}')
        
        marvel_json = response.json()
        if marvel_json.get("message"):
            print(marvel_json["message"])
            return

        else:
            try:
                characters_list = marvel_json['data']['results']
            except KeyError as e:
                print(e)

            for i in characters_list:
                name.append(i['name'])
                id.append(i['id'])
                comics_avail.append(i['comics']['available'])
                series_avail.append(i['series']['available'])
                stories_avail.append(i['stories']['available'])
                events_avail.append(i['events']['available'])
                
            if len(name)<offset+100:
                break
            else:
                offset=offset+100
            
    ## Create a dataframe
    marvel_df = pd.DataFrame()
    marvel_df["Character_id"] = id
    marvel_df["Character_name"] = name
    marvel_df["comics_avail"] = comics_avail
    marvel_df["series_avail"] = series_avail
    marvel_df["stories_avail"] = stories_avail
    marvel_df["events_avail"] = events_avail
    return marvel_df
    ## Filter the dataframe 
    # marvel_df.to_csv(f"marvel_{startsWithLetter}_characters.csv", index=False)


## Set the path. Suppose if .env is in another folder then this will helps us to set the path
path = Path('.')/'.env'

## load the keys to the environment
load_dotenv(path)
## load_dotenv()       ## if .env is in the same folder then can call load_dotenv directly

## fetch the keys from environment and store it in variables
ts=5
private_key = os.environ.get('private_key')
public_key = os.environ.get('public_key')

## Find the has value by converting ts+private_key+public_key string to md5 value
m = hashlib.md5()
text = str(ts)+private_key+public_key
m.update(text.encode('utf-8'))
hash = m.hexdigest()

## Call the function
startsWithLetter = input("Enter a letter from which marvel characters should starts: ").lower()

marvel_df = create_marvel_df(public_key, hash, startsWithLetter)
# print(marvel_df)

## Create a lambda function to filter the number columns
filter_column = input('Enter the column you want to filter out:')
condition = input('Provide the condition for filter: ')
number = int(input('Enter the base number for filter: '))

## Using eval we are filtering the condition that is entered by the user
marvel_filter = lambda x, condition, number: x if eval(f'{x} {condition} {number}') else nan
marvel_df['comics_avail'] = marvel_df['comics_avail'].apply(marvel_filter, args=(condition, 10))
marvel_df = marvel_df[marvel_df["comics_avail"].notnull()]
marvel_df.reset_index(inplace=True)
marvel_df.drop('index', axis=1, inplace=True)
print(marvel_df)

## Filter using loc
# marvel_df = marvel_df.loc[marvel_df['comics_avail']>10]
# print(marvel_df)