from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
	"""
	Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
	through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
	and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

	[('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
	"""
	fhand = open(filename)
	data = fhand.read()
	fhand.close()
	soup = BeautifulSoup(data, 'html.parser')

	bookList = []
	bookTags = soup.find_all("a", class_="bookTitle")
	for bookTag in bookTags:
		bookList.append(bookTag.text.strip())
	
	authorList = []
	authorTags = soup.find_all('div', class_ = "authorName__container")
	for authorTag in authorTags:
		authorList.append(authorTag.text.strip())

	tupleList = []
	for x in range(len(bookList)):
		tupleList.append((bookList[x], authorList[x]))

	return tupleList


def get_search_links():
	"""
	Write a function that creates a BeautifulSoup object after retrieving content from
	"https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
	URLs for each of the first ten books in the search using the following format:

	['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

	Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
	your list, and , and be sure to append the full path to the URL so that the url is in the format 
	“https://www.goodreads.com/book/show/kdkd".

	"""

	url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	

	urlList = []
	bookTags = soup.find_all("a", class_="bookTitle")
	for bookTag in bookTags[:10]:
		if bookTag.get("href").startswith("/book/show/"):
			urlList.append("https://www.goodreads.com" + bookTag.get("href"))

	return urlList


def get_book_summary(book_url):
	"""
	Write a function that creates a BeautifulSoup object that extracts book
	information from a book's webpage, given the URL of the book. Parse through
	the BeautifulSoup object, and capture the book title, book author, and number 
	of pages. This function should return a tuple in the following format:

	('Some book title', 'the book's author', number of pages)

	HINT: Using BeautifulSoup's find() method may help you here.
	You can easily capture CSS selectors with your browser's inspector window.
	Make sure to strip() any newlines from the book title and number of pages.
	"""

	r = requests.get(book_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	bookTitle = soup.find('h1', id="bookTitle").text.strip()
	authorDiv = soup.find('div', class_="authorName__container")
	bookAuthor = authorDiv.find('span').text.strip()
	pages = int(soup.find('span', itemprop = "numberOfPages").text.strip()[:-6])
	return (bookTitle, bookAuthor, pages)



def summarize_best_books(filepath):
	"""
	Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
	page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
	filepath and return a list of (category, book title, URL) tuples.
	
	For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
	https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
	("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
	to your list of tuples.
	"""
	fhand = open(filepath)
	data = fhand.read()
	fhand.close()
	soup = BeautifulSoup(data, 'html.parser')

	Categories = []
	categoryTags = soup.find_all("h4", class_="category__copy")
	for tag in categoryTags:
		Categories.append(tag.text.strip())
	
	Titles = []
	titleTags = soup.find_all('img', class_="category__winnerImage")
	for tag in titleTags:
		Titles.append(tag.get("alt"))
	
	URLs = []
	divTags = soup.find_all('div', class_="category clearFix")
	for div in divTags:
		urlTag = div.find("a")
		URLs.append(urlTag.get("href"))

	tupleList = []
	for x in range(len(URLs)):
		tupleList.append((Categories[x], Titles[x], URLs[x]))

	return tupleList

def write_csv(data, filename):
	"""
	Write a function that takes in a list of tuples (called data, i.e. the
	one that is returned by get_titles_from_search_results()), writes the data to a 
	csv file, and saves it to the passed filename.

	The first row of the csv should contain "Book Title" and "Author Name", and
	respectively as column headers. For each tuple in data, write a new
	row to the csv, placing each element of the tuple in the correct column.

	When you are done your CSV file should look like this:

	Book title,Author Name
	Book1,Author1
	Book2,Author2
	Book3,Author3
	......

	This function should not return anything.
	"""
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "w") as f:
		writer = csv.writer(f, delimiter=",")
		writer.writerow(["Book Title", "Author Name"])
		for item in data:
			writer.writerow(item)


def extra_credit(filepath):
	"""
	EXTRA CREDIT

	Please see the instructions document for more information on how to complete this function.
	You do not have to write test cases for this function.
	"""
	with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:    
		data = f.read()
	
	soup = BeautifulSoup(data, "html.parser")

	div = soup.find("div", class_="readable stacked")
	description = div.find("span", id="freeText4791443123668479528").text.strip()

	regex = r"\b[A-Z]\w.\w+(?:\s[A-Z]\w+)+"
	NameEntities = []
	NameEntities.extend(re.findall(regex, description))
	
	return NameEntities

class TestCases(unittest.TestCase):

	# call get_search_links() and save it to a static variable: search_urls
	search_urls = get_search_links()

	def test_get_titles_from_search_results(self):
		# call get_titles_from_search_results() on search_results.htm and save to a local variable
		tupleList = get_titles_from_search_results("search_results.htm")
		# check that the number of titles extracted is correct (20 titles)
		self.assertEqual(len(tupleList), 20)
		# check that the variable you saved after calling the function is a list
		self.assertEqual(type(tupleList), list)
		# check that each item in the list is a tuple
		for x in tupleList:
			self.assertEqual(type(x), tuple)
		# check that the first book and author tuple is correct (open search_results.htm and find it)
		self.assertEqual(tupleList[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
		# check that the last title is correct (open search_results.htm and find it)
		self.assertEqual(tupleList[19], ("Harry Potter: The Prequel (Harry Potter, #0.5)", "Julian Harrison (Introduction)"))

	def test_get_search_links(self):
		# check that TestCases.search_urls is a list
		self.assertEqual(type(TestCases.search_urls), list)
		# check that the length of TestCases.search_urls is correct (10 URLs)
		self.assertEqual(len(TestCases.search_urls), 10)
		# check that each URL in the TestCases.search_urls is a string
		# check that each URL contains the correct url for Goodreads.com followed by /book/show/
		for url in TestCases.search_urls:
			self.assertEqual(type(url), str)
			self.assertTrue(url.startswith("https://www.goodreads.com/book/show/"))

	def test_get_book_summary(self):
		# create a local variable – summaries – a list containing the results from get_book_summary()
		# for each URL in TestCases.search_urls (should be a list of tuples)
		summaries = []
		for url in TestCases.search_urls:
			summaries.append(get_book_summary(url))
		# check that the number of book summaries is correct (10)
		self.assertEqual(len(summaries), 10)
		# check that each item in the list is a tuple
		# check that each tuple has 3 elements
		# check that the first two elements in the tuple are string
		# check that the third element in the tuple, i.e. pages is an int
		for summary in summaries:
			self.assertEqual(type(summary), tuple)
			self.assertEqual(len(summary), 3)
			self.assertEqual(type(summary[0]), str)
			self.assertEqual(type(summary[1]), str)
			self.assertEqual(type(summary[2]), int)
		# check that the first book in the search has 337 pages
		self.assertEqual(summaries[0][2], 337)

	def test_summarize_best_books(self):
		# call summarize_best_books and save it to a variable
		tupleList = summarize_best_books("best_books_2020.htm")
		# check that we have the right number of best books (20)
		self.assertEqual(len(tupleList), 20)
		# assert each item in the list of best books is a tuple
		# check that each tuple has a length of 3
		for x in tupleList:
			self.assertEqual(type(x), tuple)
			self.assertEqual(len(x), 3)
		# check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
		self.assertEqual(tupleList[0], ("Fiction", "The Midnight Library", "https://www.goodreads.com/choiceawards/best-fiction-books-2020"))
		# check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
		self.assertEqual(tupleList[19], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

	def test_write_csv(self):
		# call get_titles_from_search_results on search_results.htm and save the result to a variable
		tupleList = get_titles_from_search_results("search_results.htm")
		# call write csv on the variable you saved and 'test.csv'
		write_csv(tupleList, "test.csv")
		# read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
		fhand = open("test.csv", "r")
		csv_reader = csv.reader(fhand)
		csv_lines = []
		for i in csv_reader:
			csv_lines.append(i)
		fhand.close()
		# check that there are 21 lines in the csv
		self.assertEqual(len(csv_lines), 21)
		# check that the header row is correct
		self.assertEqual(csv_lines[0], ["Book Title" , "Author Name"])
		# check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
		self.assertEqual(csv_lines[1], ["Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"])
		# check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
		self.assertEqual(csv_lines[-1], ["Harry Potter: The Prequel (Harry Potter, #0.5)", "Julian Harrison (Introduction)"])		

if __name__ == '__main__':
	print(extra_credit("extra_credit.htm"))
	unittest.main(verbosity=2)