from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL, Regexp
import csv
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap5(app)

emojis = {
    "x": "✘",
    "coffee": "☕️",
    "wifi": "💪",
    "power": "🔌"
}

coffee_rating_list = []
wifi_rating_list = []
power_rating_list = []

# Populate rating lists for SelectField with score from 0 (default X) to 5
coffee_rating_list = [(index, emojis["coffee"] * index) for index in range(1, 6)]
wifi_rating_list = [(index, emojis["wifi"] * index) for index in range(1, 6)]
wifi_rating_list.insert(0, (0, emojis["x"]))
power_rating_list = [(index, emojis["power"] * index) for index in range(1, 6)]
power_rating_list.insert(0, (0, emojis["x"]))


class CafeForm(FlaskForm):
    name = StringField(label="Cafe name", validators=[DataRequired()])
    cafe_location = URLField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    opening = StringField(label="Opening Time e.g. 8AM",
                          validators=[
                              DataRequired(),
                              Regexp(
                                  regex="^([1-9]|1[0-2]):?(0[0-9]|[1-5][0-9])?\\s?(AM|PM)$",
                                  message="Incorrect format. Correct format: 9PM or 5:30AM")])
    closing = StringField(label="Closing Time e.g. 5:30PM",
                          validators=[
                              DataRequired(),
                              Regexp(
                                  regex="^([1-9]|1[0-2]):?(0[0-9]|[1-5][0-9])?\\s?(AM|PM)$",
                                  message="Incorrect format. Correct format: 9PM or 5:30AM")])
    coffee_rating = SelectField(label="Coffee Rating", choices=coffee_rating_list, validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=wifi_rating_list, validators=[DataRequired()])
    power_socket_rating = SelectField(label="Power Socket Rating", choices=power_rating_list, validators=[DataRequired()])
    submit = SubmitField(label="Submit")


# All Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", encoding="utf-8") as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        cafe_data = []
        for row in csv_reader:
            cafe_data.append(row)
    return render_template("cafes.html", table_data=cafe_data)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline="", encoding="utf-8") as file_data:
            coffee_rating_option = dict(coffee_rating_list).get(int(form.coffee_rating.data))
            wifi_rating_option = dict(wifi_rating_list).get(int(form.wifi_rating.data))
            socket_rating_option = dict(power_rating_list).get(int(form.power_socket_rating.data))
            new_row = [form.name.data,
                       form.cafe_location.data,
                       str(form.opening.data).replace(" ", ""),
                       str(form.closing.data).replace(" ", ""),
                       coffee_rating_option,
                       wifi_rating_option,
                       socket_rating_option]
            writer = csv.writer(file_data)
            writer.writerow(new_row)
            return redirect(url_for("cafes"))
    return render_template("add.html", cafe_form=form)


if __name__ == "__main__":
    app.run(debug=True)
