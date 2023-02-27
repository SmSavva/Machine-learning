from PreparationData import films

vote_counts = films[films.vote_count.notnull()]['vote_count']
vote_averages = films[films.vote_average.notnull()]['vote_average']

VA_mean = vote_averages.mean()
VC_quantile = vote_counts.quantile(0.9)

filter = (films.vote_count>=VC_quantile) & (films.vote_count.notnull()) & (films.vote_average.notnull())
columns = ['movieId','title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']
qualified = films[filter][columns]

def weighted_rating(x):
    VC = x.vote_count
    VA = x.vote_average
    return( VC/(VC+VC_quantile)*VA + (VC_quantile/(VC_quantile+VC)*VA_mean))

qualified['weight_rating'] = qualified.apply(weighted_rating, axis=1)
qualified = qualified.sort_values('weight_rating' ,ascending=False).head(50)
qualified['number'] = [i for i in range(1,51)]

