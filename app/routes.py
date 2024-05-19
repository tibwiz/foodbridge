# app/routes.py
from datetime import datetime

from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from app.forms import RegistrationForm, LoginForm,CreateDonationForm
from app.models import DonationItem
import json
from werkzeug.utils import secure_filename
import os
# Create a Blueprint for routes
bp = Blueprint('main', __name__)
@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = form.authenticate_user(username, password)
        print("user", user)
        if user:
            session['user_category'] = user.category
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.listings'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)


@bp.route('/listings')
def listings():
    # Load all donation items and sort them based on expiry date
    donation_items = DonationItem.load_all()
    sorted_items = sorted(donation_items, key=lambda x: x.expiry_date)

    # Get user category from session
    user_category = session.get('user_category')

    return render_template('listings.html', donation_items=sorted_items, user_category=user_category)


@bp.route('/delete_donation', methods=['POST'])
def delete_donation():
    # Get the id of the donation item to delete
    item_id = request.form.get('item_id')

    # Load the donation item
    item = DonationItem.load(item_id)

    # Delete the donation item
    item.delete()

    flash('Donation deleted successfully!', 'success')
    return redirect(url_for('main.listings'))


#create_donation
@bp.route('/create_donation', methods=['GET', 'POST'])
def create_donation():
    form = CreateDonationForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        quantity = form.quantity.data
        location = form.location.data
        contact = form.contact.data
        expiry_date = form.expiry_date.data
        image = form.image.data


        new_id = DonationItem.get_next_id()
        posted_by = 'current_user'  # Replace with actual logic to get the current user's name
        donation_item = DonationItem(
            item_id=new_id,
            posted_by=posted_by,
            claimed_by=None,
            title=title,
            description=description,
            category=category,
            quantity=quantity,
            location=location,
            contact=contact,
            expiry_date="",
            image="filename"
        )

        with open(f'db/items/{new_id}.json', 'w') as f:
            json.dump(donation_item.to_json(), f)

        flash('Donation item created successfully!', 'success')
        return redirect(url_for('main.listings'))

    return render_template('create_donation.html', form=form)
# claim donation
@bp.route('/claim_donation', methods=['POST'])
def claim_donation():
    # Get the id of the donation item to claim
    item_id = request.form.get('item_id')

    # Load the donation item
    item = DonationItem.load(item_id)

    # Update the claimed_by field of the donation item
    item.claimed_by = session.get('username')

    # Save the updated donation item
    item.save()
    print("session.get('username')", session.get('username'))

    flash('Donation claimed successfully!', 'success')
    return redirect(url_for('main.listings'))
