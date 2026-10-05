import re,sys
def intro(name,n=900):
    try: t=open("pages/"+name+".txt").read()
    except: return "(missing)"
    # strip infobox lines
    lines=[l for l in t.split("\n") if l.strip() and not re.match(r'^\s*[\|\*\{\}!]',l) and not l.startswith("==") and not l.startswith("<")]
    s=" ".join(lines)
    s=re.sub(r'\{\{[^}]*\}\}','',s)
    s=re.sub(r'\[\d[^\]]*\]','',s)
    return s[:n]
for nm in sys.argv[2:]:
    print("##",nm,":",intro(nm,int(sys.argv[1])))
