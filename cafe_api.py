# import libraries
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

# setup flask application
app = Flask(__name__)

# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    open_time = db.Column(db.String(250), nullable=False)
    close_time = db.Column(db.String(250), nullable=False)

    def row_to_dict(self):
        # Loop through each column in the data record
        # Create a new dictionary entry
        # where the key is the name of the column
        # and the value is the value of the column
        # using Dictionary Comprehension
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("main.html")


# HTTP GET - Read Random Record
@app.route("/random")
def get_random_cafe():

    all_cafes = Cafe.query.all()
    random_cafe = choice(all_cafes)

    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=random_cafe.row_to_dict())


# HTTP GET - Read All Records
@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()

    cafe_list = [cafe.row_to_dict() for cafe in all_cafes]

    return jsonify(cafes=cafe_list)


# HTTP GET - Search Record by Location
@app.route("/search")
def search_cafe():

    city = request.args.get("loc")

    # Read a particular record by query
    located_cafe = Cafe.query.filter_by(location=city).first()

    if located_cafe:
        return jsonify(cafe=located_cafe.row_to_dict())
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location"
        }), 404


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_new_cafe():

    if request.method == "POST":

        data = request.get_json()

        def convert_str(field):
            """A function that converts a string to a boolean"""

            if data[field] == "True":
                data[field] = True
            elif data[field] == "False":
                data[field] = False

        convert_str("toilet")
        convert_str("wifi")
        convert_str("socket")
        convert_str("phone_call")

        # Create a new record
        new_cafe = Cafe(
            name=data["cafe"],
            map_url=data["map"],
            img_url=data["image"],
            location=data["location"],
            seats=data["seats"],
            has_toilet=data["toilet"],
            has_wifi=data["wifi"],
            has_sockets=data["socket"],
            can_take_calls=data["phone_call"],
            coffee_price=data["coffee_price"],
            open_time=data["open_time"],
            close_time=data["close_time"]
        )

        db.session.add(new_cafe)
        db.session.commit()

        return jsonify(response={
            "Success": "Successfully added the new cafe."
        })


# HTTP PUT/PATCH - Update Record Price
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):

    if request.method == "PATCH":

        cafe_to_update = Cafe.query.get(int(cafe_id))

        if cafe_to_update:

            new_price = request.args.get("new_price")
            cafe_to_update.coffee_price = new_price
            db.session.commit()

            return jsonify(success="Successfully updated the price.")
        else:
            return jsonify(error={
                "Not Found": "Sorry a Cafe with that id was not found in the database"
            }), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):

    if request.method == "DELETE":

        api_key = request.args.get("api-key")

        if api_key == "TopSecretAPIKey":

            # Delete a particular record by primary key
            cafe_to_delete = Cafe.query.get(int(cafe_id))

            if cafe_to_delete:

                db.session.delete(cafe_to_delete)
                db.session.commit()

                return jsonify(success="Successfully deleted the cafe.")
            else:
                return jsonify(error={
                    "Not Found": "Sorry a Cafe with that id was not found in the database"
                }), 404
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api-key"), 403


# start the back-end application
if __name__ == "__main__":
    app.run(debug=True)
