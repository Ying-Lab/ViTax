# ViTax
## Overview
ViTax is a virus taxonomy classification tool powered by the HyenaDNA foundation model, a large language model for long-range genomic sequences at single nucleotide resolution. Aiming to the specific challenges of virus taxonomy classification, ViTax integrates supervised prototypical contrastive learning to address the challenge of highly imbalanced distributions across various taxonomic clades and employs a belief mapping tree on the Least Common Ancestor algorithm to achieve the taxonomy level with the most confidence adaptively. ViTax support the classification of up to 631 genera.
## Installation
ViTax is a Python package. To install it, run the following command in your terminal:
```
git clone https://github.com/Ying-Lab/ViTax.git
pip install -r requirements.txt
``` 

## Run ViTax model
``` 
python ViTax.py [--contigs INPUT_FA] [--out OUTPUT_TXT] 
--contigs INPUT_FA   input fasta file
--out OUTPUT_TXT     The output csv file (prediction_output.txt default) 
--confidence         The confidence threshold of the prediction (0.6 default)  
```
## Example
```
python ViTax.py --contigs test.fa --out prediction_output.txt --confidence 0.6
```