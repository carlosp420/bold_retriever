.. :changelog:

History
-------
* v0.2.X: Reorganizing columns in output file. Querying the API for family
          name of taxa.
* v0.2.2: Killed bug taxon search.
* v0.2.1: Killed bug in scraping web ``Public_BIN`` for species ID.
* v0.2.0: Scraping web ``Public_BIN`` for species ID.
* v0.1.9: Added request_id test and option to run fuction in debug mode.
* v0.1.8: Fixed bug for exception when BOLD sends empty list of taxon names.
* v0.1.7: Fixed bug for exception when BOLD sends empty list of taxon names.
* v0.1.6: Append taxon identification results to file as we get them.
* v0.1.5: Additionat tests coverage 92%
* v0.1.4: Fixed bug in taxon_search function
* v0.1.3: Coverage 75%
* v0.1.2: Pep8 and test coverage 69%
* v0.1.1: Packaged as Python module.
* v0.1.0: You can specify which BOLD datase should be used for BLAST of FASTA sequences.
* v0.0.7: Catching exception for NULL, list and text returned instead  of XML from BOLD.
* v0.0.6: Catching exception for malformed XML from BOLD.
* v0.0.5: Catch exception when BOLD sends funny data such as ``{"481541":[]}``.
