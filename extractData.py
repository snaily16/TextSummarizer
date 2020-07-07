import os
from bs4 import BeautifulSoup as bs
import textract
import requests
import re

def url_extract(url):
	page = requests.get(url)
	data = page.text
	soup = bs(data,'html.parser')
	text = soup.title.text + " "
	parah = soup.find_all('p')
	for p in parah:
		text += p.text

	return text

def pdf_extract(filenames):
	text = ''
	for file in filenames:
		extracted_text=textract.process('uploads/'+file, method='pdfminer')
		text += extracted_text.decode('utf-8')
	return text