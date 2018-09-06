from flask import (Flask,
                  render_template) # render_template_string (특수문자 거르고 표시)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy_statements.html')

if __name__ == '__main__':
    app.run(debug=True)
