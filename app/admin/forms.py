from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, FileField, SelectField


class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired()])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class RequestReset(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired()])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=[(
        'web', 'web'), ('mobile', 'mobile'), ('desktop', 'desktop'), ('photo', 'photo'), ('video', 'video')])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


#    def validate_email(self, email):
#        user = User.query.filter_by(email=email.data).first()
#        if user is None:
#            raise ValidationError('There is no account with that email. You must register first.')

class EmailForm(FlaskForm):
    sndr_email = StringField("Sender Email", description="Please enter your email address", default="shot@dikedim.com")
    rcpt_email = StringField("Recipient Email", validators=[DataRequired("Please enter recipient email address")])
    cc = StringField("cc", description="copy address")
    bcc = StringField("bcc", description="blind copy addresses")
    dummy = StringField("dummy")
    attachment = FileField("attachments")
    subject = StringField("Subject", validators=[DataRequired("Please enter a subject")])
    message1 = TextAreaField("Message")
    submit = SubmitField("Send Message")


class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('link')
    category = StringField('Category', validators=[DataRequired()])
    content = TextAreaField('Content')
    photo = FileField("attachments")

    submit = SubmitField('Post')
