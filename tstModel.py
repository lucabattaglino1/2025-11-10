# tstModel.py
from model.model import Model

mdl = Model()
mdl.buildGraph('Santa Cruz Bikes', 5)
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")
