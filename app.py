import subcategory
import flask
from flask import request, redirect, url_for, jsonify, render_template
app = flask.Flask(__name__)


@app.route('/') # this is the main page
def main():
    return flask.render_template('main.html')
    #^^^^ this will render the main.html file
    #in the templates folder

@app.route('/search',methods = ['GET','POST']) # this is an "html form"
def search():
    if request.method == 'POST':
        search_category = request.form['searcher']
        return redirect(url_for('success', name = search_category.lower()))
    elif request.method == 'GET':
        return render_template('main.html')

@app.route('/<name>', methods = ['GET','POST']) # this will redirect us to a successful search
def success(name):
    if request.method == 'GET':
        if name[-1] == "s":
            name = name[:-1]
        category_url = subcategory.main_category(name+'/')
        category_list = subcategory.generate_subs(category_url)
        return render_template('inside_main_category.html',category_list = category_list)
    elif request.method == 'POST':
        if name[-1] == "s":
            name = name[:-1]
        category_url = subcategory.main_category(name+'/')
        category_list = subcategory.generate_subs(category_url)        
        fandom_selection = request.form['subcategory']
        fandom_selection = fandom_selection.replace('/',' ')
        return redirect(url_for('madlib', fandom = fandom_selection))

@app.route('/madlib/<fandom>')
def madlib(fandom):
    return "Welcome  to the madlib page for " + fandom

if __name__ == '__main__':
    app.debug=True # this will give us an error message when the app crashes
    app.run()
