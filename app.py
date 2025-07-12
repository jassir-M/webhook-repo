from flask import Flask, request, jsonify, render_template
from models import save_event, get_latest_events

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Your frontend HTML

@app.route('/github', methods=['POST'])
def webhook():
    payload = request.json

    if not payload:
        return "Invalid payload", 400

    if 'head_commit' in payload:  # PUSH event
        author = payload['head_commit']['author']['name']
        to_branch = payload['ref'].split('/')[-1]
        timestamp = payload['head_commit']['timestamp']
        print(f'{author} pushed to {to_branch} on {timestamp}')
        save_event('push', author, None, to_branch, timestamp)

    elif 'pull_request' in payload:
        pr = payload['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        timestamp = pr['created_at']

        if payload.get('action') == 'opened':
            save_event('pull_request', author, from_branch, to_branch, timestamp)
            print(f'{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}')

        elif payload.get('action') == 'closed' and pr.get('merged'):
            save_event('merge', author, from_branch, to_branch, timestamp)
              # Print merged message here:
            print(f'{author} merged branch "{from_branch}" to "{to_branch}" on {timestamp}')

    return '', 204

@app.route('/events', methods=['GET'])
def events():
    events = get_latest_events()
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
