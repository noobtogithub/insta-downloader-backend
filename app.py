from flask import Flask, request, jsonify, send_file
import yt_dlp
import os, uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url or 'instagram.com' not in url:
        return jsonify(error='Invalid URL'), 400

    filename = f"{uuid.uuid4()}.mp4"
     opts = {
        'format': 'best',
        'outtmpl': filename,
        'cookiefile': 'instagram_cookies.txt'  # ← this is the key
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
