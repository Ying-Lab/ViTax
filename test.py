from model_vitax import *
import torch
a = Encoder()

a.load_state_dict(torch.load('/workspace/ICTV/model/model_save/19k3/trainf52000-gacc_0.899,gpre_0.844,grecal_0.8325201540202029.pth'),strict=False)