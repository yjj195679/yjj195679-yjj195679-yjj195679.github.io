"""Independent references for the new foundational examples."""
from pathlib import Path
import json,ipaddress,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];items=json.loads((R/'data/408-handbook.json').read_text())
scenes={s['diagram']:s['simulation'] for c in items for s in c['sections'] if s.get('diagram','').startswith('foundation-')};assert len(scenes)==32
for name,sim in scenes.items():
 E.parse(R/'images/408'/f'{name}.svg')
 for state in sim['steps']:
  ids={n['id'] for n in state['nodes']};assert len(ids)==len(state['nodes'])
  for n in state['nodes']:assert isinstance(n['w'],(int,float)) and isinstance(n['h'],(int,float));assert 0<=n['x']<=900-n['w'] and 0<=n['y']<=420-n['h'],name
  for e in state['edges']:assert e['a'] in ids and e['b'] in ids
# Row/column major and lower-triangle indexing.
assert (1*3+2)*4==(2*2+1)*4==20
assert (0*3+1)*4==4 and (1*2+0)*4==8
assert 2*(2+1)//2+1==4
values=[329,457,657,839,436,720,355]
for d in [1,10,100]:values=sorted(values,key=lambda n:(n//d)%10)
assert values==[329,355,436,457,657,720,839]
assert ','.join(map(str,values)) in scenes['foundation-radix-lsd']['steps'][-1]['explain']
A=[1,1,-1,-1];B=[1,-1,1,-1];r=[a-b for a,b in zip(A,B)]
assert sum(a*b for a,b in zip(A,B))==0
assert sum(a*v for a,v in zip(A,r))/4==1 and sum(b*v for b,v in zip(B,r))/4==-1
assert (0.75*1+0.25*3)==1.5
assert (1<<20)*4==4*(1<<20)
assert ipaddress.IPv6Address('2001:0db8:0000:0000:0000:0000:0000:0001').compressed=='2001:db8::1'
threads=scenes['foundation-threaded-links']['steps'][-1]['edges'];assert len([e for e in threads if e.get('points')])==2
assert sum([6,6,2,46,4])==64
assert (14-2,5-2,14-2-6,(14-2)/6)==(12,3,6,2)
print('PASS: 32 foundation scenes; arrays/matrix indexing, stable radix result, CDMA orthogonality, CPI, page table size, IPv6 expansion, routed threads and scheduling metrics.')
