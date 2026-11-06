"""Independent arithmetic and state checks for the systems expansion."""
from pathlib import Path
import json,struct,ipaddress,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];items=json.loads((R/'data/408-handbook.json').read_text());scenes={s['diagram']:s['simulation'] for c in items for s in c['sections'] if s.get('diagram','').startswith('systems-')};assert len(scenes)==32
for name,sim in scenes.items():
 E.parse(R/'images/408'/f'{name}.svg')
 for st in sim['steps']:
  ids={n['id'] for n in st['nodes']};assert len(ids)==len(st['nodes'])
  assert all(0<=n['x']<=900-n['w'] and 0<=n['y']<=420-n['h'] for n in st['nodes']),name
  assert all(e['a'] in ids and e['b'] in ids for e in st['edges'])
p='abaabcac';nxt=[0]
for j in range(2,len(p)+1):
 prefix=p[:j-1];border=max([0]+[k for k in range(1,len(prefix)) if prefix[:k]==prefix[-k:]])
 nxt.append(border+1)
nv=[0]
for j in range(2,len(p)+1):
 k=nxt[j-1];nv.append(k if p[j-1]!=p[k-1] else nv[k-1])
assert nxt==[0,1,1,2,2,3,1,2] and nv==[0,1,0,2,1,3,0,2]
assert ','.join(map(str,nv)) in scenes['systems-nextval']['steps'][-1]['nodes'][-1]['label']
heap=[int(n['label']) for n in scenes['systems-bottom-up-heap']['steps'][-1]['nodes']]
assert sorted(heap)==[1,2,3,4,5,6]
assert all(heap[(i-1)//2]>=heap[i] for i in range(1,len(heap)))
assert [int(n['label']) for n in scenes['systems-shell-gaps']['steps'][-1]['nodes']]==[1,3,4,5,6,7,8,9]
assert struct.unpack('>f',struct.pack('>f',16777217))[0]==16777216
assert ((2*4+1)*8+4-1)*512==38400
assert 0x1004+12==0x1010
raw=[0x45,0x7e,0x7d,0];wire=[]
for b in raw:wire.extend([0x7d,b^0x20] if b in [0x7d,0x7e] else [b])
assert wire==[0x45,0x7d,0x5e,0x7d,0x5d,0]
back=[];i=0
while i<len(wire):
 if wire[i]==0x7d:i+=1;back.append(wire[i]^0x20)
 else:back.append(wire[i])
 i+=1
assert back==raw
assert (int(ipaddress.IPv4Address('224.1.2.3'))&0x7fffff)==(int(ipaddress.IPv4Address('239.129.2.3'))&0x7fffff)==0x010203
assert abs(8+1000/120/2+1000/120/200-12.208333333333334)<1e-9
assert len(set([3,0,1])&set([0,1,2]))==2 and not set([2,3])&set([0,1])
print('PASS: 32 systems scenes; next/nextval, max heap, Shellsort, binary32 rounding, CHS and PC arithmetic, PPP round trip, multicast collision, disk latency and sequence-window overlap.')
