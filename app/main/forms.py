from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from flask_babel import _, lazy_gettext as _l


class PostForm(FlaskForm):
    post = TextAreaField(
        _l('Say something'), 
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField(_l('Submit'))