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

