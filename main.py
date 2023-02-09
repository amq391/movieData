#
# main.py
#
# Presentation tier for program to execute user commands
# to display information from MovieLens database.
#
# Aaron Quino
# University of Illinois at Chicago
# Project 02-03: Presentation-Tier
#
import sqlite3
import objecttier


####################################################################
#
# movie_search
#
# Displays the id, title, and year of release of the movie
# matching the movie name passed in as a parameter. If no 
# movie search returns more than 100 movies, movies are not
# displayed.
#
def movie_search(dbConn):
  print()
  movie_name = input("Enter movie name (wildcards _ and % supported): ")

  movies = objecttier.get_movies(dbConn, movie_name)

  print()
  if movies is None:
    print("# of movies found: 0")
  elif len(movies) > 100:
    print("# of movies found: {}".format(len(movies)))
    print()
    print("There are too many movies to display, please narrow your search and try again...")
    print()
  else:
    print("# of movies found: {}".format(len(movies)))
    print()
    for movie in movies:
      print(movie.Movie_ID,":", movie.Title, "(" + movie.Release_Year + ")")
    print()

    
####################################################################
#
# detailed_movie_search
#
# Displays the id, title, year of release, runtime, 
# original language, budget, revenue, number of reviews, 
# average rating, list of genres, list of production 
# companies, and the tagline of the movie matching the 
# movie name passed in as a parameter. If movie is not
# found in the database, "No such movie..." is output.
#
def detailed_movie_search(dbConn):
  print()
  movie_name = input("Enter movie id: ")

  movie_details = objecttier.get_movie_details(dbConn, movie_name)

  print()
  if movie_details is None:
    print("No such movie...")
  else:
    print(movie_details.Movie_ID, ":", movie_details.Title)
    print("  Release date:", movie_details.Release_Date)
    print("  Runtime:", movie_details.Runtime, "(mins)")
    print("  Orig language:", movie_details.Original_Language)
    print("  Budget:", "$" + f"{movie_details.Budget:,}", "(USD)")
    print("  Revenue:", "$" + f"{movie_details.Revenue:,}", "(USD)")
    print("  Num reviews:", movie_details.Num_Reviews)
    print("  Avg rating:", f"{movie_details.Avg_Rating:.2f}", "(0..10)") 
    genres = "  Genres: "
    for genre in movie_details.Genres:
      genres += genre + ", "
    print(genres)
    companies = "  Production companies: "
    for company in movie_details.Production_Companies:
      companies += company + ", "
    print(companies)
    print("  Tagline:", movie_details.Tagline)
    print()

    
####################################################################
#
# top_N_movies
#
# Displays the top N movies based on their rating and the minimum
# number of reviews given as a parameter. Number of movies 
# and the number of reviews must be > 0. If number of reviews
# given is too high, the user is encouraged to narrow their search.
#
def top_N_movies(dbCnn):
  print()
  num_movies = input("N? ")
  if int(num_movies) <= 0:
    print("Please enter a positive value for N...")
  else:
    min_num_reviews = input("min number of reviews? ")
    if int(min_num_reviews) <= 0:
      print("Please enter a positive value for min number of reviews...")
    else:
      movies = objecttier.get_top_N_movies(dbConn, int(num_movies), int(min_num_reviews))
      if len(movies) != 0:
        print()
        for movie in movies:
          print(movie.Movie_ID, ":", movie.Title, "(" + movie.Release_Year + "),", "avg rating =", f"{movie.Avg_Rating:.2f}", "(" + str(movie.Num_Reviews) + " reviews)")
  print()

  
####################################################################
#
# insert_review
#
# Prompts for new rating (between 0 and 10 inclusive) and 
# movie id to apply the rating to, then adds this new review 
# to the database. If the movie is not found "No such movie..."
# is output.
#
def insert_review(dbConn):
  print()
  new_rating = int(input("Enter rating (0..10): "))
  if new_rating < 0 or new_rating > 10:
    print("Invalid rating...")
  else:
    id = input("Enter movie id: ")
    ret_val = objecttier.add_review(dbConn, id, new_rating)
    print()
    if ret_val == 0:
      print("No such movie...")
    else:
      print("Review successfully inserted")
  print()

  
####################################################################
#
# update_tagline
#
# Prompts for new tagline and movie id to apply the new tagline to,
# then associates this new tagline with the given movie. If the movie 
# is not found "No such movie..." is output. 
#
def update_tagline(dbConn):
  print()
  new_tagline = input("tagline? ")
  id = int(input("movie id? "))
  
  ret_val = objecttier.set_tagline(dbConn, id, new_tagline)
  print()
  if ret_val == 0:
    print("No such movie...")
  else:
    print("Tagline successfully set")
  print()


  
#
# main
#
print('** Welcome to the MovieLens app **')
print()

dbConn = sqlite3.connect('MovieLens.db')

stats = "General stats:\n  # of movies: {}\n  # of reviews: {}\n"
print(stats.format(f"{objecttier.num_movies(dbConn):,}", f"{objecttier.num_reviews(dbConn):,}"))

command = input("Please enter a command (1-5, x to exit): ")

while command !=  "x":
  if command == "1":
    movie_search(dbConn)
  elif command == "2":
    detailed_movie_search(dbConn)
  elif command == "3":
    top_N_movies(dbConn)
  elif command == "4":
    insert_review(dbConn)
  elif command == "5":
    update_tagline(dbConn)
  else:
    print("**Error, unknown command, try again...")
    print()

  command = input("Please enter a command (1-5, x to exit): ")