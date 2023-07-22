from flask import Flask, request, jsonify, send_file
import cardCompilerDbOperations
import authorization
import dbOperations
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
if not os.path.exists("reports"):
   os.mkdir("reports")

@app.route('/user', methods=['POST'])
def register():
   username = request.form['username']
   password = request.form['password']
   group_id = request.form['group_id']
   try:
    cardCompilerDbOperations.register_contributer(username, password,
                                                   group_id)
   except KeyError:
     return 'Group not found', 404
   except ValueError:
      return 'Username taken in this group', 409
   return 'Contributer Registered', 201


@app.route('/group', methods=['POST'])
def create_group():
  return str(cardCompilerDbOperations.create_group(request.form['group_name'])), 201


@app.route('/card', methods=['POST'])
def add_card():
    session_id = request.headers['session_id']
    user_id = ''
    try:
        user_id = authorization.get_user_id(session_id)
    except IndexError:
        return 'Bad Session', 401
    cardCompilerDbOperations.add_card(request.form['card_text'], user_id)
    return 'Card Added', 201

@app.route('/login', methods=['POST'])
def login():
    #WARNING: session_ids do not currently expire!!!
    try:
        return authorization.login(request.form['username'], request.form['password'], request.form['group_id']), 201
    except Exception as Error:
        print(Error)
        return 'Login Failed', 401


@app.route('/cards', methods=['GET'])
def get_all_cards():
   # DEBUG ONLY
   cards=dbOperations.select('*', 'cards', 'True')
   return str(cards), 200

@app.route('/my_cards', methods=['GET'])
def get_my_cards():
    session_id = request.headers['session_id']
    user_id = ''
    try:
      user_id = authorization.get_user_id(session_id)
    except:
       return 'Bad session', 401
    return jsonify(cardCompilerDbOperations.get_my_cards(user_id))

from openpyxl import Workbook
from datetime import datetime
@app.route('/report', methods=['GET, POST'])
def get_report():
    session_id = request.headers['session_id']
    user_id = ''
    try:
      user_id = authorization.get_user_id(session_id)
    except:
       return 'Bad session', 401
    where = f"contributer_id='{user_id}'"
    group_id = dbOperations.select('group_id', 'contributers', where)[0][0]
    join = dbOperations.get_inner_join_expression('cards', 'contributers', 'cards.contributer_id=contributers.contributer_id')
    cards = dbOperations.select('card_text', join, f"group_id='{group_id}'")
    print('cards: ', cards)
    wb = Workbook()
    sheet = wb.active
    for y in range(0,len(cards)):
       sheet['A'+str(y+1)] = cards[y][0]
    now = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    path = f'./reports/{user_id}-{now}.xls'
    wb.save(path)
    return send_file(path, download_name="report.xls", as_attachment=False)

@app.route('/group/<group_id>', methods=["GET"])
def get_group(group_id):
   name = cardCompilerDbOperations.get_group_name(group_id)
   if name is None:
      return "Group not found", 404
   return name, 200