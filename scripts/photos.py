import json,re,html,urllib.request,concurrent.futures,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
parks=json.loads((root/'data/parks.json').read_text())
def get(p):
 page='https://www.nps.gov/'+p['code']+'/index.htm'
 try:
  raw=urllib.request.urlopen(page,timeout=35).read().decode()
  figures=re.findall(r'<figure\b.*?</figure>',raw,re.S)
  picks=[]
  for f in figures:
   src=re.search(r'src="([^"]+uploads[^"]+)"',f)
   credit=re.search(r'<span class="credit">(.*?)</span>',f,re.S)
   alt=re.search(r'alt="([^"]*)"',f)
   if src and credit:
    c=html.unescape(re.sub('<[^>]+>','',credit[1])).strip()
    if 'NPS' in c.upper() and '©' not in c:
     picks.append((html.unescape(src[1]),c,html.unescape(alt[1]) if alt else p['name']))
  if not picks: raise Exception('No credited NPS photo')
  src,credit,alt=picks[0]
  src=src.split('?')[0]
  if src.startswith('/'): src='https://www.nps.gov'+src
  out={**p,'image':'/assets/'+p['slug']+'.webp','credit':credit,'imageSource':src,'imageAlt':alt,'source':page}
  for suffix,width in [('',800),('-large',1800)] if p['slug'] in ['yosemite','zion','grand-teton','olympic'] else [('',800)]:
   url=src+'?width='+str(width)+'&quality=85&format=webp'
   data=urllib.request.urlopen(url,timeout=45).read()
   (root/'site/assets'/ (p['slug']+suffix+'.webp')).write_bytes(data)
  return out
 except Exception as e:
  print(p['slug'],str(e),flush=True);return {**p,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool: result=list(pool.map(get,parks))
(root/'data/photos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('Complete',len(result),'errors',sum('error' in p for p in result))
