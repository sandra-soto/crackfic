import storyscrape as sc
import flask
import random
from flask import request, redirect, url_for, jsonify, render_template, session
import madlib as ml
app = flask.Flask(__name__)
app.secret_key = 'huh'

import subcateg_list

@app.route('/') # this is the main page
def main():
    return flask.render_template('main.html')
    #^^^^ this will render the main.html file
    #in the templates folder

@app.route('/search',methods = ['GET','POST']) # this is an "html form"
def search():
    if request.method == 'POST':
        search_category = request.form['searcher']
        return redirect(url_for('success', name = search_category.replace(" ", "").lower()))
    elif request.method == 'GET':
        return render_template('main.html')

@app.route('/<name>', methods = ['GET','POST']) # this will redirect us to a successful search
def success(name):
    if request.method == 'GET':
        category_list_str = f'subcateg_list.{name}_subcateg'
        category_list = eval(category_list_str)
        return render_template('inside_main_category.html',category_list = category_list)
    elif request.method == 'POST':   
        fandom_selection = request.form['subcategory']
        fandom_selection = fandom_selection.replace('/',' ')
        session['fandom'] = fandom_selection
        return redirect(url_for('madlib', fandom = session['fandom']))

@app.route('/madlib/<fandom>', methods = ['GET', 'POST'])
def madlib(fandom):
    if request.method == 'GET':
        session['fandom'] = fandom
        session['story'] = sc.random_story_in_page(fandom)
        session['msg'], session['num_changes'], session['pos_list'], session['tokens'] = ml.madlib_out(session['story'])
        return render_template('madlib.html',rand = session['num_changes']) #creates random number of input boxes from 1-20
    if request.method == 'POST':
        fandom = session['fandom']
        session["word_list"] = request.form.getlist('input_text[]') #lowkey dont know if this works but lmao
        return redirect(url_for('testinputs', fandom=fandom, words=session["word_list"]))
            
@app.route('/why/<fandom>/<words>')
def testinputs(fandom, words):
    madlib =  ml.madlib_done(session["word_list"],session['num_changes'], session['pos_list'], session['tokens'])
    session.clear()
    return madlib


if __name__ == '__main__':
    app.debug=True # this will give us an error message when the app crashes
    app.run()
