from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.fields import MultipleFileField
from wtforms.validators import DataRequired, url, InputRequired
from flask_wtf.file import FileRequired, FileAllowed
from app.validators import MultiFileAllowed

class TextForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank'), ('TF_IDF', 'TF_IDF')])
	text = TextAreaField('Text', validators=[DataRequired()])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class UrlForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank'), ('TF_IDF', 'TF_IDF')])
	url = URLField('Url', validators=[DataRequired(), url()])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class FileForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank'), ('TF_IDF', 'TF_IDF')])
	files = MultipleFileField('File(s)', validators=[InputRequired() ,MultiFileAllowed(['pdf', 'doc', 'txt', 'epub'])])
	sentences = IntegerField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class DownloadForm(FlaskForm):
	download = SubmitField('Download')
