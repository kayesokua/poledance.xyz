from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class NewDancePost(FlaskForm):
    title = StringField('Title', validators=[Length(max=128)])
    description = TextAreaField('Description')
    instruction = TextAreaField('Instruction')
    ai_instruction = BooleanField('Generate Instructions?', render_kw={"disabled": True})
    filename = FileField('Upload Video', validators=[FileRequired(), FileAllowed(['mp4'], 'MP4 videos only!')])
    submit = SubmitField('Submit')

class EditDancePost(FlaskForm):
    title = StringField('Title', validators=[Length(max=128)])
    description = TextAreaField('Description')
    instruction = TextAreaField('Instruction')
    ai_instruction = BooleanField('Generate Instructions?', render_kw={"disabled": True})
    deleted = BooleanField('Delete Post?')
    submit = SubmitField('Submit')