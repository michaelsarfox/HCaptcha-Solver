import hcaptcha
import handler
import logging
import atexit
import signal
import flask

captcha_handler = handler.Handler()
app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/create_instance/", methods = ["POST"])
def create_instance():
    json_data = flask.request.json
    if not captcha_handler.is_browser_launched() and captcha_handler.launch_hsw_browser(json_data.get("captcha_url")) and captcha_handler.set_captcha_data(json_data.get("site_key"), json_data.get("site_host"), json_data.get("is_invisible")):
        return flask.jsonify({"message": "Successfully created captcha instance"})
    return flask.jsonify({"message": "Instance already created or invalid captcha data"})

@app.route("/get_hsw/", methods = ["GET"])
def get_hsw():
    if captcha_handler.is_browser_launched():
        token = captcha_handler.hsw_browser.generate_hsw(flask.request.args.get("jwt"))
        if token:
            return flask.jsonify({"data": token})
    print("[ERROR]: HSW browser is not launched \n")
    return flask.Response(status = 401)

@app.route("/solve/", methods = ["POST"])
def solve():
    if captcha_handler.is_browser_launched():
        for _ in range(10):
            captcha = hcaptcha.HCaptcha(captcha_handler.site_key, captcha_handler.site_host)
            token = captcha.solve()
            if token:
                return flask.jsonify({"data": token})
    return flask.Response(status = 401)

if __name__ == "__main__":
    atexit.register(captcha_handler.kill_browser)
    signal.signal(signal.SIGINT, captcha_handler.cleanup_handler)
    app.run(debug=True, use_reloader=False)
