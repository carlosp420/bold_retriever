# genomseq

# Our potential dataset

* Full transcriptome from high quality specimen. mRNA -> cDNA to be used to pull down the genes from other
  specimens. Expected to pull down most exons from 1000's of genes for species withing 20--30 Mya window of
  the species used as bait. If works, can work with museum specimens.
* Expect 6,000 Lepidoptera single copy genes.
* Identify orthologs in Bombyx mori and H. melpomene and genomic locations of those genes in 
  those species.
* Generate a phylogenomic tree for each gene in various combinations (concatenated, individual, TIGER, etc)
* Combine data for genes that are close to each other on the chromosomes and run analyses for the question
  of gene trees versus species trees.

# Schetch of application

* Database in a Couchdb (NOSQL).
* Backend in PHP or Ruby.
* Accessed via a web browser, away from Domeneshop, probably in own office computer.
* User can select geneset to run, taxonsets and gene partitioning.
* User's input will be used as parameters for python scripts for creating datasets and analysis.
* TIGER is written in Python and can be optimzed for speed as it is not using any optimized library
  for speed.
* Dataset partitioning should be done with Python.
* Output a series of dataset files to run in RAXML or EXAML software.

# Similar software

1. Taming of impossible child [@peters2011] uses a pipeline of a series of scripts in ruby and perl 
   to harvest sequences from GenBank for Hymenoptear, process the sequences and create datasets for
   phylogenetic analysis (120,000 sequences). Dataset of 80,000 sites and 1,100 species.
2. *mor* [@hibbett2005] retrieves, screens, aligns, and analyzes nuc-lsu rDNA sequences of homobasidiomycetes
   from GenBank, and then parses out the contents of individual clades using node-based
   phylogenetic taxon definitions and creates NJ, MP and ML trees.
3. CouchDB is being used to develop database applications to deal with genomic data [@manyam2012].
4. STBase: *One billion species trees database* uses C++ scripts to generate tree files from Genbank
   sequences [not published yet; Mike Sanderson's group].

# References
