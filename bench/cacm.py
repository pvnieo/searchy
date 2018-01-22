# stdlib
import os.path
# project
from Index import Index
from Document import Document
from search.vectorial import VectorialSearchEngine
from search.calc import WEIGHTINGS, NORMS


collection_path = os.path.join("data", "CACM", "cacm.all")
querls_path =  os.path.join("data", "CACM", "qrels.text")
queries_path =  os.path.join("data", "CACM", "query.text")

index = Index.index_cacm_file(collection_path)
queries = Document.parse_cacm(queries_path)

querls = {}
with open(querls_path, 'r') as querls_file:
    for line in querls_file:
        query_id, res, _, _ = list(map(int, line.split()))
        if query_id not in querls:
            querls[query_id] = set()
        querls[query_id].add(res)

results = {weighting: {norm: 0 for norm in NORMS} for weighting in WEIGHTINGS}
for weighting in WEIGHTINGS:
    for norm in NORMS:
        engine = VectorialSearchEngine(index, weighting=weighting, norm=norm, threshold=0.1)
        success = 0
        total = 0
        for query in queries:
            if query.get_id() not in querls:
                continue
            querl = querls[query.get_id()]
            query_str = query.content.replace('.W\n', '')
            query_str = query_str.replace('.K\n', '')
            res, _ = engine.search(query_str, top=len(querl))
            success += sum([1 if doc_id in querl else 0 for _, doc_id in res]) / len(querl)
            total += 1
        print(weighting, norm, ": {:.2f}%".format(success * 100 / total))
        results[weighting][norm] = success * 100 / total
