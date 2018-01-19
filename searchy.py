#! /usr/bin/env python3

# stdlib
import argparse
import time
import os.path
# project
from Document import Document
from Index import Index
from search.bool import BooleanSearchEngine, NotValidQueryExpression
from search.vectorial import VectorialSearchEngine
import utils


def exec_search(index, engine, query, **kargs):
    start_time = time.time()
    try:
        results, total = engine.search(query, **kargs)
        end_time = time.time()
        for score, doc_id in results:
            header = str(doc_id+1) + ". " + index.get_doc_by_id(doc_id).title + "  (" + str(abs(score)) + ")"
            print(utils.COLOR.BOLD, '-'*len(header), utils.COLOR.ENDC)
            print(utils.COLOR.BOLD, header, utils.COLOR.ENDC)
            print(utils.COLOR.BOLD, '-'*len(header), utils.COLOR.ENDC)
            print(index.get_doc_by_id(doc_id).highlighted_content(query))
        print()
        print("total results:", total, "%8.2f s" % (end_time - start_time))
    except NotValidQueryExpression as error:
        print(error)

def main():
    parser = argparse.ArgumentParser(description="Builds a search engine on a collection of documents")
    parser.add_argument("collection", help="Path to collection file (CACM format), directory or url to zip", type=str)
    parser.add_argument("-q", "--query", help="Execute a search query", type=str)
    parser.add_argument("-m", "--model", help="Search engine model", type=str, default="vect", choices=["bool", "vect"])
    parser.add_argument("-n", "--norm", help="Vectorial search norm", type=str, default="dice", choices=list(VectorialSearchEngine.NORMS.keys()))
    parser.add_argument("-t", "--threshold", help="Vectorial search norm threshold", type=float, default=0.1)
    parser.add_argument("-w", "--weighting", help="Vectorial weighting method", type=str, default="tfidf", choices=list(VectorialSearchEngine.WEIGHTINGS.keys()))
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
        engine = VectorialSearchEngine(index, weighting=args.weighting, norm=args.norm, threshold=args.threshold)
    
    if args.query:
        exec_search(index, engine, args.query)
    else:
        try:
            while True:
                query = input(u'\U0001F50D  > ')
                exec_search(index, engine, query)
        except KeyboardInterrupt:
            return

if __name__ == "__main__":
    main()
