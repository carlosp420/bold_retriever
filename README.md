# Generate document by using Makefiles
* ``make pdf``
* ``make docx``

# Run this way

1. clone repository

    cd $USERAPPL
    git clone https://github.com/carlosp420/bold_retriever.git

2. install dependencies

    cd bold_retriever
    module load biopython-env
    pip install -r requeriments.txt

3. run software

    python bold_retriever.py ZA2013-0565.fasta
