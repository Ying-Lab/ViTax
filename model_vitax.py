import torch.nn as nn
from model_hyena import HyenaDNAModel
import json


class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()
        config = json.load(open("model/config.json"))
        self.model = HyenaDNAModel(**config, use_head=False)
        

        
        
    def forward(self, dna):

        dna_embed = self.get_dna(dna)
        return dna_embed

    def get_dna(self,dna_inputs):
        dna_embed = self.model(dna_inputs)[:,-1,:]

        return dna_embed

        
        
