"""Build the vocabulary print edition from the corrected online groups."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from lxml import html
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, KeepTogether, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
for name,file in [('English','LiberationSerif-Regular.ttf'),('EnglishBold','LiberationSerif-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/liberation/'+file))
def mixed(text,bold=False):
 return ''.join('<font name="'+('EnglishBold' if bold else 'English')+'">'+escape(t)+'</font>' if all(ord(c)<256 for c in t) else '<font name="STSong-Light">'+escape(t)+'</font>' for t in re.findall(r'[\x00-\xff]+|[^\x00-\xff]+',text))
page=html.parse(str(ROOT/'vocabulary.html'))
groups=page.xpath('//*[@class="vocab-group"]');count=len(page.xpath('//*[@class="vocab-entry"]'))
style=ParagraphStyle('entry',fontName='STSong-Light',fontSize=10.5,leading=15.5,spaceAfter=3,wordWrap='CJK')
noteStyle=ParagraphStyle('note',parent=style,fontSize=9.5,leading=14)
W,H=A4;margin=48;gap=24;width=(W-2*margin-gap)/2
class NumberedGroup(KeepTogether):pass
story=[]
for n,g in enumerate(groups,1):
 items=[]
 for node in g.xpath('.//*[@class="vocab-content"]/*'):
  if node.get('class')=='vocab-entry':
   term=node.xpath('.//*[@class="vocab-term"]')[0].text_content();definition=node.xpath('.//*[@class="vocab-definition"]')[0].text_content()
   items.append(Paragraph(mixed(term,True)+' '+mixed(definition),style))
  else:
   text=html.tostring(node,encoding='unicode').replace('<br>','\n');text=html.fromstring(text).text_content()
   items.append(Paragraph(mixed(text).replace('\n','<br/>'),noteStyle))
 # A two-cell table keeps the number aligned and each complete group in one column.
 from reportlab.platypus import Table,TableStyle
 table=Table([[Paragraph(f'{n:03}',ParagraphStyle('num',fontName='English',fontSize=7.5,leading=14)),items]],colWidths=[24,width-24])
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
 story.append(KeepTogether([table,Spacer(1,9)]))
def decorate(c,doc):
 c.setTitle(f'不背单词 · 合并纠错打印版 · {len(groups)}组 / {count}词条');c.setAuthor('True Path M')
 c.setFont('STSong-Light',8);c.drawString(margin,H-30,f'不背单词   {len(groups)}组 / {count}词条   更新于 2026-11-10')
 c.setFont('English',9);c.drawCentredString(W/2,26,str(doc.page))
doc=BaseDocTemplate(str(ROOT/'documents/vocabulary-notes.pdf'),pagesize=A4)
frames=[Frame(margin,48,width,H-100,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),Frame(margin+width+gap,48,width,H-100,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)]
doc.addPageTemplates(PageTemplate(id='two-columns',frames=frames,onPage=decorate));doc.build(story)
print(f'{len(groups)} groups / {count} entries')
