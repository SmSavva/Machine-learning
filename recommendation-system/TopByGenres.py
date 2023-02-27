from PreparationData import films
import pandas as pd

genres = films.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
genres.name = 'genres'
movie_gen = films.drop('genres', axis=1).join(genres)

def chart_by_genre(genre, percentile=0.8):
    if len(genre)!=0:
        m_g = movie_gen.query('genres in @genre')
        if len(m_g) == 0: return pd.DataFrame()
        if len(genre) != 1:
            isd=m_g['movieId']
            m_g = m_g[isd.isin(isd[isd.duplicated()])].drop_duplicates(subset='movieId')
        vote_counts = m_g[m_g['vote_count'].notnull()]['vote_count'] 
        vote_averages = m_g[m_g['vote_average'].notnull()]['vote_average']
        VA_mean = vote_averages.mean()
        VC_quantile = vote_counts.quantile(percentile)

        filter = (m_g['vote_count']>=VC_quantile) & (m_g['vote_count'].notnull()) & (m_g['vote_average'].notnull())
        columns = ['movieId','title', 'year', 'vote_count', 'vote_average', 'popularity']
        qualified = m_g[filter][columns]

        condition = lambda x: x['vote_count']/(x['vote_count']+VC_quantile)*x['vote_average'] + (VC_quantile/(VC_quantile+x['vote_count'])*VA_mean)
        qualified['weight_rating'] = qualified.apply(condition, axis=1)
        qualified = qualified.sort_values('weight_rating' ,ascending=False).head(50)

        return qualified
    else: return pd.DataFrame()


