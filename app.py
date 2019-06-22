import flask
from flask import request, redirect, url_for
app = flask.Flask(__name__)


@app.route('/') # this is the main page
def main():
    return flask.render_template('main.html')
    #^^^^ this will render the main.html file
    #in the templates folder

@app.route('/search',methods = ['POST']) # this is an "html form"
def search():
    if request.method == 'POST':
        search_category = request.form['search_category']
        return redirect(url_for('success', name = search_category))

@app.route('/success/<name>') # this will redirect us to a successful search
def success(name): 
   return 'This category is ' + str(len(name))+ 'characters long' + 'welcome %s' % name 


if __name__ == '__main__':
    app.debug=True # this will give us an error message when the app crashes
    app.run()
