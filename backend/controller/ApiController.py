from subprocess import Popen

# import res as res
from flask import Flask
from flask import request
from backend.kafka.kafkaconnector import KafkaConnection
from threading import Thread
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch


app = Flask(__name__, static_folder='~/AutomatedArticleTaggerApp/UI/app/build', static_url_path='/')

CORS(app)
#app.get('/cors', (req, res) => {res.set('Access-Control-Allow-Origin', 'http://localhost:3000'); res.send({ "msg": "This has CORS enabled 🎈" })})
STATUS = {'status': 'READY'}

status_conn = KafkaConnection(topic="status")

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


# thread process to update the status
def status_listener():
    global STATUS
    for data in status_conn.get_data():
        if data is not None:
            STATUS = data


status_thread = Thread(target=status_listener)


# Begin data extraction
@app.route("/extract")
@cross_origin()
def start_data_extraction():
    global STATUS
    query = request.args['q']
    Popen(['python', '-m', 'getData', query])
    STATUS['status'] = 'BEGINNING DATA EXTRACTION'
    return {"message": "started data extraction", "status": STATUS}, 200


# Data Fetch from elasticsearch
@app.route("/results")
@cross_origin()
def show_results():
    query = request.args['q']
    if 'limit' in request.args:
        limit = request.args['limit']
    else:
        limit = 10

    if 'offset' in request.args:
        offset = request.args['offset']
    else:
        offset = 0
    # Get data from elasticsearch and show to the user
    response = es.search(index='articles', q=query, from_=offset, size=limit)
    data = response['hits']['hits']
    data = [x['_source'] for x in data]
    return {'results': data}, 200


@app.route("/status")
@cross_origin()
def get_status():
    global STATUS
    return STATUS, 200


if __name__ == '__main__':
    status_thread.start()
    app.run()
