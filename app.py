from flask import Flask, request
import cardCompilerDbOperations
import authorization
import dbOperations
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/user", methods=["POST"])
def register():
   username = request.form["username"]
   password = request.form["password"]
   group_id = request.form["group_id"]
   try:
    cardCompilerDbOperations.register_contributer(username, password,
                                                   group_id)
   except KeyError:
     return "Group not found", 404
   except ValueError:
      return "Username taken in this group", 409
   return "Contributer Registered", 201


@app.route("/group", methods=["POST"])
def create_group():
  return str(cardCompilerDbOperations.create_group(request.form["group_name"])), 201


@app.route("/card", methods=["POST"])
def add_card():
    session_id = request.headers["session_id"]
    user_id = ""
    try:
        user_id = authorization.get_user_id(session_id)
    except IndexError:
        return "Bad Session", 401
    cardCompilerDbOperations.add_card(request.form["card_text"], user_id)
    return "Card Added", 201

@app.route("/login", methods=["POST"])
def login():
    #WARNING: session_ids do not currently expire!!!
    try:
        return authorization.login(request.form["username"], request.form["password"], request.form["group_id"]), 201
    except Exception as Error:
        print(Error)
        return "Login Failed", 401


@app.route("/cards", methods=["GET"])
def get_all_cards():
   # DEBUG ONLY
   cards=dbOperations.select("*", "cards", "True")
   return str(cards), 200

if __name__ == '__main__':
   app.secret_key='secretivekeyagain'
   app.run(host="127.0.0.1", port=8000, debug=True)