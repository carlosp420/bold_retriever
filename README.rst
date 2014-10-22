==============
Bold Retriever
==============

|Pypi index| |Build Status| |Cover alls| |Dependencies status| |Download numbers|


This script accepts FASTA files containing COI sequences. It queries the BOLD
database http://boldsystems.org/ in order to get the taxa identification
based on the sequences.
 
Run this way
------------
* clone repository::

    cd $USERAPPL
    git clone https://github.com/carlosp420/bold_retriever.git

* install dependencies (python2.7)::

    cd bold_retriever
    module load biopython-env
    pip install -r requirements.txt

* run software

You have to choose one of the databases available from BOLD
http://www.boldsystems.org/index.php/resources/api?type=idengine
and enter it as argument:

* COX1_SPECIES
* COX1
* COX1_SPECIES_PUBLIC
* COX1_L640bp

For example::

    python bold_retriever.py -f ZA2013-0565.fasta -db COX1_SPECIES

* output::

    bold_id        seq_id            similarity  collection_country  division  taxon                        class    order    family
    FIDIP558-11    TE-14-27_FHYP_av  0.9884      Finland             animal    Diptera                      Insecta  Diptera  None
    GBDP6413-09    TE-14-27_FHYP_av  0.9242      None                animal    Ornithomya anchineura        Insecta  Diptera  Hippoboscidae
    GBDP2916-07    TE-14-27_FHYP_av  0.922       None                animal    Stenepteryx hirundinis       Insecta  Diptera  Hippoboscidae
    GBDP2919-07    TE-14-27_FHYP_av  0.9149      None                animal    Ornithomya biloba            Insecta  Diptera  Hippoboscidae
    GBDP2908-07    TE-14-27_FHYP_av  0.9078      None                animal    Ornithoctona sp. P-20        Insecta  Diptera  Hippoboscidae
    GBDP2918-07    TE-14-27_FHYP_av  0.9076      None                animal    Ornithomya chloropus         Insecta  Diptera  Hippoboscidae
    GBDP2935-07    TE-14-27_FHYP_av  0.8936      None                animal    Crataerina pallida           Insecta  Diptera  Hippoboscidae
    GBMIN26225-13  TE-14-27_FHYP_av  0.8889      None                animal    Lucilia sericata             Insecta  Diptera  Calliphoridae
    GBDP5820-09    TE-14-27_FHYP_av  0.8833      None                animal    Coenosia tigrina             Insecta  Diptera  Muscidae
    GBMIN26204-13  TE-14-27_FHYP_av  0.883       None                animal    Lucilia cuprina              Insecta  Diptera  Calliphoridae
    GBMIN18768-13  TE-14-27_FHYP_av  0.8823      Brazil              animal    Ornithoctona erythrocephala  Insecta  Diptera  Hippoboscidae

Full documentation
------------------
See the full documentation at http://bold-retriever.readthedocs.org

.. |Pypi index| image:: https://badge.fury.io/py/bold_retriever.svg
   :target: http://badge.fury.io/py/bold_retriever
.. |Build Status| image:: https://travis-ci.org/carlosp420/bold_retriever.png?branch=master
   :target: https://travis-ci.org/carlosp420/bold_retriever
.. |Cover alls| image:: https://img.shields.io/coveralls/carlosp420/bold_retriever.svg
   :target: https://coveralls.io/r/carlosp420/bold_retriever?branch=master
.. |Dependencies status| image:: https://gemnasium.com/carlosp420/bold_retriever.svg
   :target: https://gemnasium.com/carlosp420/bold_retriever
.. |Download numbers| image:: https://pypip.in/download/bold_retriever/badge.svg
   :target: https://crate.io/packages/bold_retriever
   :alt: Downloads
