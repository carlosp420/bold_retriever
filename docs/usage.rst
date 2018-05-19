.. _usage-label:

=====
Usage
=====

How to run ``bold_retriever``
-----------------------------

You have to choose one of the databases available from BOLD
http://www.boldsystems.org/index.php/resources/api?type=idengine
and enter it as argument:

* COX1_SPECIES
* COX1
* COX1_SPECIES_PUBLIC
* COX1_L640bp

For example::

    python bold_retriever.py -f ZA2013-0565.fasta -db COX1_SPECIES

The output should look like this::

    OtuID             bold_id        similarity  division  class    order    family         species                      collection_country
    TE-14-27_FHYP_av  FIDIP558-11    0.9884      animal    Insecta  Diptera  None           Diptera                      Finland           
    TE-14-27_FHYP_av  GBDP6413-09    0.9242      animal    Insecta  Diptera  Hippoboscidae  Ornithomya anchineura        None              
    TE-14-27_FHYP_av  GBDP2916-07    0.922       animal    Insecta  Diptera  Hippoboscidae  Stenepteryx hirundinis       None              
    TE-14-27_FHYP_av  GBDP2919-07    0.9149      animal    Insecta  Diptera  Hippoboscidae  Ornithomya biloba            None              
    TE-14-27_FHYP_av  GBDP2908-07    0.9078      animal    Insecta  Diptera  Hippoboscidae  Ornithoctona sp. P-20        None              
    TE-14-27_FHYP_av  GBDP2918-07    0.9076      animal    Insecta  Diptera  Hippoboscidae  Ornithomya chloropus         None              
    TE-14-27_FHYP_av  GBDP2935-07    0.8936      animal    Insecta  Diptera  Hippoboscidae  Crataerina pallida           None              
    TE-14-27_FHYP_av  GBMIN26225-13  0.8889      animal    Insecta  Diptera  Calliphoridae  Lucilia sericata             None              
    TE-14-27_FHYP_av  GBDP5820-09    0.8833      animal    Insecta  Diptera  Muscidae       Coenosia tigrina             None              
    TE-14-27_FHYP_av  GBMIN26204-13  0.883       animal    Insecta  Diptera  Calliphoridae  Lucilia cuprina              None              
    TE-14-27_FHYP_av  GBMIN18768-13  0.8823      animal    Insecta  Diptera  Hippoboscidae  Ornithoctona erythrocephala  Brazil            

As an alternative you can use ``bold_retriever`` as a Python module
-------------------------------------------------------------------
To use Bold Retriever in a project::

    >>> from Bio import SeqIO
    >>> from bold_retriever import bold_retriever as br

    >>> # database from BOLD
    >>> db = "COX1_SPECIES"

    >>> all_ids = []
    >>> for seq_record in SeqIO.parse("tests/ionx13.fas", "fasta"):
    ...    my_ids = br.request_id(seq_record.seq, seq_record.id, db)
    Psocoptera 0.9796
    Selenops mexicanus 0.8933
    Austrophorocera Janzen03 0.8736
    Austrophorocera Janzen04 0.8667
    Lepidoptera 0.8667
    Proechimys simonsi 0.8667
    Diptera 0.8667
    Scathophaga stercoraria 0.8667
    Culex quinquefasciatus 0.8667
    Folsomia fimetaria L1 0.8652
    Lepidopsocidae sp. RS-2001 0.8639
    lepidopsocid RS-2001 0.8639
    Selenops micropalpus 0.859
    Geocoris pallidipennis 0.8586
    Selenops sp. 2 SCC-2009 0.8571
    Mermessus trilobatus 0.8571
    Drosophila neotestacea 0.8571
    Hemiptera 0.8556
    Miromantis mirandula 0.8537
    Houghia gracilis 0.8533
    Adoxophyes nr. marmarygodes 0.8533
    Trichoptera 0.8533
    Araneae 0.8533
    Hydroporus morio 0.8533
    Rodentia 0.8533

In that case the output will be contained in the variable ``my_ids`` and
will look like this::

    [{'bold_id': 'FIPSO166-14',
    'collection_country': 'Finland',
    'id': 'ionx13',
    'seq': 'AATTTGAGCTGGTATACTTGGGACTAGTTTAAGAATCTTAATTCGACTTGAGTTAGGCCAACCAGGTTTATTtttAGAAGATGACCAAACATATAATGTTATCGTTACCGCTCACGCTTTTATTATAATTttttttATAGTAATACCAATATA',
    'similarity': '0.9796',
    'tax_id': 'Psocoptera'},
    {'bold_id': 'GBCH4611-10',
    'collection_country': 'None',
    'id': 'ionx13',
    'seq': 'AATTTGAGCTGGTATACTTGGGACTAGTTTAAGAATCTTAATTCGACTTGAGTTAGGCCAACCAGGTTTATTtttAGAAGATGACCAAACATATAATGTTATCGTTACCGCTCACGCTTTTATTATAATTttttttATAGTAATACCAATATA',
    'similarity': '0.8933',
    'tax_id': 'Selenops mexicanus'},
    {'bold_id': 'ASTAQ477-06',
    'collection_country': 'Costa Rica',
    'id': 'ionx13',
    'seq': 'AATTTGAGCTGGTATACTTGGGACTAGTTTAAGAATCTTAATTCGACTTGAGTTAGGCCAACCAGGTTTATTtttAGAAGATGACCAAACATATAATGTTATCGTTACCGCTCACGCTTTTATTATAATTttttttATAGTAATACCAATATA',
    'similarity': '0.8736',
    'tax_id': 'Austrophorocera Janzen03'},
    {'bold_id': 'ASTAR353-07',
    'collection_country': 'Costa Rica',
    'id': 'ionx13',
    'seq': 'AATTTGAGCTGGTATACTTGGGACTAGTTTAAGAATCTTAATTCGACTTGAGTTAGGCCAACCAGGTTTATTtttAGAAGATGACCAAACATATAATGTTATCGTTACCGCTCACGCTTTTATTATAATTttttttATAGTAATACCAATATA',
    'similarity': '0.8667',
    'tax_id': 'Austrophorocera Janzen04'}]

