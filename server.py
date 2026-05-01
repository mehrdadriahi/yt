from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', methods=['POST'])
def process_download():
    data = request.json
    url = data.get('url')
    format_type = data.get('format')

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'quiet': True,
            'restrictfilenames': True # جلوگیری از ارور نام‌های عجیب
        }
        if format_type == 'mp3':
            ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio'
        else:
            ydl_opts['format'] = 'best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # پیدا کردن نام دقیق فایلی که دانلود شده
            filename = os.path.basename(ydl.prepare_filename(info))

        return jsonify({"success": True, "file_name": filename})

    except Exception as e:
        return jsonify({"error": "Download Failed."}), 500

@app.route('/fetch-file/<filename>', methods=['GET'])
def fetch_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)