from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from app import people

app = Flask(__name__)
app.debug=True

@app.route("/",methods=['GET','POST'])
def app1():
    return("run to deploy model")

@app.route('/run',methods=['GET','POST'])
def run_model():
  people()
  return("done")

app.run()