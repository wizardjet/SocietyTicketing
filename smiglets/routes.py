from flask import render_template, url_for, flash, redirect
from smiglets import app, db
from smiglets.forms import RegistrationForm, LoginForm
from smiglets.models import Person, Membership, Event, Event_Attendee, Event_Guest


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        person = Person(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, year_of_study=form.year_of_study.data, course=form.course.data, malaysian=form.malaysian.data)
        membership = Membership(person_email=form.email.data, is_member=form.membership.data)
        db.session.add(person)
        db.session.add(membership)
        db.session.commit()
        # if form.membership.data: # checkout member
        #     return redirect()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# # checkout page
# @app.route("/checkout", methods=['GET', 'POST'])
# def checkout()


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)