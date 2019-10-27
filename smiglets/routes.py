from flask import render_template, url_for, flash, redirect, request
from smiglets import app, db
from smiglets.forms import RegistrationForm, LoginForm, CheckoutForm
from smiglets.models import Smiglet, Membership, Event, Event_Attendee, Event_Guest


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

############################# register page #############################
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        smiglet = Smiglet(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, year_of_study=form.year_of_study.data, course=form.course.data, malaysian=form.malaysian.data)
        membership = Membership(smiglet_email=form.email.data, is_member=form.membership.data)
        db.session.add(smiglet)
        db.session.add(membership)
        db.session.commit()
        if form.membership.data: # checkout member
            return redirect(url_for('checkout', smiglet_email=smiglet.email, item="Membership"))
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

############################# checkout page #############################
@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    item = request.args.get('item')
    smiglet_email = request.args.get('smiglet_email')
    if item == "Membership":
        form = CheckoutForm(data={'email': smiglet_email}) #populate form
        if form.validate_on_submit():
            membership = Membership(smiglet_email=smiglet_email, is_member=True, has_paid=True, id_number=form.library_id.data[:-1])
            db.session.add(membership)
            db.session.commit()
            flash(f'Membership added for {form.email.data}!', 'success')
            return redirect(url_for('home'))
        return render_template('checkout.html', title='Checkout', form=form)

############################# smiglets page #############################
@app.route("/smiglets", methods=['GET', 'POST'])
def smiglets():
    smiglets = Smiglet.query.all()
    return render_template('smiglets.html', smiglets=smiglets)

############################# view smiglet page #############################
@app.route("/smiglet/<string:smiglet_email>", methods=['GET', 'POST'])
def smiglet(smiglet_email):
    smiglet = Smiglet.query.get_or_404(smiglet_email)
    form = RegistrationForm(data={'first_name': smiglet.first_name, 'last_name': smiglet.last_name, 'email': smiglet.email, 'membership': True if smiglet.membership=='Member' else False, 'year_of_study': smiglet.year_of_study, 'course': smiglet.course, 'malaysian': smiglet.malaysian, 'committee': smiglet.committee})
    form.submit.label.text = "Edit"
    if form.is_submitted():
        return redirect(url_for('edit_smiglet', smiglet_email=smiglet_email))
    return render_template('smiglet.html', smiglet=smiglet, form=form, title=f"View {smiglet_email} | SMIG App", editing=False)

############################# edit smiglet page #############################
@app.route("/smiglet/<string:smiglet_email>/edit", methods=['GET', 'POST'])
def edit_smiglet(smiglet_email):
    smiglet = Smiglet.query.get_or_404(smiglet_email)
    form = RegistrationForm(data={'first_name': smiglet.first_name, 'last_name': smiglet.last_name, 'email': smiglet.email, 'membership': True if smiglet.membership=='Member' else False, 'year_of_study': smiglet.year_of_study, 'course': smiglet.course, 'malaysian': smiglet.malaysian, 'committee': smiglet.committee})
    form.submit.label.text = "Update"
    # if form.validate_on_submit():
    # catch if buying membership
    #     return redirect(url_for(''))
    return render_template('smiglet.html', smiglet=smiglet, form=form, title=f"Edit {smiglet_email} | SMIG App", editing=True)

############################# event page #############################


############################# checkout page #############################


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