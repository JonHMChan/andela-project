from elasticsearch import Elasticsearch

es = Elasticsearch()
# es.index(index="my-index", doc_type="test-type", id=1, body={"name": "Jon", "language": "python"})
result = es.search(index="my-index", body={"query": {"fuzzy": {'language':'javascript'}}})
print result