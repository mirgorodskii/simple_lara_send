import os
from flask import Flask, request, jsonify
from datetime import datetime
import resend

app = Flask(__name__)

resend.api_key = os.environ["RESEND_API_KEY"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]


def cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return resp


@app.route('/send', methods=['POST'])
def send_manual():
    text = request.json.get('text', '').strip()
    if not text:
        return cors(jsonify({"error": "empty"})), 400

    now = datetime.now()

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "subject": f"✨ {now.strftime('%B %d')}",
        "html": f"""
        <div style="font-family: Georgia, serif; max-width: 480px; margin: 0 auto; padding: 40px 20px; color: #222;">
            <p style="font-size: 18px; line-height: 1.8; margin-bottom: 32px; white-space: pre-line;">{text}</p>
            <p style="font-size: 13px; color: #bbb; margin-top: 32px;">— V</p>
        </div>
        """
    })


    return cors(jsonify({"ok": True}))


@app.route('/send', methods=['OPTIONS'])
def send_options():
    return cors(jsonify({}))


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"ok": True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
