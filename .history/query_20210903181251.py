from app import Movie
movie = Movie.query.first()

print(movie.title,movie.year) 
print(Movie.query.add())
print(Movie.query.count())
print(Movie.query.get(1))
print(Movie.query.filter_by()