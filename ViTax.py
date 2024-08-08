import argparse
import torch
from model_vitax import Encoder
from tokenizer_hyena import CharacterTokenizer
from Bio import SeqIO
from lca.tree import *
from utils import *
from tqdm import tqdm
parser = argparse.ArgumentParser(description="""ViTax is a python library for DSDNA virus genus-level classification.""")



parser.add_argument('--contigs', help='FASTA file of contigs',  default = 'test_contigs.fasta')
parser.add_argument('--model', help='Model weight',  default = 'model/model_weight.pth')
parser.add_argument('--kmean', help='kmeans result',  default = 'model/kmeans.pickle')
parser.add_argument('--tree', help='taxonomy belief tree',  default = 'model/tbt.pickle')
parser.add_argument('--out', help='name of the output file',  type=str, default = 'prediction_output.txt')
parser.add_argument('--index', help='tree index',  type=str, default = 'model/index.pickle')

inputs = parser.parse_args()

input_data = inputs.contigs
output_dir = inputs.out
model_dict = inputs.model
kmeans_dict = inputs.kmean
tree_dict = inputs.tree
index_dict = inputs.index

# load taxonomy belief tree and tree node
node = load_node(tree_dict)
kmean = load_node(kmeans_dict)
index = load_node(index_dict)

#determine GPU or CPU, which device is used.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Specify the GPU device

model = Encoder().to(device)
model.load_state_dict(torch.load(model_dict),strict=False)


# defie dnatokenizer
batch = 64
max_length = 32768
dnatokenizer = CharacterTokenizer(
        characters=['A', 'C', 'G', 'T', 'N'], 
        model_max_length=max_length + 2, 
        add_special_tokens=False, 
        padding_side='left', 
    )
results = []
with torch.no_grad():
  for record in tqdm(SeqIO.parse(input_data, "fasta")):
    tbt = copy.deepcopy(node) 
    sequence_id = record.id
    sequence = str(record.seq)
    inds = []
    
    dnas = split_string(sequence,chunk_size=2000,step_size=400)
    for i in range(0, len(dnas), batch):
          batch_dnas = dnas[i:i+batch] if i+batch <= len(dnas) else dnas[i:]
          dna_token = dnatokenizer(batch_dnas,padding=True, return_tensors = 'pt')['input_ids'].to(device)
          embedding = model.get_dna(dna_token)
          ind = kmean.predict(embedding.cpu().numpy().tolist())
          inds.extend(ind)
    dnas = split_string(reverse_complement(sequence),chunk_size=2000,step_size=400)
    for i in range(0, len(dnas), batch):
          batch_dnas = dnas[i:i+batch] if i+batch <= len(dnas) else dnas[i:]
          dna_token = dnatokenizer(batch_dnas,padding=True, return_tensors = 'pt')['input_ids'].to(device)
          embedding = model.get_dna(dna_token)
          ind = kmean.predict(embedding.cpu().numpy().tolist())
          inds.extend(ind)
    add_values_node2(tbt,index,inds)
    max_sum,leaf = max_leaf_sum2(tbt["root"],confidence=0.6,length=len(dnas)*2)
    belief = max_sum/(len(dnas)*2)
    if leaf.level == "root":
      pname = "unclassified"
    else:
      pname = leaf.name + "_"  +leaf.level
    results.append(sequence_id+" "+pname + " "+ f"{belief:.2f}")
with open(output_dir, "w") as file:
    # 遍历字符串列表，并将每个元素写入文件，每个字符串后跟一个换行符
    for string in results:
        file.write(string + "\n")
  