import simplejson
import sys
import pydot
from graphviz import Digraph

dot = Digraph(comment='Ceph Crush Map')
dot.graph_attr['size'] = '100,500'
dot.graph_attr['resolution'] = '200'
dot.graph_attr['bb'] = '0,0,4,8'
dot.format = 'png'
m = sys.argv[1]

data_file = open(m)

cm = simplejson.load(data_file)

print (str(cm)+'\n')

print (str(cm.keys())+'\n')
print (str(cm['devices'])+'\n')

graph = pydot.Dot('ceph_crushmap', graph_type='digraph')

for i in range(len(cm['devices'])):
  dot.node(str(cm['devices'][i]['id']), 'device: '+cm['devices'][i]['name'], {'style':'filled','fillcolor':'Yellow'}) 

for i in range(len(cm['buckets'])):
  dot.node(str(cm['buckets'][i]['id']), cm['buckets'][i]['type_name']+': '+cm['buckets'][i]['name'], {'style':'filled','fillcolor':'Red'}) 

for i in range(len(cm['rules'])):
  dot.node('rule'+str(i), str(cm['rules'][i]), {'style':'filled','shape':'box', 'fillcolor':'Blue'})

edges_list = []

for i in range(len(cm['buckets'])):
   for j in range(len(cm['buckets'][i]['items'])):
       dot.edge(str(cm['buckets'][i]['id']), str(cm['buckets'][i]['items'][j]['id']))
       edges_list.append(str(cm['buckets'][i]['id']) + str(cm['buckets'][i]['items'][j]['id']))

print str(edges_list)

print(dot.source)
dot.render('crushmap')
