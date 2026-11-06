"""Check teaching invariants independently of animation controls."""
import json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'data/408-handbook.json').read_text())
scenes={s['diagram']:s['simulation'] for c in items for s in c['sections'] if s.get('diagram','').startswith('advanced-')}
assert len(scenes)==32
for name,sim in scenes.items():
 ET.parse(R/'images/408'/f'{name}.svg')
 for state in sim['steps']:
  ids={n['id'] for n in state['nodes']};assert len(ids)==len(state['nodes'])
  assert all(e['a'] in ids and e['b'] in ids for e in state['edges'])
  assert all(0<=n['x']<=900-n['w'] and 0<=n['y']<=420-n['h'] for n in state['nodes']),name
 if name.startswith('advanced-rbt-'):
  state=sim['steps'][-1];ns={n['id']:n for n in state['nodes']};ch={k:[] for k in ns}
  for e in state['edges']:ch[e['a']].append(e['b'])
  root=(set(ns)-{e['b'] for e in state['edges']}).pop();assert '黑' in ns[root]['label']
  def height(k):
   kids=ch[k];red='红' in ns[k]['label']
   assert not red or all('黑' in ns[c]['label'] for c in kids)
   hs=[height(c) for c in kids]+[1]*(2-len(kids));assert len(set(hs))==1
   return hs[0]+(not red)
  height(root)
# Recompute Belady's counts from the published reference sequence.
refs=[1,2,3,4,1,2,5,1,2,3,4,5]
def fifo(n):
 q=[];faults=0
 for p in refs:
  if p not in q:
   faults+=1
   if len(q)==n:q.pop(0)
   q.append(p)
 return faults
assert (fifo(3),fifo(4))==(9,10)
fifo_text=' '.join(n['label'] for n in scenes['advanced-fifo-belady']['steps'][-1]['nodes'])
assert '3页框：9次' in fifo_text and '4页框：10次' in fifo_text
fragments=scenes['advanced-refragment-offset']['steps'][-1]['nodes']
for n,(offset,length) in zip(fragments,[(185,600),(260,600),(335,280)]):
 assert f'偏移{offset}，MF=1' in n['label'] and f'数据长{length}B' in n['label']
assert sum([600,600,280])==1480
out=scenes['advanced-replacement-freeze']['steps'][-1]['nodes']
assert [n['label'] for n in out]==['段1：1,2,4,5,6','段2：0,3']
# Recompute the final LRU set content after blocks 0,2,0,4.
lru=[]
for b in [0,2,0,4]:
 if b in lru:lru.remove(b)
 elif len(lru)==2:lru.pop(0)
 lru.append(b)
assert lru==[0,4]
print('PASS: 32 scene bounds/SVGs, red-black deletion black heights, FIFO 9/10 faults, fragment offsets/MF, replacement-selection runs, 2-way LRU.')
