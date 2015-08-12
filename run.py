from flask import Flask

app = Flask("flask demo")

@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	app.run()
