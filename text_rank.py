from collections import Counter
import nltk
from nltk.cluster.util import cosine_distance
import re
import numpy as np

class TextRank:

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
		count = Counter(word_freq)
		top = count.most_common(2)
		wordmax= ''
		for k in top:
			wordmax += k[0] +' '
		return wordmax

	def pagerank(self, A, eps=0.0001, d=0.85):
		P = np.ones(len(A))/len(A)
		while True:
			new_P = np.ones(len(A)) * (1-d) / len(A) + d* A.T.dot(P)
			delta = abs(new_P - P).sum()
			if delta <= eps:
				return new_P
			P = new_P

	def sentence_similarity(self,sent1, sent2):
	    
	    sent1 = [w.lower() for w in sent1]
	    sent2 = [w.lower() for w in sent2]
	    
	    all_words = list(set(sent1+sent2))
	    vec1 = [0]*len(all_words)
	    vec2 = [0]*len(all_words)
	    
	    # vector for first sentence
	    for w in sent1:
	        if w in self.stopwords:
	            continue
	        vec1[all_words.index(w)] += 1
	        
	    # vector for second sentence
	    for w in sent2:
	        if w in self.stopwords:
	            continue
	        vec2[all_words.index(w)] += 1
	        
	    return 1-cosine_distance(vec1, vec2)

	def build_similarity_matrix(self,sentences):
	    # create an empty matrix
	    S = np.zeros((len(sentences), len(sentences)))
	    
	    for idx1 in range(len(sentences)):
	        for idx2 in range(len(sentences)):
	            if idx1==idx2:
	                continue
	            S[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2])
	    # normalize the matrix row-wise
	    for idx in range(len(S)):
	        S[idx] /= S[idx].sum()
	    return S

	def clean_text(self):
		#cleaning
		cleaned_text = re.sub(r'\[[0-9]*\]','',self.text)
		cleaned_text=cleaned_text.lower()
		return cleaned_text

	def generate_summary(self,text):
		words,sentences = self.word_sent_tokenizer(text)
		similarity_matrix = self.build_similarity_matrix(sentences)
		sentence_ranks = self.pagerank(similarity_matrix)
		ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
		selected_sentences = sorted(ranked_sentence_indexes[:self.num])
		summary=''
		for i in selected_sentences:
			summary += ' '+sentences[i].capitalize()
		word_frequency = self.create_wordfrequency(words)
		maxWord = self.maxWordFreq(word_frequency)
		return summary, maxWord.upper()

	def summarize_text(self):
		# if query in text form
		text = self.clean_text()
		summary, title = self.generate_summary(text)
		#print(summary)
		return title, summary