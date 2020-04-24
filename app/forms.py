from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired

class TextForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	text = TextAreaField('Text', validators=[DataRequired()])
	sentences = StringField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class UrlForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	url = StringField('Url', validators=[DataRequired()])
	sentences = StringField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')

class PdfForm(FlaskForm):
	algo = SelectField('Choose Algorithm', choices=[('Wordfreq','Word Frequency'), ('TextRank','Text Rank')])
	files = FileField('File')
	sentences = StringField('Number of sentences', validators=[DataRequired()])
	submit = SubmitField('Submit')