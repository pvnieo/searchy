# Moteur de recherche

[![Build Status](https://travis-ci.org/souhaibattaiki/searchy.svg?branch=master)](https://travis-ci.org/souhaibattaiki/searchy)

Implémentation d'un moteur de recherche.

## Usage

Deux collections de documents sont disponibles pour utiliser l'outil.

### Collection CACM

Utilisez le script `cacm.py` pour indexer une collection CACM:
```
usage: cacm.py [-h] [-q QUERY] [-m {bool,vect}] [-i] [-s] [-f] collection

Loads CACM collection and indexes it.

positional arguments:
  collection            Path to CACM collection file

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Execute a search query
  -m {bool,vect}, --model {bool,vect}
                        Search engine model
  -i, --interactive     Run in interactive mode
  -s, --silent          Disable verbose mode
  -f, --force           Force re-indexing without cache
```

exemple d'usage:
```
$ ./cacm.py -i Data/CACM/cacm.all
Loaded Data/CACM/cacm.all
  documents 	 3204
  tokens 	 118919
🔍  > programming&address&(~computer|user)
--- 2253
.T
Index Ranges for Matrix Calculi
...
4.12 4.22 5.14
--- 1693
.T
GPL, a Truly General Purpose Language
...
4.20
--- 79
.T
programming for a Machine With an Extended
address Calculational Mechanism
--- 1463
.T
More on Extensible Machines
...

total results: 4     0.00 ms
```
