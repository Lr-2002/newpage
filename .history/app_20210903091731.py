from flask import Flask

app = Flask(__name__)

@app.route('/my-app')
def hello():
    return 'Welcome to My home'


# if __name__ == '__main__':
#     app.run()