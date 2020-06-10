import flask  # import main Flask class and request object
from flask import request, jsonify
import requests
import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = flask.Flask(__name__)  # create the Flask app
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pages.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model for ORM DB
class pages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String)
    page_url = db.Column(db.String)
    page_traffic = db.Column(db.String)
    page_status = db.Column(db.Integer)
    page_signups = db.Column(db.String)
    page_response_time = db.Column(db.String)

    def __init__(self, page_name, page_url, page_traffic, page_status, page_signups, page_response_time):
        self.page_name = page_name
        self.page_url = page_url
        self.page_traffic = page_traffic
        self.page_status = page_status
        self.page_signups = page_signups
        self.page_response_time = page_response_time


class pagesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'page_name', 'page_url', 'page_traffic', 'page_status', 'page_signups', 'page_response_time')


# init schema
page_schema = pagesSchema()
pages_schema = pagesSchema(many=True)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>LANDING PAGE MANAGER</h1>
    <p>An API for managing and testing landing pages</p>'''


@app.route('/api/v1/pages/all', methods=['GET'])
def api_all():
    all_pages = pages.query.all()
    result = pages_schema.dump(all_pages)
    return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/pages/add_page', methods=['GET', 'POST'])
def api_add_page():
    if request.method == 'POST' and not request.json:  # this block is only entered when the form is submitted
        try:
            page_name = request.form.get('page_name')
            page_url = request.form['url']
            page_traffic = request.form['traffic']
            # Get status code and response time
            r = requests.get(page_url, timeout=6)
            r.raise_for_status()
            page_status = r.status_code
            page_signups = request.form['page_signups']
            page_response_time = str(round(r.elapsed.total_seconds(), 2))
            #Create a new instance of data
            new_page = pages(page_name, page_url, page_traffic, page_status, page_signups, page_response_time)
            db.session.add(new_page)
            db.session.commit()
            return page_schema.jsonify(new_page)
        except:
            conn.rollback()
            msg = "error in insertion operation"
        finally:
            return render_template("result.html",msg = msg)

    if request.json:
        request_data = request.get_json()

    return '''<form method="POST">
                    Page Name: <input type="text" name="page_name"><br>
                    Url: <input type="text" name="url"><br>
                    Traffic: <input type="text" name="traffic"><br>
                    Signups: <input type="text" name="page_signups"><br>
                    <input type="submit" value="Submit"><br>
            </form>'''


@app.route('/api/v1/pages/remove_page', methods=['DELETE'])
def api_delete_page():
    return "rem"


@app.route('/api/v1/pages/page_status/', methods=['GET'])
def api_page_status():
    return "stats"


@app.route('/api/v1/pages/page_traffic', methods=['GET'])
def api_page_traffic():
    return "traf"


@app.route('/api/v1/pages/page_signups', methods=['GET'])
def api_page_signups():
    return "sunps"

    # landing_page = request.args.get('page') #if key doesn't exist, returns None

    # r = requests.get(landing_page, timeout =6)
    # r.raise_for_status()
    # respTime = str(round(r.elapsed.total_seconds(), 2))


# currDate = datetime.datetime.now()
# currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
# print(currDate + " " + respTime)
# return respTime

if __name__ == "__main__":
    app.run(debug=True, port=5000)
