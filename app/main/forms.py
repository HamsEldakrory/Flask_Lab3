from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField, FloatField, DateField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class book_form(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[DataRequired()])
    publish_date = DateField("Publish Date", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    appropriate_for = SelectField("Appropriate For", choices=[("under 8", "Under 8"),("8-15", "8-15"),("adults", "Adults")], validators=[DataRequired()])
    image = FileField("Book Image", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"], "Images only!")])
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add Book")

class author_form(FlaskForm):
    name = StringField("Author Name", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Add Author")
