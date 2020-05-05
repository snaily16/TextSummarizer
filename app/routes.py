from flask import render_template,flash, redirect
from app import app
from app.forms import TextForm, UrlForm, PdfForm
from word_frequency import WordFrequency
from text_rank import TextRank
from extractData import url_extract, pdf_extract
from werkzeug import secure_filename

@app.route('/')
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

@app.route('/url', methods=['GET', 'POST'])
def url():
	form = UrlForm()
	if form.validate_on_submit():
		algo = form.algo.data
		url = form.url.data
		num = form.sentences.data

		text = url_extract(url)
		if algo=='Wordfreq':
			obj = WordFrequency(text,num)
		elif algo=='TextRank':
			obj = TextRank(text,num)

		return render_template('url_input.html', title='URL', 
			results = obj.summarize_text(), form=form)
	return render_template('url_input.html', title='URL', form=form)

@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
	form = PdfForm()
	if form.validate_on_submit():
		algo = form.algo.data
		num = form.sentences.data
		filename = secure_filename(form.files.data.filename)
		form.files.data.save('uploads/'+filename)
		
		text = pdf_extract('uploads/'+filename)
		if algo=='Wordfreq':
			obj = WordFrequency(text,num)
		elif algo=='TextRank':
			obj = TextRank(text,num)
		return render_template('pdf_input.html', title='PDF', 
			results = obj.summarize_text(), form=form)
	return render_template('pdf_input.html', title='PDF', form=form)
