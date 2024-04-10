import flask
from flask import Flask, jsonify, request, render_template
from es import ESKNN

app = Flask(__name__)

esknn = ESKNN()
result = esknn.create_index()
INDEX_FLAG = False
if result == 1 or result == 2:
    INDEX_FLAG = True
else:
    print('main.py -> Something went wrong with create index.')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/insert_document', methods=['POST'])
def insert_document():
    data = request.json
    try:
        result = esknn.insert_document(data)
        if 'result' in result and result['result'] == 'created':
            return jsonify({
                "status": 200,
                "message": "Document inserted successfully"
            })
        else:
            return jsonify({
                "status": 500,
                "message": "Failed to insert document"
            })
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": "An error occurred: " + str(e)
        })

@app.route('/api/search_document', methods=['POST'])
def search_document():
    data = request.json
    fields = ['play_name', 'author', 'characters']
    query = data['query']

    result = esknn.search_document(query, fields)

    documents = []

    hits = result['hits']['hits']

    for hit in hits:
        documents.append(hit['_source'])

    return jsonify({
        "status": 200,
        "documents": documents
    })

