import os
import json
from dotenv import load_dotenv

tools=[
    {
        "type":"function",
        "function":{
            "name":"analyse_movies",
            "description":"当你想要了解一部电影和它的影评的时候非常有用。",
            "parameters":{
                "type":"object",
                "properties": {
                    "movie_name":{
                        "type":"string",
                        "description":"电影的名称，如肖申克的救赎、霸王别姬等。"
                    }
                }
            },
            "required":["movie_name"]
        }
    }
]

def get_moive_info(movie_name):
    pass