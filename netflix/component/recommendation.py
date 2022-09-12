from email import message
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from collections import namedtuple
from netflix.exception import RecommendationException
from netflix.logger import lg


recommendation = namedtuple("recommendation",["message","recom_1","recom_2","recom_3","recom_4","recom_5"])


class Recommendation:
    def __init__(self, type:str):
        try:
            self.type = type
            if type == "movies":
                lg.info("searching for movies")
                self.df = pd.read_csv("netflix_movies.csv")
            elif type == "shows":
                lg.info("searching for shows")
                self.df = pd.read_csv("netflix_shows.csv")
        except Exception as e:
            raise RecommendationException(e, sys) from e

    def recommendation(self, input: str) -> recommendation:
        try:
            input = input.lower()
            searched = self.df[self.df['genres'].str.lower().str.contains(input)]
            if len(searched):
                l = []
                for i, row in searched.iterrows():
                    l.append(self.df.iloc[i].title)
    


                lg.info(f"Recommendation for {input} : {l[:10]}")
                #print(searched['title'][:10])  # to display output in terminal
                recommendation_output = recommendation(message = f"Recommendation for {[input]} :",
                                                recom_1 =  l[0],
                                                recom_2 =  l[1],
                                                recom_3 =  l[2],
                                                recom_4 =  l[3],
                                                recom_5 =  l[4])
            
                return recommendation_output
            else:
                invalid_output = recommendation(message = f"No {[input]} found in Netflix . Please check your input {[input]} is a genre or Not .",
                                                recom_1 =  None,
                                                recom_2 =  None,
                                                recom_3 =  None,
                                                recom_4 =  None,
                                                recom_5 =  None)
            return invalid_output
            #print(recommendation_output)
        except Exception as e:
            raise RecommendationException(e, sys) from e

