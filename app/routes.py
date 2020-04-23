from flask import render_template,flash, redirect
from app import app
from app.forms import TextForm
from word_frequency import WordFrequency
from text_rank import TextRank

@app.route('/')
@app.route('/index')
def index():
	user = {'username':'M'}
	return render_template('index.html', title="Home", user=user)

@app.route('/text', methods=['GET', 'POST'])
def text():
	form = TextForm()
	if form.validate_on_submit():
		algo = form.algo.data
		text = form.text.data
		num = form.sentences.data
		if algo=='Wordfreq':
			obj = WordFrequency(text,num)
		elif algo=='TextRank':
			obj = TextRank(text,num)

		return render_template('text_input.html', title='Text', 
			results = obj.summarize_text(), form=form)
	return render_template('text_input.html', title='Text',form=form)