from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('Study.html')

@app.route('/test')
def test():
    return render_template("sample.html")

@app.route('/<path>')
def exercise(path):
    return render_template(f'{path}.html')


if __name__ == '__main__':
    app.run()
