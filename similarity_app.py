"""Simple flask app to calculate document similarity."""

from flask import Flask, render_template, request

from similarity import similarity

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template(
            'index.html',
            doc1=None,
            doc2=None,
            similarity=None,
        )
    elif request.method == 'POST':
        doc1 = request.form['doc1']
        doc2 = request.form['doc2']
        sim = similarity(doc1, doc2)
        return render_template(
            'index.html',
            doc1=doc1,
            doc2=doc2,
            similarity=sim
        )
