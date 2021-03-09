# import libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import requests

# setup flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)

# request parameter
cafe_parameter = {
    "api-key": "TopSecretAPIKey"
}

# request header
req_header = {
    "Content-Type": "application/json"
}


# form to add a new cafe
class CafeForm(FlaskForm):

    cafe = StringField(label="Cafe Name", validators=[DataRequired()])
    location = StringField(label="Cafe City", validators=[DataRequired()])
    map = StringField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open_time = StringField(label="Opening Time e.g. 8AM", validators=[DataRequired()])
    close_time = StringField(label="Closing Time e.g. 5:30PM", validators=[DataRequired()])

    image = StringField(label="Cafe Image (URL)", validators=[DataRequired(), URL()])
    coffee_price = StringField(label="Coffee Price", validators=[DataRequired()])
    seats = StringField(label="Number of Seats", validators=[DataRequired()])

    wifi = SelectField(label="Is WiFi Available?", choices=["False", "True"], validators=[DataRequired()])
    socket = SelectField(label="Are there Sockets?", choices=["False", "True"], validators=[DataRequired()])
    toilet = SelectField(label="Are there Toilets?", choices=["False", "True"], validators=[DataRequired()])
    phone_call = SelectField(label="Can you take a Phone Call?", choices=["False", "True"], validators=[DataRequired()])

    submit = SubmitField(label="Submit")


# home route
@app.route("/")
def home():
    return render_template("index.html")


# route to render all cafes from API request
@app.route("/cafes")
def cafes():

    all_cafe = requests.get(url="http://127.0.0.1:5000/all")
    all_cafe.raise_for_status()

    cafe_data = all_cafe.json()["cafes"]
    return render_template("cafes.html", cafes=cafe_data)


# route to render a form and make a POST request with the form data to an API
@app.route("/add", methods=["GET", "POST"])
def add_cafe():

    cafe_form = CafeForm()

    if cafe_form.validate_on_submit():

        new_cafe = requests.post(url="http://127.0.0.1:5000/add", json=cafe_form.data, headers=req_header)
        new_cafe.raise_for_status()

        print()
        print(new_cafe.text)

        return redirect(url_for("cafes"))

    return render_template("add.html", form=cafe_form)


# route to delete a cafe
@app.route("/delete")
def delete_cafe():

    cafe_index = request.args.get("index")

    del_cafe = requests.delete(url=f"http://127.0.0.1:5000//report-closed/{cafe_index}", params=cafe_parameter)
    del_cafe.raise_for_status()

    print()
    print(del_cafe.text)

    return redirect(url_for("cafes"))


# start the front-end application
if __name__ == "__main__":
    app.run(port=5001, debug=True)
