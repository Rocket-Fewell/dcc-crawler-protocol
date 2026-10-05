import sys
from youtube_transcript_api import YouTubeTranscriptApi
api=YouTubeTranscriptApi()
for vid in sys.argv[1:]:
    try:
        t=api.fetch(vid)
        txt=' '.join(s.text.replace('\n',' ') for s in t)
        open(f'/workspace/dcc-lore/sources/youtube/{vid}.txt','w').write(txt)
        print(vid,len(txt))
    except Exception as e:
        print(vid,'ERR',str(e)[:150])
