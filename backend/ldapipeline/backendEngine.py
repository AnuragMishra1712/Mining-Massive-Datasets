#!/usr/bin/env python
# coding: utf-8

from backend.ldapipeline import ldapipelinehandler
from elasticsearch import Elasticsearch
from backend.kafka.kafkaconnector import KafkaConnection
import requests


def get_status():
    return requests.get('http://127.0.0.1:5000/status').json()


def run_kafka():
    conn = KafkaConnection()
    # download es and keep it running on the local sys while executing this
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # set up of index for es
    id = 0
    index = 'articles'
    doc_type = 'article'

    status_conn = KafkaConnection(topic='status')

    for data in conn.get_data():
        status = get_status()
        detail = ldapipelinehandler.write_to_json(data)
        id += 1

        # handling url is empty or vocab is empty(in this case do not dump into es)
        if (not detail['url']) or (not detail['vocab']):
            if 'count' in status:
                status['count'] -= 1
                if status['count'] == 0:
                    status = {'status': 'READY'}
                status_conn.send_data(status)
            continue

        # insert json into elasticsearch
        store = es.index(index=index, doc_type=doc_type, id=id, body=detail)
        print(store)

        if 'count' in status:
            status['count'] -= 1
            if status['count'] == 0:
                status = {'status': 'READY'}
            status_conn.send_data(status)

        # just to retrieve data from es
        retrieve = es.get(index=index, doc_type=doc_type, id=id)
        print(retrieve['_source'])

        # deleting the document(this statement can be deleted later)
        #  = es.delete(index=index, doc_type=doc_type, id=id)
        # print(erase['result'])


if __name__ == "__main__":
    run_kafka()
