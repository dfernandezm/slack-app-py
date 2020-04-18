'''
This is an example of the server-side logic to handle slash commands in
Python with Flask.
Detailed documentation of Slack slash commands:
https://api.slack.com/slash-commands
Slash commands style guide:
https://medium.com/slack-developer-blog/slash-commands-style-guide-4e91272aa43a#.6zmti394c
'''

# import your app object
import time
import datetime
from flask import Flask, g, request, render_template, session, flash, redirect, \
    url_for, jsonify
import sys
import logging
from rfc3339 import rfc3339

app = Flask(__name__)

# app.logger.disabled = True
# log = logging.getLogger('werkzeug')
# log.disabled = True

#https://flask.palletsprojects.com/en/1.0.x/logging/

# The parameters included in a slash command request (with example values):
#   token=gIkuvaNzQIHg97ATvDxqgjtO
#   team_id=T0001
#   team_domain=example
#   channel_id=C2147483705
#   channel_name=test
#   user_id=U2147483697
#   user_name=Steve
#   command=/weather
#   text=94070
#   response_url=https://hooks.slack.com/commands/1234/5678

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue'),
        ('response', response.data, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

# https://dev.to/rhymes/logging-flask-requests-with-colors-and-structure--7g1
    parts = []
    for name, value, color in log_params:
        part = "{}={}".format(name, value)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "alive"})


@app.route('/slash', methods=['POST'])
def slash_command():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
  
    app.logger.info(f"Token {token}")
    app.logger.info(f"Command {command}")
    app.logger.info(f"text {text}")

    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)
    # Use one of the following return statements
    # 1. Return plain text
    # return 'Simple plain response to the slash command received'
    # 2. Return a JSON payload
    # See https://api.slack.com/docs/formatting and
    # https://api.slack.com/docs/attachments to send richly formatted messages
    return jsonify({
        # Uncomment the line below for the response to be visible to everyone
        # 'response_type': 'in_channel',
        'text': 'More fleshed out response to the slash command',
        'attachments': [
            {
                'fallback': 'Required plain-text summary of the attachment.',
                'color': '#36a64f',
                'pretext': 'Optional text above the attachment block',
                'author_name': 'Bobby Tables',
                'author_link': 'http://flickr.com/bobby/',
                'author_icon': 'http://flickr.com/icons/bobby.jpg',
                'title': 'Slack API Documentation',
                'title_link': 'https://api.slack.com/',
                'text': 'Optional text that appears within the attachment',
                'fields': [
                    {
                        'title': 'Priority',
                        'value': 'High',
                        'short': False
                    }
                ],
                'image_url': 'http://my-website.com/path/to/image.jpg',
                'thumb_url': 'http://example.com/path/to/thumb.png'
            }
        ]
    })
    # 3. Send up to 5 responses within 30 minutes to the response_url
    # Implement your custom logic here

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5004, debug=True)