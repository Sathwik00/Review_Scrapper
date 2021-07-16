from Scrapper import Scrapper
course_url = "https://www.coursera.org/learn/python-crash-course"
scrapper = Scrapper(course_url)
data_dictionary = scrapper.get_output("dictionary")
data_df = scrapper.get_output("data frame")
