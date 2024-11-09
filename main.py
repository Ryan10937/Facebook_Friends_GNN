import networkx as nx
import numpy as np
import os

def make_feature_dict(data_path):

  # feat_path = f'{data_path}{node_num}.feat'
  ego_node_feat_paths = [os.path.join(data_path,x) for x in os.listdir(data_path) if x.split('.')[-1]=='feat']
  print(ego_node_feat_paths)
  feature_dict={}
  for path in ego_node_feat_paths:
    with open(path,'r') as f:
      dump = f.read()
    lines = dump.split('\n')
    lines_split = [x.split(' ') for x in lines]
    feature_dict[int(path.split('/')[-1].split('.')[0])] = {int(x[0]):[int(y) for y in x[1:]] for x in lines_split if len(x[0])>0}
  return feature_dict



def build_graph(data_path:str):
  combined_txt_file = os.path.join(data_path,'facebook_combined.txt')
  with open(combined_txt_file,'r') as f:
    txt_dump = f.read()
  edge_lines = txt_dump.split('\n')
  edges = [tuple([int(y) for y in x.split(' ') if y!=',' and len(y)>0]) for x in edge_lines]
  unique_node_names = np.unique([int(y) for x in edge_lines for y in x.split(' ') if len(y)>0])

  graph = nx.Graph()
  feature_dict = make_feature_dict(os.path.join(data_path,'facebook'))
  for node in unique_node_names:
    try:
      feature_dict[node] = feature_dict[node]
    except:
      feature_dict[node] = {}

  graph.add_nodes_from([tuple([node,feature_dict[node]]) for node in unique_node_names])
  for ed in edges:
    if len(ed)>0:
      graph.add_edge(ed[0],ed[1])
    else:
      print('ed',ed)
    

  return graph
if __name__ == '__main__':

  data_path = 'data/'
  graph = build_graph(data_path)
  n=124
  neighbors = graph.neighbors(n)
  edges_from_n = [(n, neighbor) for neighbor in neighbors]
  print(edges_from_n)  

  print(graph.nodes[0][335])
