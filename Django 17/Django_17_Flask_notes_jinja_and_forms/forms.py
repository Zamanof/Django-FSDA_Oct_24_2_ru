from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class NoteForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(
            message="Title is required"),
            Length(min = 1,max=200, message="Title must be between 1 and 200 characters")
        ], )
    content = TextAreaField(
        "Content",
        validators=[Optional(), Length(min=1, max=1000, message="Content must be between 1 and 1000 characters")]
    )
    submit = SubmitField("Save")