#! /usr/bin/env python3

# stdlib
import argparse
import time
# project
from Document import Document
from Index import Index
from search.bool import BooleanSearchEngine, NotValidQueryExpression


def exec_search(index, engine, query):
    start_time = time.time()
    try:
        results = engine.search(query)
        end_time = time.time()
        for doc in results:
            print("---", doc)
            print('\n'.join(index.get_doc_by_id(doc).content))
        print()
        print("total results:", len(results), "%8.2f ms" % (end_time - start_time))
    except NotValidQueryExpression as error:
        print(error)

def main():
    parser = argparse.ArgumentParser(description="Loads CACM collection and indexes it.")
    parser.add_argument("collection", help="Path to CACM collection file", type=str)
    parser.add_argument("-q", "--query", help="Execute a search query", type=str)
    parser.add_argument("-m", "--model", help="Search engine model", type=str, default="bool", choices=["bool", "vect"])
    parser.add_argument("-i", "--interactive", help="Run in interactive mode", action="store_true")
    parser.add_argument("-s", "--silent", help="Disable verbose mode", action="store_true")
    parser.add_argument("-f", "--force", help="Force re-indexing without cache", action="store_true")
    args = parser.parse_args()

    index = Index.index_cacm_file(args.collection, verbose=(not args.silent), use_cache=(not args.force))
    engine =  None
    if args.model == "bool":
        engine = BooleanSearchEngine(index)
    else:
        print("Not implemented")
        return

    if args.interactive:
        while True:
            query = input(u'\U0001F50D  > ')
            exec_search(index, engine, query)
    elif args.query:
        exec_search(index, engine, args.query)

if __name__ == "__main__":
    main()
