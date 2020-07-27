# Crackfic

A fun madlib generator that uses fanfic to create new stories

Generate your own madlibs [here](http://crackfic.herokuapp.com/)!

## How it Works

- **Finding the Fanfic** -  [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to webscrape stories from the popular fanfiction website [Archive of Our Own](https://archiveofourown.org/), also known as AO3
- **Creating the Madlib** - the [NLTK](https://www.nltk.org/) part-of-speech tagger to identify word categories and process inputted language
- **Putting it All Together** - [Flask](https://flask.palletsprojects.com/en/1.1.x/), a python web framework, to connect and deploy all the modules, and display the "madlibified" story based on the user's input

## License
[Apache](https://choosealicense.com/licenses/apache-2.0/)
