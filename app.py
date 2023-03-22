'''
Instagram Following Non-followers (v2) -> Instagram Follower Tracker
Created Date: 03/08/23
The Instagram tracker tool allows users to check their Instagram account followings to discover which accounts are not following back.

Created by: Johnson Le
'''

import json
import os
from flask import Flask, render_template, url_for, jsonify, flash, redirect, request, session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from sqlalchemy import true

app = Flask(__name__)
app.config['SECRET_KEY']='johnson'
app.config['UPLOAD_FOLDER']='static/files'

class UploadFileForm(FlaskForm):
    file = FileField("Followers", validators=[InputRequired()])
    file2 = FileField("Following", validators=[InputRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
        file2 = form.file2.data

        # Allows both files called "followers" or "followers_1" to be read
        if file.filename != "followers.json" and file.filename != "followers_1.json":
            flash('Invalid file for Followers.', category='error')
            return redirect(url_for('index'))
        if file2.filename != "following.json":
            flash('Invalid file for Following.', category='error')
            return redirect(url_for('index'))

        else:
            # Reads the contents of the files into memory
            followers_data = json.loads(file.read())
            following_data = json.loads(file2.read())

            # Establishing arrays for each files
            followers_values = []
            followers_link = []
            following_values = []
            following_link = []
            if file.filename == "followers.json":
                # Iterates through the relationships_followers list
                for relationship in followers_data['relationships_followers']:
                    # Iterates through the string_list_data list
                    for string_data in relationship['string_list_data']:
                        # Adds the value to the appropriate values array
                        followers_values.append(string_data['value'])
                        followers_link.append(string_data['href'])

            if file.filename == "followers_1.json":
                # Iterates through the relationships_followers list
                for relationship in followers_data:
                    # Iterates through the string_list_data list
                    for string_data in relationship['string_list_data']:
                        # append the value to the values array
                        followers_values.append(string_data['value'])
                        followers_link.append(string_data['href'])

            # Iterates through the relationships_followers list
            for relationship in following_data['relationships_following']:
                # Iterates through the string_list_data list
                for string_data in relationship['string_list_data']:
                    # Adds the value to the appropriate values array
                    following_values.append(string_data['value'])
                    following_link.append(string_data['href'])

            # Iterates the remaining variables to the arrays
            not_in_followers = []
            not_in_followers_link = []
            for val in following_values:
                if val not in followers_values:
                    not_in_followers.append(val)

            # Displays compilation on results page
            for non_follower in not_in_followers:
                index = following_values.index(non_follower)
                not_in_followers_link.append(following_link[index])
            return render_template('results.html', not_in_followers=not_in_followers, not_in_followers_link=not_in_followers_link)

    return render_template('index.html', form=form)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    return render_template('tutorial.html')


if __name__ == "__main__":
    app.run(debug=True)