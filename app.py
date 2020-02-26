from flask import Flask,request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/post/', methods=['POST'])
def accept_user_data():
    print(request.data)
    print(type(request.data))
    a = str(request.data)
    print(a)
    print(type(a))
    return 'thankyou'


#
# if __name__ == '__main__':
#     app.run()
