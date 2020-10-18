import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
df = pd.DataFrame({ 'from':['A', 'B', 'C','A'], 'to':['D', 'A', 'E','C']})
df
 
# Build your graph
G=nx.from_pandas_edgelist(df, 'from', 'to')
layout = nx.planar_layout(G)
# All together we can do something fancy
nx.draw(G,pos=layout, with_labels=True, node_size=150, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=1, font_size=10, font_color="grey", font_weight="bold", edge_color="grey")
plt.savefig("path.png")