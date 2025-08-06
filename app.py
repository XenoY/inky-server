from flask import Flask, send_file
from render.wortuhr import Wortuhr
from render.calendar import Calendar

app = Flask(__name__)

@app.route('/image/calendar')
def get_calendar():
    calendar = Calendar()
    calendar.render_image()
    return send_file(calendar.image_file)

@app.route('/view/calendar')
def view_calendar():
    calendar = Calendar()
    calendar.build_html()
    return send_file(calendar.html_file)

@app.route('/image/wortuhr')
def get_wortuhr():
    wortuhr = Wortuhr()
    wortuhr.render_image()
    return send_file(wortuhr.image_file)

@app.route('/view/wortuhr')
def view_wortuhr():
    wortuhr = Wortuhr()
    wortuhr.build_html()
    return send_file(wortuhr.html_file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)