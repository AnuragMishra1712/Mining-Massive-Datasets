import json
import os
import sys

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

data_dir = "../../data/"
PORT = 9200
INDEXNAME = "data"

DIRS = [data_dir]
host = "localhost:%s" % PORT
global esW
es = Elasticsearch([host])
print(es.info())


def process_dir(dir, index_name, verbose=False):
    files = os.listdir(dir)
    for file in files:
        file = os.path.join(dir, file)
        with open(file) as f:
            try:
                data = json.load(f)
                body = {'url': data["url"], 'content': data["text"]}
                item = {"_index": index_name, "doc": body}
                yield item
            except:
                if verbose:
                    print("Error in: ", file)
                continue


def create_index(index_name="data"):
    item = {"mappings": {
        "properties": {
            "url": {"type": "text", "index": False},
            "content": {"type": "text"},
        }
    }
    }
    try:
        response = es.indices.create(index=index_name, body=item)
        print(response)
        if response["acknowledged"]:
            print("Index %s created successfully" % index_name)
            return False
        else:
            print("Error in creating Index %s" % index_name)
            return True
    except Exception as e:
        print("Error: ", e)
        return True


def main():
    err = create_index(INDEXNAME)
    if err:
        sys.exit("Check index creation errors")
    for dir in DIRS:
        print("Indexing: ", dir)
        bulk(es, process_dir(dir, INDEXNAME))
    print("Initialization completed")


if __name__ == "__main__":
    main()