#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author (headers and structure):
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#
# Modified (function logic/bodies) Spring 2022 by:
#   Aaron Quino
#   University of Illinois at Chicago
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, id, title, year):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
  
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, id, title, year, numReviews, avgRating):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating
  
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  
  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, id, title, date, runtime, origLanguage, budget, revenue, numReviews, avgRating, tagline, genres, companies):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = date
    self._Runtime = runtime
    self._Original_Language = origLanguage
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = companies
  
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  
  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property 
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  row = datatier.select_one_row(dbConn, "SELECT count(*) FROM Movies;")
  if row is None:
    return -1
  return row[0]


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  row = datatier.select_one_row(dbConn, "SELECT count(*) FROM Ratings;")
  if row is None:
    return -1
  return row[0]


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """SELECT Movie_ID, Title, strftime('%Y', Release_Date)
           FROM Movies
           WHERE Title like ?
           ORDER BY Title asc;"""
  rows = datatier.select_n_rows(dbConn, sql, [pattern])

  if rows is None:
    return []
  
  movies = []
  for row in rows:
    id = row[0]
    title = row[1]
    year = row[2]
    movies.append(Movie(id, title, year))
  return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  sql = """SELECT Movies.Movie_ID, Title, date(Release_Date), Runtime, Original_Language, Budget, Revenue, Tagline
           FROM Movies
           LEFT JOIN Movie_Taglines on Movies.Movie_ID = Movie_Taglines.Movie_ID
           WHERE Movies.Movie_ID = ?;"""
  row = datatier.select_one_row(dbConn, sql, [movie_id])
  
  if row is ():   # catches if movie does not exist before other queries
    return None
    
  sql = """SELECT count(Rating), round(avg(Rating), 2)
           FROM Ratings
           WHERE Movie_ID = ?"""
  avg_rating_row = datatier.select_one_row(dbConn, sql, [movie_id])

  sql = """SELECT Genre_Name
           FROM Genres
           JOIN Movie_Genres on Genres.Genre_ID = Movie_Genres.Genre_ID
           JOIN Movies on Movie_Genres.Movie_ID = Movies.Movie_ID
           WHERE Movies.Movie_ID = ?
           ORDER BY Genre_Name asc;"""
  genre_rows = datatier.select_n_rows(dbConn, sql, [movie_id])

  sql = """SELECT Company_Name
           FROM Companies
           JOIN Movie_Production_Companies on Companies.Company_ID = Movie_Production_Companies.Company_ID
           JOIN Movies on Movie_Production_Companies.Movie_ID = Movies.Movie_ID
           WHERE Movies.Movie_ID = ?
          ORDER BY Company_Name asc;"""
  companies_rows = datatier.select_n_rows(dbConn, sql, [movie_id])

  id = row[0]
  title = row[1]
  date = row[2]
  runtime = row[3]
  origLanguage = row[4]
  budget = row[5]
  revenue = row[6]
  numRatings = avg_rating_row[0]
  tagline = row[7]
  if tagline == None:     # movie has no tagline
    tagline = ""
  if numRatings == 0:     # there are no ratings to average
    avgRatings = 0
  else:
    avgRatings = avg_rating_row[1]
    
  genres = []
  for row in genre_rows:
    genres.append(row[0])
  companies = []
  for row in companies_rows:
    companies.append(row[0])

  return MovieDetails(id, title, date, runtime, origLanguage, budget, revenue, numRatings, avgRatings, tagline, genres, companies)
  
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  sql = """SELECT Movies.Movie_ID, Title, strftime('%Y',Release_Date), count(Rating), avg(Rating)
           FROM Movies join Ratings on Movies.Movie_ID = Ratings.Movie_ID
           GROUP BY Movies.Movie_ID
           HAVING count(Rating) >= ?
           ORDER BY avg(Rating) desc, count(Rating) desc
           LIMIT ?;"""
  rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  if rows is ():
    return []        # number of reviews may be too high
    
  movie_rating = []
  for row in rows:
    id = row[0]
    title = row[1]
    year = row[2]
    numRatings = row[3]
    avgRatings = row[4]
    movie_rating.append(MovieRating(id, title, year, numRatings, avgRatings))
    
  return movie_rating


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):

  # check if movie exists
  sql = "select * from Movies where Movie_ID = ?"
  row = datatier.select_one_row(dbConn, sql, [movie_id])
  if row is ():
    return 0       # movie does not exist
    
  sql = """INSERT INTO Ratings(Movie_ID, Rating)
           VALUES(?, ?);"""
  retval = datatier.perform_action(dbConn, sql, [movie_id, rating])
  if retval < 0:
    return 0
  return 1

##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  
  # check if movie exists
  sql = "select * from Movies where Movie_ID = ?"
  row = datatier.select_one_row(dbConn, sql, [movie_id])
  if row is ():
    return 0       # movie does not exist

  sql = "select Tagline from Movie_Taglines where Movie_ID = ?"
  row = datatier.select_one_row(dbConn, sql, [movie_id])
  if row is ():     # movie does not have a tagline
    sql = """INSERT INTO Movie_Taglines(Movie_ID, Tagline)
             VALUES(?, ?);"""
    retval = datatier.perform_action(dbConn, sql, [movie_id, tagline])
  else:             # movie has a tagline, so update it
    sql = """UPDATE Movie_Taglines
             SET Tagline = ?
             WHERE Movie_ID = ?"""
    retval = datatier.perform_action(dbConn, sql, [tagline, movie_id])
    
  if retval < 0:     # error in datatier.perform_action
    return 0
  return 1