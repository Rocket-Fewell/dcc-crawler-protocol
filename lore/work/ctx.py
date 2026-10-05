import re,sys,glob
pat=re.compile(sys.argv[1],re.I)
w=int(sys.argv[2]) if len(sys.argv)>2 else 300
files=sys.argv[3:] or glob.glob('sources/youtube/*.txt')
for f in sorted(files):
    t=open(f,errors='ignore').read().replace('\n',' ')
    for m in pat.finditer(t):
        print(f.split('/')[-1], '::', t[max(0,m.start()-w):m.end()+w]); print()
