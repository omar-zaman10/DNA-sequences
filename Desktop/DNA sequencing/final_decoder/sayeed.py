import numpy as np
import networkx as nx

minima = np.genfromtxt('min.data')
ts = np.genfromtxt('ts.data')

min_energies = minima[:,0]
ts_energies = ts[:,0]
ts_connections = ts[:,3:5].astype(int)
ts_connections = ts_connections-1

batch_size = 3

def Monotonic(G, min_energies):
   MSB = []
   for i in range(np.size(min_energies, axis=0)):
      monotonic = True
      energy_i = min_energies[i]
      i_edges = list(G.edges())
      for j in list(i_edges):
         min1 = j[0]
         min2 = j[1]
         if ((min1 == i) or (min2 == i)):
            if (min1 == min2):
               continue
            if (min1 == i):
               energy_j = min_energies[min2]
            else:
               energy_j = min_energies[min1]
         if (energy_j <= energy_i):
            monotonic = False
      if (monotonic):
         MSB.append(i)
   return MSB

def BarrierSelection(G, batch, banned_minima, barrier_cutoff, min_energies, ts_energies, ts_connections):
   for i in range(np.size(min_energies, axis=0)):
       if (i in batch):
           continue
       if (i in banned_minima):
           continue
       allowed = True
       for j in batch:
          barrier_height = BarrierHeight(G, i, j, min_energies, ts_energies, ts_connections)
          h1 = barrier_height-min_energies[i]
          h2 = barrier_height-min_energies[j]
          h = min(h1, h2)
          if (h < barrier_cutoff):
             allowed = False
       if (allowed):
          batch.append(i)
   return batch

def BarrierHeight(G, i, j, min_energies, ts_energies, ts_connections):
   G_cutting = G.copy()
   start_energy = max(min_energies[i], min_energies[j]) + 2.0
   for k in range(500):
      current_energy = start_energy-(k*0.01)
      for j in range(np.size(ts_energies)):
          if (ts_energies[j] > current_energy):
              try:
                 G_cutting.remove_edge(ts_connections[j,0], ts_connections[j,1])
              except:
                 pass
      connected_minima = nx.node_connected_component(G_cutting, j)
      if (i not in connected_minima):
         return current_energy
      if (len(connected_minima) == 1):
         return current_energy

r = np.max(min_energies) - np.min(min_energies)
energy_cutoff = np.min(min_energies)+0.8*r
if (energy_cutoff > -0.5):
   energy_cutoff = -0.5

barrier_cutoff = 0.2*r
if (barrier_cutoff > 0.2):
    barrier_cutoff = 0.2

banned_minima = []
for i in range(np.size(min_energies, axis=0)):
   if (min_energies[i] > energy_cutoff):
      min_energies[i] = energy_cutoff + 1e-3
      banned_minima.append(i)

G = nx.Graph()
for i in range(np.size(min_energies, axis=0)):
   G.add_node(i, energy=min_energies[i])
for i in range(np.size(ts_connections, axis=0)):
   G.add_edge(int(ts_connections[i,0]), int(ts_connections[i,1]), energy=ts_energies[i])
batch = Monotonic(G, min_energies)
print("Monotonic sequence basins = ", batch)
batch = BarrierSelection(G, batch, banned_minima, barrier_cutoff, min_energies, ts_energies, ts_connections)
print("Monotonic + barrier selection = ", batch)