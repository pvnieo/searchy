# Moteur de recherche

[![Build Status](https://travis-ci.org/souhaibattaiki/searchy.svg?branch=master)](https://travis-ci.org/souhaibattaiki/searchy)

Implémentation d'un moteur de recherche pour une collection de fichiers.

## Usage

Utilisez le script `searchy.py` pour indexer une collection:
```
usage: searchy.py [-h] [-q QUERY] [-m {bool,vect}]
                  [-n {cos,dice,jaccard,overlap}] [-t THRESHOLD]
                  [-w {f,tfidf,nf}] [-s] [-f] [--no-cache]
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
  -w {f,tfidf,nf}, --weighting {f,tfidf,nf}
                        Vectorial weighting method
  -s, --silent          Disable verbose mode
  -f, --force           Force re-indexing overwrite cache
  --no-cache            Disable disk cache
```

## Exemple d'usage

### Model vectoriel

Les requêtes sont des phrases. Ici on chechre dans la collection CACM.

```
$ ./searchy.py data/CACM/cacm.all
Loading data/CACM/cacm.all
Using cache 64f76a63
  documents 	 3204
  tokens 	 113754
  terms 	 5961
memory: 0.42 mb
🔍  > Processes and Proofs of Theorems and Programs
 -----
 3079. An Algorithm for Reasoning About Equality [93.99%]
 -----
.T
An Algorithm for Reasoning About Equality
.W
A simple technique for reasoning about equalities
that is fast and complete for ground formulas
...
 -----
 3140. Social Processes and Proofs of Theorems and Programs [93.87%]
 -----
.T
Social Processes and Proofs of Theorems and Programs
.W
It is argued that formal verifications of
programs, no matter how obtained, will not play the
same key role in the development of computer science and software
engineering as proofs do in mathematics.  Furthermore the absence
...

total results: 260     2.94 s
```

Pour charger la collection Stanford on peut utiliser l'url directement comme argument
```
$ ./searchy.py http://web.stanford.edu/class/cs276/pa/pa1-data.zip
```

### Model booléen

Les requêtes doivent être au format booléen suivant: `(mot1 & mot2) | ~mot3` 
les opérateurs booléen autorisés sont: `&` (et), `|` (ou), `~` (négation).

```
./searchy.py -m bool data/CACM/cacm.all
Loading data/CACM/cacm.all
Using cache 64f76a63
  documents 	 3204
  tokens 	 113754
  terms 	 5961
memory: 0.42 mb
🔍  > processes & Proofs & theorems & programs
 -----
 3140. Social Processes and Proofs of Theorems and Programs [100.00%]
 -----
.T
Social Processes and Proofs of Theorems and Programs
.W
It is argued that formal verifications of
programs, no matter how obtained, will not play the
same key role in the development of computer science and software
engineering as proofs do in mathematics.  Furthermore the absence
of continuity, the inevitability of change, and the complexity of
specification of significantly many real programs make the form
al verification process difficult to justify and manage.  It is felt
that ease of formal verification should not dominate program
language design.
.K
Formal mathematics, mathematical proofs,
program verification, program specification
2.10 4.6 5.24

total results: 1     2.96 s
```
