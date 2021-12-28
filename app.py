import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests
from pager import Pager

MEDIA_FOLDER='//nas/Fotos/FotoScans/Scanned_Pictures/Hofbilder/'

def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]


APPNAME = "Photoalbum"
STATIC_FOLDER = 'example'
TABLE_FILE = "example/fakecatalog2.csv"

table = read_table(TABLE_FILE)
pager = Pager(len(table))

print(table[1])

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<int:ind>/')
def image_view(ind=None):
    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        pager.current = ind
        xx=table[ind]
        print(xx['name'])
        print(url_for('download_file', filename=xx['name']))
        return render_template(
            'imageview.html',
            index=ind,
            pager=pager,
            data=table[ind])


@app.route('/uploads/<path:filename>')
def download_file(filename):
    print(filename)
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)

@app.route('/goto', methods=['POST', 'GET'])    
def goto():
    return redirect('/' + request.form['index'])


if __name__ == '__main__':
    app.run(debug=True)
