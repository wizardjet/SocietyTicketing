from flask import render_template, url_for, flash, redirect, request
from smiglets import app, db
from smiglets.forms import RegistrationForm, LoginForm, CheckoutForm
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
        if form.membership.data: # checkout member
            return redirect(url_for('checkout', person_email=person.email, item="Membership"))
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# checkout page
@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    item = request.args.get('item')
    person_email = request.args.get('person_email')
    if item == "Membership":
        form = CheckoutForm(data={'email': person_email}) #populate form
        if form.validate_on_submit():
            membership = Membership(person_email=person_email, is_member=True, has_paid=True, library_id=form.library_id.data)
            db.session.add(membership)
            db.session.commit()
            flash(f'Membership added for {form.email.data}!', 'success')
            return redirect(url_for('home'))
        return render_template('checkout.html', title='Checkout', form=form)
    


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