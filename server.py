import os
from flask import Flask, request, jsonify

from modules.facebook import Facebook
from modules.threads import Threads
from modules.instagram import Instagram
from modules.tiktok import TikTok
from modules.youtube import YouTube

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "service": "Social Job Checker Microservice",
        "version": "1.0.0"
    })

# 1. Endpoint Facebook
@app.route('/check-facebook', methods=['POST'])
def handle_check_facebook():
    req = request.get_json(force=True)
    cookies = req.get('cookies', '')
    target_id = str(req.get('target_id', ''))
    user_list = req.get('user_list', [])
    action_type = str(req.get('action_type', 'follow')).lower()

    fb = Facebook(cookies)
    if action_type == 'like':
        res_json = fb.like(target_id)
    elif action_type == 'comment':
        res_json = fb.comment(target_id)
    else:
        res_json = fb.follow(target_id)

    result = fb.check_list(
        target_id=target_id,
        user_list=user_list,
        response_data=res_json,
        check_type=action_type
    )
    return jsonify(result)

# 2. Endpoint Threads
@app.route('/check-threads', methods=['POST'])
def handle_check_threads():
    req = request.get_json(force=True)
    cookies = req.get('cookies', '')
    target_id = str(req.get('target_id', ''))
    user_list = req.get('user_list', [])
    action_type = str(req.get('action_type', 'follow')).lower()

    th = Threads(cookies)
    if action_type == 'like':
        res_json = th.like(target_id)
    elif action_type == 'comment':
        res_json = th.comment(target_id)
    else:
        res_json = th.follow(target_id)

    result = th.check_list(
        target_id=target_id,
        user_list=user_list,
        response_data=res_json,
        check_type=action_type
    )
    return jsonify(result)

# 3. Endpoint Instagram
@app.route('/check-instagram', methods=['POST'])
def handle_check_instagram():
    req = request.get_json(force=True)
    cookies = req.get('cookies', '')
    target_id = str(req.get('target_id', ''))
    user_list = req.get('user_list', [])
    action_type = str(req.get('action_type', 'follow')).lower()

    ig = Instagram(cookies)
    if action_type == 'like':
        res_json = ig.like(target_id)
    elif action_type == 'comment':
        res_json = ig.comment(target_id)
    else:
        res_json = ig.follow(target_id)

    result = ig.check_list(
        target_id=target_id,
        user_list=user_list,
        response_data=res_json,
        check_type=action_type
    )
    return jsonify(result)

# 4. Endpoint TikTok
@app.route('/check-tiktok', methods=['POST'])
def handle_check_tiktok():
    req = request.get_json(force=True)
    cookies = req.get('cookies', '')
    target_id = str(req.get('target_id', ''))
    user_list = req.get('user_list', [])
    action_type = str(req.get('action_type', 'follow')).lower()

    tt = TikTok(cookies)
    if action_type == 'like':
        res_json = tt.like(target_id)
    elif action_type == 'comment':
        res_json = tt.comment(target_id)
    else:
        res_json = tt.follow(target_id)

    result = tt.check_list(
        target_id=target_id,
        user_list=user_list,
        response_data=res_json,
        check_type=action_type
    )
    return jsonify(result)

# 5. Endpoint YouTube
@app.route('/check-youtube', methods=['POST'])
def handle_check_youtube():
    req = request.get_json(force=True)
    target_id = str(req.get('target_id', ''))
    user_list = req.get('user_list', [])
    action_type = str(req.get('action_type', 'subscribe')).lower()
    custom_api_key = req.get('api_key', None)

    yt = YouTube(api_key=custom_api_key) if custom_api_key else YouTube()
    result = yt.check_list(
        target_channel_id=target_id,
        user_channel_list=user_list,
        check_type=action_type
    )
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
