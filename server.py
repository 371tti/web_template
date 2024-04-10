from flask import Flask ,session ,g ,render_template ,request ,jsonify ,send_file ,Response ,abort

from flask_socketio import SocketIO , emit
import threading


from datetime import timedelta 
from datetime import datetime
import mimetypes
import time


import session as Sin


import os ,json ,re




app = Flask(__name__)
sin = Sin.SESSION()



#sessionの設定
app.secret_key = 'u9t2W*.(7CZBN~a2wb+kzAFC+n*M-HM|'

app.permanent_session_lifetime = timedelta(days=365)



socketio = SocketIO(app)



base_path = r"//TRUENAS/route/D/web_dev/idis_v2/users/"


@app.route('/favicon.ico')
def favicon():
    return send_file(base_path + "root/favicon.ico")


@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')


@app.route('/ads.txt')
def ads():
    return render_template('ads.txt')


@app.before_request
def before_request(): 
    g.reqest_time = time.time()

    sins = sin.ref_session(session.get('id'),session.get('key'))
    session['id'] = sins[0]
    session['key'] = sins[1]

    g.q_date = {"""いろいろユーザー名とかセッション情報を格納しようぜ"""}

    g.user = "@everyone"

    pass


@app.after_request
def after_request(response):

    run_time = time.time() - g.reqest_time
    
    request_info = {
        'time': datetime.now().strftime("%Y.%m/%d %H:%M-%S"),
        'run_time':run_time,
        'ip': request.remote_addr,
        'method': request.method,
        'path': request.path,
        'user-agent': request.headers.get('User-Agent'),
        'status_code': response.status_code,
        'content_type': response.content_type,
        'content_size': response.content_length
    }
    print(json.dumps(request_info, indent=4, ensure_ascii=False))
    return response


@app.teardown_request
def teardown_request(exception):
    pass


@app.errorhandler(Exception)
def errorhandler(err):

    app.logger.error('An error occurred', exc_info=True)
    
    code = 500
    if hasattr(err, 'code'):
        code = err.code

    debug = {
        'Host' : request.headers.get('Host'),
        'Path' : request.path,
        'Connection' : request.headers.get('Connection'),
        'User-Agent' : request.headers.get('User-Agent'),
        'Last-Time' : datetime.now().strftime("%Y.%m/%d %H:%M:%S.%f") ,
        'Cf-Connecting-Ip' : request.headers.get('Cf-Connecting-Ip'),
        'Accept-Encoding' : request.headers.get('Accept-Encoding'),
        'Accept-Language' : request.headers.get('Accept-Language')
    }
    return render_template("ERRN.html",code=code,ms = extended_error_handling[code] + (f" - {err.description}" if hasattr(err , 'description') and err.description else "") ,solution = extended_error_handling_suggestions.get(code),debug = debug, collor = extended_error_code_color.get(code // 100)) ,code

@app.route('/license')
def license_page():
    return render_template("license.html")





extended_error_code_color = {
    4:"#ff9900ff",
    5:"#ff0000bb"
}


extended_error_handling = {
    400: 'BadRequest',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'NotFound',
    405: 'MethodNotAllowed',
    406: 'NotAcceptable',
    408: 'RequestTimeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'LengthRequired',
    412: 'PreconditionFailed',
    413: 'RequestEntityTooLarge',
    414: 'RequestURITooLarge',
    415: 'UnsupportedMediaType',
    416: 'RequestedRangeNotSatisfiable',
    417: 'ExpectationFailed',
    418: 'ImATeapot',
    422: 'UnprocessableEntity',
    423: 'Locked',
    424: 'FailedDependency',
    428: 'PreconditionRequired',
    429: 'TooManyRequests',
    431: 'RequestHeaderFieldsTooLarge',
    451: 'UnavailableForLegalReasons',
    500: 'InternalServerError',
    501: 'NotImplemented',
    502: 'BadGateway',
    503: 'ServiceUnavailable',
    504: 'GatewayTimeout',
    505: 'HTTPVersionNotSupported'

}


extended_error_handling_suggestions = {
    400: {
        1: "Check the request syntax",
        2: "Verify the request parameters",
        3: "Ensure the URL is correct",
    },
    401: {
        1: "Check the authentication credentials",
        2: "Login again",
        3: "Contact the website administrator",
    },
    403: {
        1: "Check the URL for errors",
        2: "Request access from the administrator",
        3: "Ensure you have the necessary permissions",
    },
    404: {
        1: "Check the URL",
        2: "Reload the page",
        3: "Clear the browser cache",
        4: "Try using another browser",
        5: "Contact customer support",
    },
    405: {
        1: "Check the request method (GET, POST, etc.)",
        2: "Refer to the website's API documentation",
        3: "Ensure the method is supported",
    },
    408: {
        1: "Check your internet connection",
        2: "Ensure the server is not overloaded",
        3: "Retry the request after a moment",
    },
    500: {
        1: "Wait a few moments and retry the request",
        2: "Check the website's social media for updates",
        3: "Contact customer support",
    },
    501: {
        1: "Verify the request method is correct",
        2: "Check if the feature is implemented",
        3: "Contact the website administrator",
    },
    502: {
        1: "Check your internet connection",
        2: "Wait a few moments and retry the request",
        3: "Contact the website if the issue persists",
    },
    503: {
        1: "Check if the website is under maintenance",
        2: "Wait and retry later",
        3: "Contact the website for more information",
    },
    504: {
        1: "Check your internet connection",
        2: "Ensure the server is reachable",
        3: "Retry the request after a moment",
    },
}

def background_task():
    while True:
        time.sleep(10)  # 10秒ごとに実行
        sin.tick_task()

def start_background_thread():
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()





if __name__ == "__main__":
    start_background_thread()
    socketio.run(app,host='0.0.0.0',
            port=83,
            debug=False, 
            use_reloader=False 
            )

