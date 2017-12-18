#! /usr/bin/env python3

# stdlib
import argparse
# project
from Document import Document
from Index import Index


def main():
    parser = argparse.ArgumentParser(description="Loads CACM collection and indexes it.")
    parser.add_argument("collection", help="Path to CACM collection file", type=str)
    parser.add_argument("-i", "--interactive", help="Run in interactive mode", action="store_true")
    args = parser.parse_args()

    documents = Document.parse_cacm(args.collection, verbose=True)
    index = Index.index_all(documents)
    # index.print()


if __name__ == "__main__":
    main()
