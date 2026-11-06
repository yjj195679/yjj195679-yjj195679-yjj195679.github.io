"""Shared vector primitives for deterministic 408 teaching examples."""

import copy, html

def node(id,x,y,label,w=150,h=62,tone='base'):return dict(id=str(id),x=x,y=y,label=str(label),w=w,h=h,tone=tone)

def edge(a,b,label='',directed=True):return dict(a=str(a),b=str(b),label=label,directed=directed)

def frame(title,explain,nodes,edges=(),note='',wires=()):return dict(title=title,explain=explain,nodes=copy.deepcopy(nodes),edges=copy.deepcopy(edges),note=note,wires=copy.deepcopy(wires))

def row(values,active=(),done=(),y=100,prefix='v'):
 w=min(260,790/max(1,len(values)));return [node(prefix+str(i),40+i*w,y,v,w-8,80,'active' if i in active else 'done' if i in done else 'base') for i,v in enumerate(values)]

def tree(values,links):
 return [node(id,x,y,label,130,60,tone+(' rb-red' if '红' in label else ' rb-black' if '黑' in label else '')) for id,x,y,label,tone in values],[edge(a,b) for a,b in links]

styles='<style>.bg{fill:var(--diagram-bg,#fff)}.vb{fill:var(--diagram-fill,#eff4f9);stroke:var(--diagram-line,#356493);stroke-width:2}.vt{fill:var(--diagram-text,#17212f);font-family:SimSun,"Times New Roman",serif}.ve{stroke:var(--diagram-line,#356493);stroke-width:2;fill:none}.active .vb{stroke:var(--hand-example,#7444ad);stroke-width:4}.done .vb{stroke:var(--hand-memory,#237352);stroke-width:3}.vl{paint-order:stroke;stroke:var(--diagram-bg,#fff);stroke-width:7;stroke-linejoin:round}.rb-red .vb{stroke:var(--hand-key,#ac2537)}.rb-red .vt{fill:var(--hand-key,#ac2537)}.rb-black .vb{stroke:var(--diagram-text,#17212f);stroke-width:3}</style>'

def draw(s,slug):
 out=[];ns={n['id']:n for n in s['nodes']}
 for wire in s.get('wires',[]):out.append('<path class="ve" stroke-width="4" d="'+' '.join(('M' if i==0 else 'L')+str(x)+','+str(y) for i,(x,y) in enumerate(wire['points']))+'"/>')
 for ed in s['edges']:
  a,b=ns[ed['a']],ns[ed['b']];ax,ay=a['x']+a['w']/2,a['y']+a['h']/2;bx,byy=b['x']+b['w']/2,b['y']+b['h']/2;dx,dy=bx-ax,byy-ay
  start=min((a['w']/2+4)/abs(dx) if dx else 1e6,(a['h']/2+4)/abs(dy) if dy else 1e6);end=min((b['w']/2+8)/abs(dx) if dx else 1e6,(b['h']/2+8)/abs(dy) if dy else 1e6)
  mark=f' marker-end="url(#{slug}-arrow)"' if ed.get('directed',True) else ''
  out.append(f'<path class="ve"{mark} d="M{ax+dx*start},{ay+dy*start} L{bx-dx*end},{byy-dy*end}"/>')
  if ed['label']:out.append(f'<text class="vt vl" font-size="18" x="{(ax+bx)/2}" y="{(ay+byy)/2-12}" text-anchor="middle">{html.escape(ed["label"])}</text>')
 for n in s['nodes']:
  out.append(f'<g class="{n["tone"]}"><rect class="vb" x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="10"/>');lines=n['label'].split('\n');units=max(sum(1 if ord(c)>255 else .58 for c in line) for line in lines);font=min(19,(n['w']-14)/max(1,units),(n['h']-12)/len(lines)/1.3)
  for i,line in enumerate(lines):out.append(f'<text class="vt" font-size="{font}" text-anchor="middle" x="{n["x"]+n["w"]/2}" y="{n["y"]+n["h"]/2+(i-(len(lines)-1)/2)*26+7}">{html.escape(line)}</text>')
  out.append('</g>')
 return ''.join(out)
