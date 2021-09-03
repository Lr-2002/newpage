from app import Movie
movie = Movie.query.first()

print(movie.title,movie.year) 
