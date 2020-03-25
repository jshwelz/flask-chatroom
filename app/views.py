import flask
import requests
from app import app, socketio
from flask_restful import reqparse, abort, Api, Resource
from collections import OrderedDict
from flask import request, render_template
from flask_socketio import SocketIO
import csv


STORE = {
    'john': {
        "user": "john",
        "ts": 1552479073,
        "cumulative_distance": 15560,
        "cumulative_time":  193910,
        "average_speed":0.08024341189
    },
    'peter':{
        "user": "Peter",
        "ts": 1552479066,
        "cumulative_distance": 14520,
        "cumulative_time":  215910,
        "average_speed":0.08024341189
    }    
}

parser = reqparse.RequestParser()
@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/users/', methods=['GET'])
def fetch_user():    
    return str(STORE)    
    

def messageReceived(methods=['GET', 'POST']):    
    print('message receive on server')

@socketio.on('event')
def queue_messages(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))        
    message = json.get('message')
    print(message)
    if message.find('/') != -1:
        code = message.split('/')        
        message = get_stocks(code[1].split('=')[1])
        data = {'user_name': 'bot',
                'message': message}
        socketio.emit('response', data, callback=messageReceived)
    else:
        socketio.emit('response', json, callback=messageReceived)
    
    


# /stock=stock_code
@app.route('/stock', methods=['GET'])
def get_stocks(code):            
    URL = 'https://stooq.com/q/l/'        
    PARAMS = {'s': code,'f':'sd2t2ohlcv','e':'csv'}       
    price = None
    try:
        r = requests.get(url = URL, params = PARAMS)          
        decoded_content = r.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')        
        my_list = list(cr)                
        price = my_list[0][6]
    except Exception as ex:        
        print(ex)
  
    if price is not None:
        return f'{code.upper()} quote is ${price} per share'
    else:
        return None
    # if username not in STORE:
    #     flask.abort(404,'User not found')        
    # else:
    #     STORE.update({username:{'user': username, 'ts':args['ts'], 'cumulative_distance':args['distance'],
    #         'cumulative_time':args['time']}})
    #     return str(STORE[username])



