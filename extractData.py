import os
from bs4 import BeautifulSoup as bs
import textract
import requests
import re

def url_extract(url):
	page = requests.get(url)
	data = page.text
	soup = bs(data)
	text = soup.title.text + " "
	parah = soup.find_all('p')
	for p in parah:
		text += p.text

	return text

def pdf_extract(filename):
	extracted_text=textract.process(filename,method='pdfminer')
	extracted_text = extracted_text.decode('utf-8')
	return extracted_text