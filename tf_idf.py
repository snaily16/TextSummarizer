from collections import Counter
import re
import numpy as np
import nltk
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize,RegexpTokenizer

class TF_IDF:

	def  __init__(self, text, num):
		self.text = text
		self.num = int(num)
		self.stopwords = nltk.corpus.stopwords.words('english')

	def word_sent_tokenizer(self,text):
		tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
		words = tokenizer.tokenize(text)
		sentences = nltk.sent_tokenize(text)
		return words, sentences

	def create_word_frequency(self, sentences):
	    tokenizer = RegexpTokenizer(r'\w+')
	    
	    freq_table = {}
	    for sentence in sentences:
	        words,_ = self.word_sent_tokenizer(sentence)
	        word_freq = {}
	        for k in words:
	            if k not in self.stopwords:
	                if k in word_freq:
	                    word_freq[k]+=1
	                else:
	                    word_freq[k]=1
	        freq_table[sentence]= word_freq
	                    
	    return freq_table

	def create_tf_matrix(self, freq_table):
	    tf_matrix = {}
	    for sent, word_freq in freq_table.items():
	        tf = {}
	        total_documents = len(word_freq)
	        for word, freq in word_freq.items():
	            tf[word] = freq / total_documents
	        tf_matrix[sent] = tf
	    return tf_matrix

	def calculate_docs_per_words(self, freq_matrix):
	    doc_per_word = {}
	    for sent, word_freq in freq_matrix.items():
	        for word, count in word_freq.items():
	            #word = word.lower()
	            if word in doc_per_word:
	                doc_per_word[word]+=1
	            else:
	                doc_per_word[word]=1
	    return doc_per_word

	def create_idf_matrix(self, freq_matrix, docs_per_word):
	    idf_matrix = {}
	    total_documents = len(freq_matrix)
	    for sent, ftable in freq_matrix.items():
	        idf = {}
	        for word in ftable.keys():
	            idf[word] = np.log(total_documents / float(docs_per_word[word]))
	        idf_matrix[sent] = idf
	    return idf_matrix

	def create_tf_idf_matrix(self, tf_matrix, idf_matrix):
	    tfidf_matrix = {}
	    for (sent, tf_table), (_, idf_table) in zip(tf_matrix.items(), idf_matrix.items()):
	        tfidf = {}
	        for (word,tf), (_,idf) in zip(tf_table.items(), idf_table.items()):
	            tfidf[word] = float(tf*idf)
	        tfidf_matrix[sent] = tfidf
	    return tfidf_matrix

	def score_sentences(self, tfidf_matrix):
	    sentenceValue = {}

	    for sent, tfidf_table in tfidf_matrix.items():
	        total_score_per_sentence = 0

	        words_in_sentence = len(tfidf_table)
	        for word, score in tfidf_table.items():
	            total_score_per_sentence += score

	        sentenceValue[sent] = total_score_per_sentence / words_in_sentence

	    return sentenceValue

	def create_allwordfrequency(self,words):
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
		count = Counter(word_freq)
		top = count.most_common(2)
		wordmax= ''
		for k in top:
			wordmax += k[0] +' '
		return wordmax

	def clean_text(self):
		#cleaning
		cleaned_text = re.sub(r'\[[0-9]*\]','',self.text)
		cleaned_text=cleaned_text.lower()
		return cleaned_text

	def generate_summary(self, text):

		#print(text)
		words, sentences = self.word_sent_tokenizer(text)
		word_frequency = self.create_word_frequency(sentences)
		tf_matrix = self.create_tf_matrix(word_frequency)
		docs_per_word = self.calculate_docs_per_words(tf_matrix)
		idf_matrix = self.create_idf_matrix(tf_matrix, docs_per_word)
		tfidf_matrix = self.create_tf_idf_matrix(tf_matrix, idf_matrix)
		sentence_scores = self.score_sentences(tfidf_matrix)
		result = sorted(sentence_scores, reverse=True)[:self.num]
		

		allword_frequency = self.create_allwordfrequency(words)
		maxWord = self.maxWordFreq(allword_frequency)
		#print(maxWord)
		summary = ''
		print(summary)
		for sent in result:
			summary += ' '+sent.capitalize()
		return summary, maxWord.upper()

	def summarize_text(self):
		# if query in text form
		text = self.clean_text()
		summary, title = self.generate_summary(text)
		#print(summary)
		return text, title, summary