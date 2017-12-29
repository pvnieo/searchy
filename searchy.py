#! /usr/bin/env python3

# stdlib
import argparse
import time
import os.path
# project
from Document import Document
from Index import Index
from search.bool import BooleanSearchEngine, NotValidQueryExpression
import utils


def exec_search(index, engine, query):
    start_time = time.time()
    try:
        results = engine.search(query)
        end_time = time.time()
        for doc in results:
            header = str(doc) + ". " + index.get_doc_by_id(doc).title
            print(utils.COLOR.BOLD, '-'*len(header), utils.COLOR.ENDC)
            print(utils.COLOR.BOLD, header, utils.COLOR.ENDC)
            print(utils.COLOR.BOLD, '-'*len(header), utils.COLOR.ENDC)
            print(index.get_doc_by_id(doc).content)
        print()
        print("total results:", len(results), "%8.2f ms" % (end_time - start_time))
    except NotValidQueryExpression as error:
        print(error)

def main():
    parser = argparse.ArgumentParser(description="Builds a search engine on a collection of documents")
    parser.add_argument("collection", help="Path to collection file (CACM format), directory or url to zip", type=str)
    parser.add_argument("-q", "--query", help="Execute a search query", type=str)
    parser.add_argument("-m", "--model", help="Search engine model", type=str, default="bool", choices=["bool", "vect"])
    parser.add_argument("-i", "--interactive", help="Run in interactive mode", action="store_true")
    parser.add_argument("-s", "--silent", help="Disable verbose mode", action="store_true")
    parser.add_argument("-f", "--force", help="Force re-indexing overwrite cache", action="store_true")
    parser.add_argument("--no-cache", help="Disable disk cache", action="store_true")
    args = parser.parse_args()

    if utils.is_url(args.collection):
        args.collection = utils.download_collection(args.collection)

    if not os.path.exists(args.collection):
        return print(args.collection + " Not found")

    index = None
    if os.path.isdir(args.collection):
        index = Index.index_directory(args.collection, verbose=(not args.silent), use_cache=(not args.no_cache), overwrite_cache=args.force, hold_content=False)
    else:
        index = Index.index_cacm_file(args.collection, verbose=(not args.silent), use_cache=(not args.no_cache), overwrite_cache=args.force)

    engine =  None
    if args.model == "bool":
        engine = BooleanSearchEngine(index)
    else:
        return print("Not implemented")

    if args.interactive:
        try:
            while True:
                query = input(u'\U0001F50D  > ')
                exec_search(index, engine, query)
        except KeyboardInterrupt:
            return
    elif args.query:
        exec_search(index, engine, args.query)

if __name__ == "__main__":
    main()
