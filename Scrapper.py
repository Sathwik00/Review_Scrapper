from bs4 import BeautifulSoup           # for parsing HTML file
import requests                         # for retrive data from a webpage
import pandas as pd                     # for structuring data obtained
import numpy as np

class Scrapper:
    def __init__(self, course_url):
        self.reviews_url = course_url+"/reviews"
        self.main_url = "https://www.coursera.org"
        self.reviews = []
        self.ratings = []

    def get_reviews_p(self):
        reviews_p = []
        i = 2
        link_soup = "a"
        link = self.reviews_url
        while link_soup!=None:
          response = requests.get(link)                                     # sending https request
          content = response.content                                        # accessing the contents of response
          soup = BeautifulSoup(content, "html.parser")                      # parsing the contents of the page
          divs = soup.find_all("div", attrs={'class':None, 'id':None, 'style':None})              # gets all the divs which contain only <p>...</p>
          for x in divs:                                                    # going through all <div> elemants
            if len(x.find_all('p'))>0:                                      # verifying length of review
              reviews_p.append(x.find_all('p'))
          goto = "Go to page "+str(i)
          link_soup = soup.find('a', attrs = {'aria-label':goto})           # link for next page
          if link_soup != None:
            review_url = link_soup.get("href")
            link = self.main_url+review_url
            i = i+1
        return reviews_p

    def get_reviews(self):
        reviews_p = self.get_reviews_p()
        for review in reviews_p:
          t = ""
          for n in review:
            t+=n.text                   # getting the text in the elements of review
          self.reviews.append(t)

    def get_ratings(self):
        i = 2
        link_soup = "a"
        link = self.reviews_url
        while link_soup!=None:
          response = requests.get(link)
          content = response.content
          soup = BeautifulSoup(content, "html.parser")
          divs = soup.find_all("div", attrs={'role':"img"})
          for x in divs[3:]:                                              # the first 3 elements n each page is not required
            stars = 0
            spans = x.find_all('span')
            for span in spans:
              if span.find_all('svg')[0].text == "Filled Star":
                stars+=1
            self.ratings.append(stars)
          goto = "Go to page "+str(i)
          link_soup = soup.find('a', attrs = {'aria-label':goto})
          if link_soup != None:
            review_url = link_soup.get("href")
            link = self.main_url+review_url
            i+=1

    def get_output(self, form = "dictionary"):
        self.get_reviews()
        self.get_ratings()
        if form == "dictionary":
            return dict(zip(self.reviews, self.ratings))
        elif form == "data frame":
            data = {"review":self.reviews, "rating":self.ratings}
            return pd.DataFrame(data = data)
        else:
            print("Invalid!!!")
            return None
