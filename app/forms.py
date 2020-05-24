from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from flask_wtf.file import FileRequired, FileAllowed

class TextForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	text = TextAreaField('Text', validators=[DataRequired()])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class UrlForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	url = URLField('Url', validators=[DataRequired(), url()])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class PdfForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	files = FileField('File', validators=[FileRequired(), FileAllowed(['pdf'], 'PDFs only!')])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class DownloadForm(FlaskForm):
	download = SubmitField('Download')