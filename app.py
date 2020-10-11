import logging
import os

from flask import Flask, render_template
from config import FILE_PATH, HOST, USER_NAME

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

supported_formats = ['.mkv', '.avi', '.mp4']


def is_supported(file_name: str) -> bool:
    for sup in supported_formats:
        if file_name.endswith(sup):
            return True
    return False


@app.route('/')
def list_files():
    path = FILE_PATH
    if not os.path.isabs(path):
        logging.error("Path should be absolute")
        return 'Path provided is not a valid absolute path to a directory'

    files_all = []
    for root, _, files in os.walk(FILE_PATH):
        for f in files:
            if not is_supported(f):
                continue
            sftp_link = f'sftp://{USER_NAME}@{HOST}:"{os.path.join(root, f)}"'
            files_all.append((f, sftp_link))
    return render_template('base.html', result=files_all)


if __name__ == '__main__':
    app.run(host=HOST, port=5000)
