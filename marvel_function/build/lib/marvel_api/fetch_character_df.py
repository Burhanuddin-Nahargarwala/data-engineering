## https://www.tutorialsteacher.com/python/python-package

import requests
import pandas as pd

class MarvelApi:
    ## Define the constructor
    def __init__(self):
        pass
    

    ## Create a function that call the api and returns the data in json format
    def fetchApiData(self, ts, api_key, hash_key, startsWithLetter='a', offset=0):
        ## declare the variables
        self.limit = 100

        ## Call the API with the parameters
        self.response = requests.get(f'http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={api_key}&hash={hash_key}&nameStartsWith={startsWithLetter}&limit={self.limit}&offset={offset}')
        
        ## Convert the response into json and store it in the variable
        self.marvel_json = self.response.json()

        ## If http code is 200 then there will no key such as message and in other cases there 
        ## will be 2 keys code and message thus in that case print the error thrown by API
        if self.marvel_json.get("message"):
            return self.marvel_json["message"]
        else:
            try:
                self.characters_list = self.marvel_json['data']['results']
                return self.characters_list
            except KeyError as e:
                print(e)
    
    ## Take the json file and convert it into dataframe
    def convertJsonToDataframe(self, json_file):
        ## create a Dataframe
        self.marvel_df = pd.DataFrame()
        
        ## declare the variables
        self.name = []
        self.id = []
        self.comics_avail = []
        self.series_avail = []
        self.stories_avail = []
        self.events_avail = []
        for i in json_file:
            self.name.append(i['name'])
            self.id.append(i['id'])
            self.comics_avail.append(i['comics']['returned'])
            self.series_avail.append(i['series']['returned'])
            self.stories_avail.append(i['stories']['returned'])
            self.events_avail.append(i['events']['returned'])
        
        ## Create a dataframe
        self.marvel_df = pd.DataFrame()
        self.marvel_df["Character_id"] = self.id
        self.marvel_df["Character_name"] = self.name
        self.marvel_df["comics_avail"] = self.comics_avail
        self.marvel_df["series_avail"] = self.series_avail
        self.marvel_df["stories_avail"] = self.stories_avail
        self.marvel_df["events_avail"] = self.events_avail
        return self.marvel_df