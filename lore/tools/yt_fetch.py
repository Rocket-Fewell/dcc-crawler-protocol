import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
out_dir = LORE_ROOT / "sources" / "youtube"
out_dir.mkdir(parents=True, exist_ok=True)
for vid in sys.argv[1:]:
    try:
        t = api.fetch(vid)
        txt = " ".join(s.text.replace("\n", " ") for s in t)
        (out_dir / f"{vid}.txt").write_text(txt)
        print(vid, len(txt))
    except Exception as e:
        print(vid, "ERR", str(e)[:150])
