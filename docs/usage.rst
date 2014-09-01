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

    from Bio import SeqIO
    from bold_retriever import bold_retriever as br

    # database from BOLD
    db = "COX1_SPECIES"

    all_ids = []
    for seq_record in SeqIO.parse("my_fasta_file.fas", "fasta"):
        this_ids = br.request_id(seq_record.seq, seq_record.id, db)
        all_ids.append(this_ids)
    print(all_ids)

In that case the output will be contained in the variable ``all_ids`` and
will look like this::

    [[{'bold_id': 'SAMOS029-09',
        'collection_country': 'Canada',
        'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2',
        'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
        'similarity': '1',
        'tax_id': 'Diptera'},
    {'bold_id': 'JWDCC841-10',
        'collection_country': 'Canada',
        'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2',
        'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
        'similarity': '1',
        'tax_id': 'Culicidae'},
    {'bold_id': 'BBDCN544-10',
        'collection_country': 'Canada',
        'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2',
        'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
        'similarity': '1',
        'tax_id': 'Ochlerotatus impiger'},
    {'bold_id': 'SSEIC5967-13',
        'collection_country': 'Canada',
        'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2',
        'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
        'similarity': '1',
        'tax_id': 'Ochlerotatus nigripes'}]]
