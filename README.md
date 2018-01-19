# Moteur de recherche

[![Build Status](https://travis-ci.org/souhaibattaiki/searchy.svg?branch=master)](https://travis-ci.org/souhaibattaiki/searchy)

Implémentation d'un moteur de recherche.

## Usage

Utilisez le script `searchy.py` pour indexer une collection:
```
usage: searchy.py [-h] [-q QUERY] [-m {bool,vect}]
                  [-n {cos,dice,jaccard,overlap}] [-t THRESHOLD]
                  [-w {tfidf,nf}] [-s] [-f] [--no-cache]
                  collection

Builds a search engine on a collection of documents

positional arguments:
  collection            Path to collection file (CACM format), directory or
                        url to zip

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Execute a search query
  -m {bool,vect}, --model {bool,vect}
                        Search engine model
  -n {cos,dice,jaccard,overlap}, --norm {cos,dice,jaccard,overlap}
                        Vectorial search norm
  -t THRESHOLD, --threshold THRESHOLD
                        Vectorial search norm threshold
  -w {tfidf,nf}, --weighting {tfidf,nf}
                        Vectorial weighting method
  -s, --silent          Disable verbose mode
  -f, --force           Force re-indexing overwrite cache
  --no-cache            Disable disk cache
```

exemple d'usage:
```
$ ./searchy.py data/CACM/cacm.all
Loading data/CACM/cacm.all
Loaded data/CACM/cacm.all
  documents 	 3204
  terms 	 81977
Calculating tf-idf weights matrix
Calculating normalized frequency weights matrix
🔍  > programming language
 ------------
 916. FORTRAN
 ------------
.T
FORTRAN
 --------------------
 195. What is a Code?
 --------------------
.T
What is a Code?
 -------------------------
 29. Need for an Algorithm
 -------------------------
.T
Need for an Algorithm
 -------------------------
 866. Sorting on Computers
 -------------------------
.T
Sorting on Computers
 -----------------------------
 1107. Computers and Education
 -----------------------------
.T
Computers and Education
 ----------------------------------
 948. Note on the Use of Procedures
 ----------------------------------
.T
Note on the Use of Procedures
 ---------------
 604. Why COBOL?
 ---------------
.T
Why COBOL?
 ----------
 918. COBOL
 ----------
.T
COBOL
 --------------------------------------
 1106. Programming of Digital Computers
 --------------------------------------
.T
programming of Digital Computers
 --------
 262. MAP
 --------
.T
MAP

total results: 251    10.23 ms
```
