from flask import render_template,flash, redirect, send_from_directory
from app import app
from app.forms import TextForm, UrlForm, PdfForm, DownloadForm
from word_frequency import WordFrequency
from text_rank import TextRank
from extractData import url_extract, pdf_extract
from werkzeug import secure_filename

@app.route('/')
@app.route('/text', methods=['GET', 'POST'])
def text():
	form = TextForm()
	dform = DownloadForm()
	if form.validate_on_submit():
		algo = form.algo.data
		text = form.text.data
		num = form.sentences.data
		result = select_algorithm(algo, text, num)

		return render_template('text_input.html', title='Text', 
			results = result, form=form, dform=dform)
	return render_template('text_input.html', title='Text',form=form)

@app.route('/url', methods=['GET', 'POST'])
def url():
	form = UrlForm()
	dform = DownloadForm()

	if form.validate_on_submit():
		algo = form.algo.data
		url = form.url.data
		num = form.sentences.data

		text = url_extract(url)
		result = select_algorithm(algo, text, num)

		return render_template('url_input.html', title='URL', 
			results = result, form=form, dform=dform)

	return render_template('url_input.html', title='URL', form=form)

@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
	form = PdfForm()
	dform = DownloadForm()
	if form.validate_on_submit():
		algo = form.algo.data
		num = form.sentences.data
		filename = secure_filename(form.files.data.filename)
		form.files.data.save('uploads/'+filename)
		
		text = pdf_extract('uploads/'+filename)
		result = select_algorithm(algo, text, num)

		return render_template('pdf_input.html', title='PDF', 
			results = result, form=form, dform=dform)
	return render_template('pdf_input.html', title='PDF', form=form)

def select_algorithm(algo, text, num):
	if algo == 'Wordfreq':
		obj = WordFrequency(text,num)
	elif algo == 'TextRank':
		obj = TextRank(text,num)
	return obj.summarize_text()

#def download_file():
#	filename = 'summary.pdf'
#	file_dir = 'files'
#	return send_from_directory(file_dir, filename=filename))