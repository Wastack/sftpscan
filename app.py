import logging
import os

from flask import Flask, render_template
from config import FILE_PATH, HOST, USER_NAME
from film_data import parse_tree

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

supported_formats = ['.mkv', '.avi', '.mp4']



@app.route('/')
def list_files():
    path = FILE_PATH
    if not os.path.isabs(path):
        logging.error("Path should be absolute")
        return 'Path provided is not a valid absolute path to a directory'

    db = parse_tree(path)
    logging.debug(f"bundles: {len(db.filmBundles)}")
    result = []
    for bundle in db.filmBundles:
        bundle.debug_print()
        for movie in bundle.files:
            sftp_link = f'sftp://{USER_NAME}@{HOST}:{movie.file_path}'
            result.append((movie.file_name, sftp_link))
    return render_template('base.html', result=result)


if __name__ == '__main__':
    app.run(host=HOST, port=5000)
