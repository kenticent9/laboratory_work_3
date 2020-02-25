from flask import Flask, request, render_template, url_for, redirect

from main import create_map, read_data

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    if request.method == 'POST':
        username = request.form['username']
        try:
            create_map(read_data(username))
            return redirect(url_for('friends_map'))
        except:
            return redirect(url_for('index'))


@app.route('/map', methods=['GET'])
def friends_map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run()
