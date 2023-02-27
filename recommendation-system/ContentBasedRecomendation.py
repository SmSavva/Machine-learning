import pandas as pd
import os
from PreparationData import films
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

csv_filename = os.path.join(os.path.dirname(__file__), 'data/links_small.csv')
small_links = pd.read_csv(csv_filename)
small_links = small_links[small_links['tmdbId'].notnull()]['tmdbId'].astype('int')
dop_df = films[films['movieId'].isin(small_links)]

dop_df['tagline'] = dop_df['tagline'].fillna('')
dop_df['description'] = dop_df['overview'] + dop_df['tagline']
dop_df['description'] = dop_df['description'].fillna('')

tfVect = TfidfVectorizer(ngram_range=(1,2), min_df=0)
simular_films = tfVect.fit_transform(dop_df.description)
cosine_sim = cosine_similarity(simular_films, simular_films)
dop_df = dop_df.reset_index()

def get_content_recomendations(movieId):
    idx = dop_df[dop_df.movieId == movieId]['index']
    if idx.empty: return []
    idx = int(idx.iloc[0])
    if idx>dop_df.shape[0]: return [] 
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    content_rec = [i[0] for i in sim_scores]
    return content_rec
