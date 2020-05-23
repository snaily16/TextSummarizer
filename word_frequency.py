from collections import Counter
import heapq
import nltk
import re

class WordFrequency:

	def  __init__(self, text, num):
		self.text = text
		self.num = int(num)
		self.ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc'}
		self.stopwords = nltk.corpus.stopwords.words('english')

	def word_sent_tokenizer(self,text):
		tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
		words = tokenizer.tokenize(text)
		sentences = nltk.sent_tokenize(text)
		return words, sentences
  
	def create_wordfrequency(self,words):
		word_freq = {}
		for k in words:
			if k not in self.stopwords:
				if k in word_freq:
					word_freq[k]+=1
				else:
					word_freq[k]=1
		max_freq = max(word_freq.values())
		for w in word_freq.keys():
			word_freq[w] = (word_freq[w]/max_freq)
		return word_freq

	def maxWordFreq(self,word_freq):
		#Wordmax = max(word_freq, key=word_freq.get)
		#return Wordmax
		count = Counter(word_freq)
		top = count.most_common(2)
		wordmax= ''
		for k in top:
			wordmax += k[0] +' '
		return wordmax

	def score_sentences(self, sentences,word_freq):
		sent_freq=dict()
		for s in sentences:
			word, _ = self.word_sent_tokenizer(s.lower())
			num_words = len(word)
			#print(s, type(s))
			if num_words>0:
				for w in word:
					if w not in self.stopwords:
						if s in sent_freq:
							sent_freq[s]+=word_freq[w]
						else:
							sent_freq[s]=word_freq[w]

				if s in sent_freq:
					sent_freq[s]=sent_freq[s]/num_words
		return sent_freq

	def clean_text(self):
		#cleaning
		cleaned_text = re.sub(r'\[[0-9]*\]','',self.text)
		cleaned_text=cleaned_text.lower()
		return cleaned_text

	def generate_summary(self, text):

		#print(text)
		words, sentences = self.word_sent_tokenizer(text)
		word_frequency = self.create_wordfrequency(words)
		sentence_scores = self.score_sentences(sentences, word_frequency)
		result = heapq.nlargest(self.num, sentence_scores, key=sentence_scores.get)
		maxWord = self.maxWordFreq(word_frequency)
		#print(maxWord)
		summary = ''
		for i in result:
			summary += ' '+i.capitalize()
		return summary, maxWord.upper()

	def summarize_text(self):
		# if query in text form
		text = self.clean_text()
		summary, title = self.generate_summary(text)
		#print(summary)
		return text, title, summary