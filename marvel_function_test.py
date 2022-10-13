from marvel_api.fetch_character_df import MarvelApi
import argparse

## Create an object of class
marvel_api_obj = MarvelApi()

#Initialize the parser
parser = argparse.ArgumentParser(description="Provide the api key, hash key and initial letter of marvel characters")

# Adding the arguments
parser.add_argument('api_key',
                    type=str,
                    help='provide the api_key (public key)')
 
parser.add_argument('hash_key',
                    type=str,
                    help='provide the hash_key for authorization')
                    
parser.add_argument('character',
                    type=str,
                    help='Enter the initial character of which you have to fetch the marvel data')

## Parsing arguments
ts=1
args = parser.parse_args()
public_key = getattr(args, 'api_key')
hash_key = getattr(args, 'hash_key')
startsWithLetter = getattr(args, 'character').lower()

## Fetch the data from API
offset = 0
marvel_json = []
for i in range(3):
    marvel_json += marvel_api_obj.fetchApiData(ts, public_key, hash_key, startsWithLetter, offset)

    if len(marvel_json)<offset+100:
        break
    else:
        offset=offset+100

## Convert the json file to dataframe
marvel_df = marvel_api_obj.convertJsonToDataframe(marvel_json)
print(marvel_df.head())
print(len(marvel_df))