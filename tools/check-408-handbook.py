"""Check static content without optional Python dependencies."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,html):
  super().__init__(convert_charrefs=True);self.cards={};self.ids=[];self.links=[];self.current=None;self.depth=0;self.annotations={};self.ann=None;self.errors=0;self.feed(html)
 def handle_starttag(self,tag,attributes):
  a=dict(attributes)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if 'katex-error' in a.get('class','').split():self.errors+=1
  if tag=='details':
   if 'handbook408-card' in a.get('class','').split():self.current=a['id'];self.cards[self.current]=[];self.annotations[self.current]=[];self.depth=0
   if self.current:self.depth+=1
  if tag=='annotation' and self.current and a.get('encoding')=='application/x-tex':self.ann=[]
 def handle_endtag(self,tag):
  if tag=='annotation' and self.ann is not None:
   self.annotations[self.current].append(''.join(self.ann));self.ann=None
  if tag=='details' and self.current:
   self.depth-=1
   if self.depth==0:self.current=None
 def handle_data(self,text):
  if self.current:self.cards[self.current].append(text)
  if self.ann is not None:self.ann.append(text)
data=json.loads((root/'data/408-handbook.json').read_text());page=Page((root/'408-handbook.html').read_text())
assert len(page.cards)==len(data)
assert len(set(x['id'] for x in data))==len(data)
plain=lambda x:re.sub(r'\s+','',re.sub(r'\*\*(.*?)\*\*',r'\1',str(x)))
points=0
for x in data:
 raw=''.join(page.cards[x['id']]);content=plain(raw)
 for section in x['sections']:
  for key in ['paragraphs','bullets','points']:
   for text in section.get(key,[]):assert plain(text) in content,(x['title'],text);points+=1
  table=section.get('table')
  if table:
   for row in table['rows']:
    assert len(row)==len(table['headers']),x['title']
    for cell in row:assert plain(cell) in content,(x['title'],cell)
  if section.get('code'):assert section['code'] in raw,x['title']
  for formula in section.get('formulas',[]):assert formula['tex'] in page.annotations[x['id']],(x['title'],formula['tex'])
assert not page.errors
assert '真题' not in ''.join(''.join(x) for x in page.cards.values())
assert len(page.ids)==len(set(page.ids)), 'duplicate document IDs'
target_ids={root/'408-handbook.html':set(page.ids)}
for url in page.links:
 if url.startswith(('https:','http:','mailto:')):continue
 path,_,frag=url.partition('#');target=root/path if path else root/'408-handbook.html'
 assert target.exists(),url
 if frag and target.suffix=='.html':
  if target not in target_ids:target_ids[target]=set(Page(target.read_text()).ids)
  assert frag in target_ids[target],url
print(f'PASS: {len(data)} complete handbook cards; {points} paragraphs/bullets; tables, code, static MathML, unique IDs and local links.')
