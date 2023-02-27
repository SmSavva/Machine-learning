import pandas as pd
from ast import literal_eval
import os

csv_filename = os.path.join(os.path.dirname(__file__), 'data/movies_metadata.csv')
films = pd.read_csv(csv_filename)
films.genres = films.genres.fillna('[]').apply(literal_eval)\
.apply(lambda f: [i['name'] for i in f] if isinstance(f, list) else [])
films.spoken_languages = films.spoken_languages.fillna('[]')\
.apply(literal_eval).apply(lambda f: [i['name'] for i in f] if isinstance(f, list) else [])
films.release_date = pd.to_datetime(films.release_date, errors='coerce')
films['year'] = films.release_date.dt.year
films.vote_count = films[films['vote_count'].notnull()]['vote_count'].astype('int')
films = films.drop([19730, 29503, 35587])
films.homepage = films.homepage.fillna('-')
films= films.rename(columns={'id':'movieId'})
films.movieId =pd.to_numeric(films.movieId, errors='coerce')





