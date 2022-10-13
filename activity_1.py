## Doubt:- What is ts?
## Api Doc:- https://developer.marvel.com/docs#!/public/getComicsCharacterCollection_get_2

import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import hashlib
import pandas as pd
import string

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

## declare the variables
name = []
id = []
comics_avail = []
series_avail = []
stories_avail = []
events_avail = []

## Create a list of alphabet and digits
alpha_digits = list(string.ascii_lowercase)
alpha_digits.extend([1, 2, 3, 4, 5, 6, 7, 8, 9])
# print(alpha_digits)

## Make an API call to fetch the character's data dynamically
for char in alpha_digits:
    # char_name = []
    offset=0
    for i in range(3):
        char_name = []
        nameStartsWith = char
        limit = 100
        response = requests.get(f'http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={public_key}&hash={hash}&nameStartsWith={nameStartsWith}&limit={limit}&offset={offset}')

        marvel_json = response.json()
        try:
            characters_list = marvel_json['data']['results']
        except KeyError as e:
            print(e)

        for i in characters_list:
            char_name.append(i['name'])
            id.append(i['id'])
            comics_avail.append(i['comics']['available'])
            series_avail.append(i['series']['available'])
            stories_avail.append(i['stories']['available'])
            events_avail.append(i['events']['available'])
        
        # now append the char name to the name
        name.extend(char_name)

        if len(char_name)<100:
            # print(char + ":" + str(len(char_name)))
            break
        else:
            # print(char + ":" + str(len(char_name)))
            offset=offset+100
        


## Note:- If we use namesStartsWith parameter then it returns only 202 values , thus there are only 202 characters that starts with 
# s, thus withoout namesStartsWuth we get 300 unique characters.

## Create a dataframe
marvel_df = pd.DataFrame()
marvel_df["Character_id"] = id
marvel_df["Character_name"] = name
marvel_df["comics_avail"] = comics_avail
marvel_df["series_avail"] = series_avail
marvel_df["stories_avail"] = stories_avail
marvel_df["events_avail"] = events_avail
print(marvel_df)

exit()
marvel_df.to_csv("marvel.csv", index=False)