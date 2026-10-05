import re,sys
b=sys.argv[1]; needle=sys.argv[2]
cur=None
for line in open(f"Book {b} Chapter Summaries.txt",errors='ignore'):
    m=re.match(r'^\|\s*(\d+|Epilogue|Interlude[^|]*|Prologue)\b',line)
    if m and len(line.strip())<80: cur=line.strip()
    if needle.lower() in line.lower(): print(b,'|',cur,'|',line.strip()[:120]); 
