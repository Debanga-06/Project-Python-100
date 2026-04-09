from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Update Profile")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(5, 200)])
    summary = StringField("Summary", validators=[Optional(), Length(max=300)])
    content = TextAreaField("Content", validators=[DataRequired()])
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    tags = StringField("Tags (comma-separated)", validators=[Optional()])
    is_published = BooleanField("Publish Now")
    submit = SubmitField("Save Post")


class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired(), Length(1, 1000)])
    submit = SubmitField("Post Comment")
