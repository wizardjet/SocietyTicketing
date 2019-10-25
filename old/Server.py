from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

YEAR_OF_STUDY = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Foundation", "Masters", "PhD"]

class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(), Email(message='I don\'t like your email.')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=10), AnyOf(['secret', 'password'])])
    year = SelectField('Year of Study', YEAR_OF_STUDY)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		return 'Form Successfully Submitted!'
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)