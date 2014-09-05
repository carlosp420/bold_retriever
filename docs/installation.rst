============
Installation
============
You can download the lastest version of the software here:
https://github.com/carlosp420/bold_retriever/releases

Or, at the command line::

    $ # Clone repository
    $ git clone https://github.com/carlosp420/bold_retriever.git
    $ cd bold_retriever
    $ # install dependencies
    $ pip install -r requirements.txt

Run the software by specifying a FASTA file as input and a BOLD database for
queries::

    $ python bold_retriever.py -f ZA2013-0565.fasta -db COX1_SPECIES

As an alternative, if you have virtualenvwrapper installed::

    $ # install software
    $ mkvirtualenv bold_retriever
    $ pip install bold_retriever
    $ # install dependencies
    $ pip install -r requirements.txt
