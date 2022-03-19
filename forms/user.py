from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField, \
    IntegerField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo, NumberRange, ValidationError
from string import ascii_lowercase, digits, ascii_uppercase


def ascii_check(message=""):
    def _ascii_check(form, field):
        string = field.data.replace("_", "")
        string = string.replace("-", "")
        if not (string.isalnum() and string.isascii()):
            raise ValidationError(f"{message}\n{ascii_lowercase}\n{ascii_uppercase}\n{digits}_-")

    return _ascii_check


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=5, max=30,
                                              message="Имя пользователя должно иметь длину от 5 до 30 символов."),
                                       ascii_check(message=
                                                   "Имя пользователя может содержать только следующие символы:")])
    age = IntegerField('Возраст', validators=[NumberRange(min=5, max=200,
                                                          message="Сожалеем, но мы не можем допустить человека с таким возрастом к нашему сайту")])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   EqualTo("password_again",
                                                           message="Пароли должны совпадать."),
                                                   ascii_check(message=
                                                               "Пароль может содержать только следующие символы:"),
                                                   Length(min=8, max=40,
                                                          message="Пароль должно иметь длину от 8 до 40 символов.")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddWorkForm(FlaskForm):
    job = StringField('Title job', validators=[DataRequired()])
    team_leader = IntegerField('Team leader id', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators')
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
