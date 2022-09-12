import os, sys
import numpy as np
import pandas as pd
#stemming class from nltk
from nltk.stem.porter import PorterStemmer
#count vectorizor
from sklearn.feature_extraction.text import CountVectorizer
#cosine similarties to calculate the similarty measure between movies
from sklearn.metrics.pairwise import cosine_similarity
from netflix.exception import RecommendationException
from netflix.logger import lg
from collections import namedtuple

recommendation = namedtuple("recommendation",["message","recom_1","recom_2","recom_3","recom_4","recom_5"])

class similar_recommendation:
    def __init__(self, type:str):
        try:
            self.type = type
            if type == "movies":
                lg.info("searching for movies")
                self.df = pd.read_csv("netflix_movies.csv")
            elif type == "shows":
                lg.info("searching for shows")
                self.df = pd.read_csv("netflix_shows.csv")

            ps = PorterStemmer()

            cv = CountVectorizer(max_features=5000,stop_words='english')
            self.vectors = cv.fit_transform(self.df['description']).toarray()
            self.similarity = cosine_similarity(self.vectors)
        except Exception as e:
            raise RecommendationException(e, sys) from e
    
    def recommend(self,movie: str)-> recommendation:
        try:
            movie = movie.lower()
            movie_list = self.df[self.df['title'].str.lower().str.contains(movie)]
            if len(movie_list):  
                movie_idx= movie_list.index[0]
                distances = self.similarity[movie_idx]
                movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]
                
                l = []
                for i in movies_list:
                    l.append(self.df.iloc[i[0]].title)
            
                lg.info(f"Recommendations for {movie_list.iloc[0]['title']} : {l}")
    
                recommendation_output = recommendation(message = f"Recommendations for {[movie_list.iloc[0]['title']]} :",
                                            recom_1 =  l[0],
                                            recom_2 =  l[1],
                                            recom_3 =  l[2],
                                            recom_4 =  l[3],
                                            recom_5 =  l[4])
                
                return recommendation_output
            else:
                 invalid_output = recommendation(message = f"No {[movie]} found in Netflix . Please check your input {[movie]} is a show or a movie.",
                                            recom_1 =  None,
                                            recom_2 =  None,
                                            recom_3 =  None,
                                            recom_4 =  None,
                                            recom_5 =  None)
            return invalid_output
        except Exception as e:
            raise RecommendationException(e, sys) from e

