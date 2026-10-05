import re,html,subprocess,sys
def get(u):
    r=subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0',u],capture_output=True,text=True,errors='ignore');return r.stdout
def txt(h):
    h=re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>','',h,flags=re.S)
    h=re.sub(r'</(tr)>','\n',h); h=re.sub(r'</t[dh]>',' | ',h); h=re.sub(r'<(h\d|p|li|div)[^>]*>','\n',h)
    h=re.sub(r'<[^>]+>','',h);h=html.unescape(h);h=re.sub(r'[ \t]+',' ',h);h=re.sub(r'\n\s*\n+','\n',h);return h
if __name__=="__main__":
  for b in range(1,9):
      for pg in ['', 'bestiary/']:
          u=f'https://dungeon-crawler-carl.wiki/book-{b}/{pg}'
          h=get(u)
          if len(h)<2000: print('skip',u,len(h)); continue
          t=txt(h)
          # strip sidebar: start at 'On this page'
          i=t.find('On this page'); t=t[i:] if i>0 else t
          fn=f'book{b}{"-bestiary" if pg else "-overview"}.txt'
          open(fn,'w').write(t);print(fn,len(t))
