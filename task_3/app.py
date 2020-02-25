from flask import Flask, request, render_template, url_for, redirect

from main import create_map, read_data

app = Flask(__name__)


@app.route("/", methods=['get', 'post'])
def index():
    if request.method == 'get':
        return render_template("index.html")

    if request.method == 'post':
        username = request.form['username']
        create_map(read_data(username))
        return redirect(url_for('friends_map'))


@app.route('/map', methods=['get'])
def friends_map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run()
