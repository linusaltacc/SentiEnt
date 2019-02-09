import os
from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
import psycopg2
from flask_session import Session
from flask_migrate import Migrate
from functools import wraps
import requests
import json

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True, static_url_path="", static_folder="static")
app.config.from_pyfile('config.cfg')

app.config['SESSION_FILE_DIR'] = mkdtemp()
Session(app)
con = psycopg2.connect(dbname=app.config['DBNAME'],user=app.config['DBUSER'],host=app.config['HOST'],password=app.config['PASSWORD'])


def execute_db(query,args=()):
    cur = con.cursor()
    cur.execute(query,args)
    con.commit()
    cur.close()
def query_db(query,args=(),one=False):
    cur = con.cursor()
    result=cur.execute(query,args)
    if result>0:
        values=cur.fetchall()
        cur.close()
        return values

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("adminid") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin")==False:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
# Importing Blueprints
from app.views.main import main
# Registering Blueprints
app.register_blueprint(main)