from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
from models import User, Record, Base, Data
from status import error, success
from re import fullmatch
from utils import EMAIL_CHECKER_REGEX, get_metadata
from random import randrange
from time import time


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'))
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not (email := data.get("email")):
        return success(error="expected email")

    if not (password := data.get("password")):
        return error(error="expected password")
    
    if not fullmatch(EMAIL_CHECKER_REGEX, email):
        return error(error="bad email")
    
    with Session(engine) as session:
        new_user = User(
            email=email,
            password=password
        )

        try:
            session.add(new_user)
            session.commit()
        except IntegrityError:
            return error(error="user with email is exists")
        
        new_token, new_id = new_user.token, new_user.id

    return success(token=new_token, id=new_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not (email := data.get("email")):
        return error(error="expected email")

    if not (password := data.get("password")):
        return error(error="expected password")
    
    with Session(engine) as session:
        option_user = session.query(User) \
            .filter(User.email == email, User.password == password) \
            .scalar()

    return success(token=option_user.token, id=option_user.id) \
        if option_user else error(error="user isnt exists")


@app.route('/create_record', methods=['POST'])
def create_record():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    start = data.get("start", 0)
    end = data.get("end", 100)
    count = data.get("count", 50)

    if start > end or count > 100000 or count < 1:
        return error(error="unexpected input")
    
    with Session(engine) as session:
        user = session.query(User) \
            .filter(User.token == token) \
            .scalar()
        
        if not user:
            return error(error="user isnt exists")
        
        datas = [Data(value=randrange(start, end)) for _ in range(count)]
        new_record = Record(
            datas=datas,
            user=user
        )
        session.add(new_record)
        session.add_all(datas)
        session.commit()
        new_id = new_record.id

    return success(id=new_id)


@app.route('/get_record', methods=['POST'])
def get_record():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    if (_id := data.get("id")) in (None, ''):
        return error(error="expected id")
    
    offset = max(data.get("offset", 0), 0)
    step = max(data.get("step", 1), 1)
    count = 100 * step

    with Session(engine) as session:
        datas = session.query(Data) \
            .filter(Data.record_id == _id) \
            .offset(offset) \
            .limit(count) \
            .all()
        
        if not datas :
            return success(record=[], is_end=True)
        
        if datas[0].record.user.token != token:
            return error(error="record isnt exists")

        arr = [x.value for x in datas]
    
    return success(
        record=[int(i) for i in arr[::step]], 
        is_end=len(arr) != count
    )


@app.route('/drop_record', methods=['POST'])
def drop_record():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    if (_id := data.get("id")) in (None, ''):
        return error(error="expected id")
    
    with Session(engine) as session:
        record = session.query(Record) \
            .join(User) \
            .filter(User.token == token, Record.user_id == User.id, Record.id == _id) \
            .scalar()[0]
        
        if not record:
            return error(error="record isnt exists")
        
        session.delete(record)
        session.commit()

    return success()


@app.route('/get_records', methods=['POST'])
def get_records():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    with Session(engine) as session:
        records = session.query(Record.id) \
            .join(User) \
            .filter(User.token == token, Record.user_id == User.id) \
            .all()

    return success(records=[i[0] for i in records])


@app.route('/set_record', methods=['POST'])
def set_record():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    if (_id := data.get("id")) in (None, ''):
        return error(error="expected id")
    
    if not (action := data.get("action")):
        return error(error="expected action")
    
    if action not in ['add', 'set', 'del']:
        return error(error="unexpected action")
    
    value = data.get("value")
    index = data.get("index")
    
    with Session(engine) as session:
        record = session.query(Record) \
            .join(User) \
            .filter(User.token == token, Record.user_id == User.id, Record.id == _id) \
            .scalar()
        
        if not record:
            return error(error="record isnt exists")
    
        if action == "add":
            data = Data(value=0, record=record)
            session.add(data)
        elif action == "del":
            if index in (None, ''):
                return error(error="expected index")

            data = session.query(Data) \
                .offset(index) \
                .limit(1) \
                .scalar()
            
            session.delete(data)
        elif action == "set":
            if index in (None, ''):
                return error(error="expected index")
            
            if value in (None, ''):
                return error(error="expected value")
        
            data = session.query(Data) \
                .offset(index) \
                .limit(1) \
                .scalar()
            
            data.value = value

        session.commit()

    return success(index=index, value=value)


@app.route('/get_metadata', methods=['POST'])
def get_metadata_by_record():
    data = request.get_json()
    
    if not (token := data.get("token")):
        return error(error="expected token")
    
    if (_id := data.get("id")) in (None, ''):
        return error(error="expected id")
    
    with Session(engine) as session:
        datas = session.query(Data) \
            .filter(Data.record_id == _id) \
            .all()
        
        if datas[0].record.user.token != token:
            return error(error="record isnt exists")
        
        arr = map(lambda x: x.value, datas)
        
    maxs, mins, average = get_metadata(arr)

    return success(maxs=maxs, mins=mins, average=average)


if __name__ == '__main__':
    app.run()