# Run this way

* clone repository
```bash
    cd $USERAPPL
    git clone https://github.com/carlosp420/bold_retriever.git
```
* install dependencies
```bash
    cd bold_retriever
    module load biopython-env
    pip install -r requirements.txt
```
* run software
```bash
    python bold_retriever.py -f ZA2013-0565.fasta
```
* output
```
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
```

## Changes

* v0.0.6: Catching exception for malformed XML from BOLD
* v0.0.5: Catch exception when BOLD sends funny data such as `` {"481541":[]}``.
