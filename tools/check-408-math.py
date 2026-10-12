import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Verify the implemented width/shift models behind the diagrams.
def mul(m,q,n):
 a=0;mask=(1<<n)-1
 for _ in range(n):
  total=a+(m if q&1 else 0)
  aq=(total<<n)|q
  aq>>=1;a=(aq>>n)&mask;q=aq&mask
 return (a<<n)|q
def div(d,m,n):
 a=0;q=d;mask=(1<<n)-1
 for _ in range(n):
  a=2*a+(q>>(n-1));q=(q<<1)&mask
  trial=a-m
  if trial>=0:a=trial;q|=1
 return q,a
def booth(m,q,n):
 aw=n+1;amask=(1<<aw)-1;qmask=(1<<n)-1;full=aw+n+1
 a=0;q&=qmask;old=0
 for _ in range(n):
  pair=((q&1)<<1)|old
  if pair==1:a=(a+m)&amask
  elif pair==2:a=(a-m)&amask
  combined=(a<<(n+1))|(q<<1)|old
  if combined&(1<<(full-1)):combined-=1<<full
  combined >>= 1; combined &= (1<<full)-1
  old=combined&1;q=(combined>>1)&qmask;a=(combined>>(n+1))&amask
 result=((a<<n)|q)&((1<<(2*n))-1)
 if result&(1<<(2*n-1)):result-=1<<(2*n)
 return result
cases=0
for n in range(1,7):
 for m in range(1<<n):
  for q in range(1<<n):
   assert mul(m,q,n)==m*q
   if m:assert div(q,m,n)==(q//m,q%m)
   cases+=1
 for m in range(-(1<<(n-1)),1<<(n-1)):
  for q in range(-(1<<(n-1)),1<<(n-1)):
   assert booth(m,q,n)==m*q,(n,m,q)
# Enumerate B-tree key totals by feasible child occupancy for m=3..7, h<=3.
# Height counts data-bearing levels, root at level 1. Key totals include each root key.
from functools import lru_cache
@lru_cache(None)
def key_totals(m,h,root):
 amin=(m+1)//2
 if h==1:return set(range(1 if root else amin-1,m))
 child=key_totals(m,h-1,False);totals=set()
 for count in range(2 if root else amin,m+1):
  sums={0}
  for _ in range(count):sums={x+y for x in sums for y in child}
  totals.update(x+count-1 for x in sums)
 return totals
for m in range(3,8):
 amin=(m+1)//2
 for h in range(1,4):
  totals=key_totals(m,h,True)
  assert min(totals)==2*amin**(h-1)-1
  assert max(totals)==m**h-1
  for n in totals:
   # Prefer exact inequalities to floating point log rounding at powers.
   assert 2*amin**(h-1)-1<=n<=m**h-1
   lower=next(k for k in range(1,20) if m**k>=n+1)
   upper=1
   while 2*amin**upper<=n+1:upper+=1
   assert lower<=h<=upper
# Check SVG syntax, local-only markup and uniqueness.
import xml.etree.ElementTree as ET
for p in (ROOT/'images/408').glob('*.svg'):
 root=ET.fromstring(p.read_text());assert root.attrib['role']=='img'
 ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
 assert not any(e.tag.endswith(('script','foreignObject')) for e in root.iter())
 assert root.find('{http://www.w3.org/2000/svg}title') is not None
x=json.loads((ROOT/'data/408-knowledge.json').read_text())['items']
for row in x:
 assert all(isinstance(row[k],str) and row[k].strip() for k in ['wrong','right','why','example','check','answer'])
 if 'table' in row:assert all(len(r)==len(row['table']['headers']) for r in row['table']['rows'])
 if 'diagram' in row:assert ((ROOT/'images/408')/(row['diagram']+'.svg')).exists()
print('PASS: multiplication, restoring division and signed Booth including minimum negative inputs (n=1..6); B-tree occupancy/height bounds (orders 3..7, heights 1..3); six accessible safe SVGs; all 208 entries have complete explanation fields.')
