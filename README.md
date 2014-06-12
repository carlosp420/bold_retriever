# Run this way

1. clone repository

```bash
    cd $USERAPPL
    git clone https://github.com/carlosp420/bold_retriever.git
```

2. install dependencies

```bash
    cd bold_retriever
    module load biopython-env
    pip install -r requirements.txt
```

3. run software

```bash
    python bold_retriever.py -f ZA2013-0565.fasta
```

4. output

```
bold_id,seq_id,similarity,taxon,class,order,family
FIDIP558-11,TE-14-27_FHYP_av,0.9884,Ornithomyia avicularia,Insecta,Diptera,Hippoboscidae,
DIPFI041-12,TE-14-27_FHYP_av,0.9254,Ornithomya,Insecta,Diptera,Hippoboscidae,
GBDP6413-09,TE-14-27_FHYP_av,0.9242,Ornithomya anchineura,Insecta,Diptera,Hippoboscidae,
GBDP2916-07,TE-14-27_FHYP_av,0.922,Stenepteryx hirundinis,Insecta,Diptera,Hippoboscidae,
GBDP2919-07,TE-14-27_FHYP_av,0.9149,Ornithomya biloba,Insecta,Diptera,Hippoboscidae,
GBDP2908-07,TE-14-27_FHYP_av,0.9078,Ornithoctona sp. P-20,Insecta,Diptera,Hippoboscidae,
GBDP2918-07,TE-14-27_FHYP_av,0.9076,Ornithomya chloropus,Insecta,Diptera,Hippoboscidae,
GBDP2935-07,TE-14-27_FHYP_av,0.8936,Crataerina pallida,Insecta,Diptera,Hippoboscidae,
GBMIN26225-13,TE-14-27_FHYP_av,0.8889,Lucilia sericata,Insecta,Diptera,Calliphoridae,
FIDIP602-12,TE-14-27_FHYP_av,0.8856,Azelia cilipes,Insecta,Diptera,Muscidae,
GBDP5820-09,TE-14-27_FHYP_av,0.8833,Coenosia tigrina,Insecta,Diptera,Muscidae,
GBMIN26204-13,TE-14-27_FHYP_av,0.883,Lucilia cuprina,Insecta,Diptera,Calliphoridae,
TTMDI037-08,TE-14-27_FHYP_av,0.8823,Muscidae,Insecta,Diptera,Muscidae,
GBMIN18768-13,TE-14-27_FHYP_av,0.8823,Ornithoctona erythrocephala,Insecta,Diptera,Hippoboscidae,
```
