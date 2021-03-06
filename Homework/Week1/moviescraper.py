#!/usr/bin/env python
# Name: Jelle Westerbos
# Student number: 10755470
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    # extract data per movie
    movies = dom.find_all('div', class_ = 'lister-item mode-advanced')

    # list to store scraped data
    movielist = []

    for movie in movies:

        # append extracted data to this dict
        moviedict = {}

        # scrape titles and add to dict
        moviedict['title'] = movie.h3.a.text

        # scrape ratings and add to dict
        moviedict['rating'] = float(movie.strong.text)

        # scrape year of release and add to dict
        year = movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
        moviedict['year'] = re.findall('\d+', year.text.strip('()'))[0]

        # scrape actors and add to dict
        actors = movie.find_all(href=re.compile("adv_li_st"))
        actorlist = []
        for actor in actors:
            actorlist.append(actor.text)
        actorstring = ', '.join(actorlist)
        moviedict['actors'] = actorstring

        # scrape runtime and add to dict
        moviedict['runtime'] = movie.p.find('span', class_ = 'runtime').text.split(' ')[0]
        movielist.append(moviedict)


    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    return movielist   # REPLACE THIS LINE AS WELL IF APPROPRIATE



def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    fieldnames = ['title', 'rating', 'year', 'actors', 'runtime']
    with open('movies.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in movies:
            writer.writerow(line)


    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
