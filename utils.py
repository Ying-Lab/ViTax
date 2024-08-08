
def split_string(input_string, chunk_size=2000, step_size=00):

    chunks = []
    length = len(input_string)


    if length < chunk_size:
        return [input_string]

    for i in range(0, length - chunk_size + 1, step_size):
        chunks.append(input_string[i:i + chunk_size])

    if (length - chunk_size) % step_size != 0:
        chunks.append(input_string[-chunk_size:])

    return chunks

def reverse_complement(dna):
    
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', "N": "N"}
    complemented = ''.join(complement[base] if base in complement else base for base in dna)
    return complemented[::-1]