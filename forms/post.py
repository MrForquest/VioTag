from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo, NumberRange, ValidationError
from string import ascii_lowercase, digits, ascii_uppercase


class AddPostForm(FlaskForm):
    img = FileField('Добавьте изображение к вашему посту')
    tags = HiddenField('Теги')
    text = TextAreaField('Добавьте текста к своему посту', validators=[DataRequired()])
    submit = SubmitField('Создать')


class SearchForm(FlaskForm):
    tags = HiddenField('Теги')
    text = TextAreaField('Что должен содержать текст?')
    submit = SubmitField('Найти')
