from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from tempfile import TemporaryDirectory

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format')

    if not url or not format_type:
        return "URLと形式を指定してください", 400

    try:
        yt = YouTube(url)
        yt.check_availability()
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 400

    try:
        with TemporaryDirectory() as temp_dir:
            if format_type == 'audio':
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.get_highest_resolution()

            if not stream:
                return "対応するストリームが見つかりません", 400

            file_path = stream.download(output_path=temp_dir)
            return send_file(
                file_path,
                as_attachment=True,
                download_name=f"{yt.title}.{stream.subtype}"
            )
    except Exception as e:
        return f"ダウンロード処理中にエラーが発生しました: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)