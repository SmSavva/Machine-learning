import pandas as pd
import os
from PreparationData import movies_metadata
import numpy as np
from sklearn.metrics.pairwise import  cosine_similarity

csv_filename = os.path.join(os.path.dirname(__file__), 'data/ratings_small.csv')
ratings = pd.read_csv(csv_filename)
ratings.movieId = pd.to_numeric(ratings.movieId, errors= 'coerce')
dict_ratings = ((ratings.userId.iloc[0],ratings.userId.iloc[0]),)
for e in set(ratings.userId):
    if (e,e) in dict_ratings: continue
    else: dict_ratings += ((e,e),)

data = pd.merge(ratings, movies_metadata, on='movieId')
matrix = data.pivot_table(index='userId', columns='movieId', values='rating')
matrix = matrix.fillna(0)

def user_films(userId=1):
    moviesId = list(ratings[ratings['userId']==userId]['movieId'])
    movies = []
    for movieId in moviesId:
        title = movies_metadata[movies_metadata['movieId']==movieId]['title']
        if not title.empty: movies.append({'movieId':movieId, 'title': title.to_string(index=False)})
    return movies[:7]

def CollaborativeRec(userId=1, nBestUser=5, nBestProducts=5):
    matches = [(u, cosine_similarity([matrix.iloc[userId]], [matrix.iloc[u]])[0][0]) for u in range(matrix.shape[0]) if u != userId]
    bestMatches = sorted(matches, key=lambda x: x[1], reverse=True)[:nBestUser]
    sim = dict()
    sim_all = sum([x[1] for x in bestMatches])
    bestMatches = dict([x for x in bestMatches if x[1]>0.0])
    user_film = list(ratings[ratings['userId']==userId]['movieId'])
    for relatedUser in bestMatches:
        for film in matrix.iloc[relatedUser].index:
            if film not in user_film:
                if not film in sim: sim[film] = 0.0
                sim[film] += matrix.iloc[relatedUser][film]*bestMatches[relatedUser]
    for film in sim:
        sim[film] /= sim_all
    bestFilms = sorted(sim.items(), key=lambda x: x[1], reverse=True)[:nBestProducts]
    movies = []
    for movieId in bestFilms:
        title = movies_metadata[movies_metadata['movieId']==movieId[0]]['title']
        if not title.empty: movies.append({'movieId':movieId[0], 'title': title.to_string(index=False)})
    return movies

    