from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class esrgan_form(FlaskForm):
    image_file = FileField("Image", validators=[FileAllowed(
        ['jpg', 'jpeg', 'png'], 'Images Only!'), FileRequired()])
    filename = StringField("File Name", validators=[
        validators.InputRequired(), validators.Length(min=1, max=10)])
    upscale = IntegerField("Upscale", validators=[validators.InputRequired()])


class sdxl_form(FlaskForm):
    prompt = StringField("Prompt", validators=[validators.InputRequired()])
    nPrompt = StringField("Negative Prompt")
    filename = StringField("File Name", validators=[
        validators.InputRequired(), validators.Length(min=1, max=10)])
    height = IntegerField("Height", validators=[validators.InputRequired()])
    width = IntegerField("Width", validators=[validators.InputRequired()])


class lcm_form(FlaskForm):
    prompt = StringField("Prompt", validators=[validators.InputRequired()])
    filename = StringField("File Name", validators=[
        validators.InputRequired(), validators.Length(min=1, max=10)])
    height = IntegerField("Height", validators=[validators.InputRequired()])
    width = IntegerField("Width", validators=[validators.InputRequired()])


class codeformer_form(FlaskForm):
    image_file = FileField("Image", validators=[FileAllowed(
        ['jpg', 'jpeg', 'png'], 'Images Only!'), FileRequired()])
    filename = StringField("File Name", validators=[
        validators.InputRequired(), validators.Length(min=1, max=10)])
    upscale = IntegerField("Upscale", validators=[validators.InputRequired()])
