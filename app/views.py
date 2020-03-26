import flask
import requests
from app import app, socketio
from flask_restful import reqparse, abort, Api, Resource
from collections import OrderedDict
from flask import request, render_template
from flask_socketio import SocketIO, send
import csv

message_queue = []
users = []

parser = reqparse.RequestParser()
@app.route('/')
def sessions():
    return render_template('session.html')

    
def message_received(methods=['GET', 'POST']):    
    print('message receive on server')

@socketio.on('event')
def receive_messages(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))        
    message = json.get('message')   
    if message is not None:     
        if message.find('/') != -1:
            code = message.split('/')        
            message = get_stocks(code[1].split('=')[1])
            if message is not None:
                data = {'user_name': 'bot',
                        'message': message}        
                socketio.emit('response', data, callback=message_received)
        else:
            socketio.emit('response', json, callback=message_received)


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
    
    if price is not None and price != 'N/D':
        return f'{code.upper()} quote is ${price} per share'
    else:
        return None




