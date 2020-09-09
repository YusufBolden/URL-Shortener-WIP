from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print 'Hello world I am running!'
    return 'Hello World!\n'

# Shortening path (i.e. hit this path when we want to shorten a new URL)
@app.route('/s')
def shorten():
    print 'Printing from the shortened path!'
    return 'URL shortening not yet available!\n'

# Redirection path (i.e. hit this path when we should be redirected by a shortened URL)
@app.route('/r/<shortened>')
def redirect(shortened):
    print 'Printing from the redirecting path! The parameter is %s' % shortened
    # Take shortened variable and look it up in the database
    # if (found_in_db) {
    #   redirect to the original URL
    # else
    #   return error message akin to url NOT_FOUND
    return 'URL redirecting for %s not yet available!\n' % shortened
