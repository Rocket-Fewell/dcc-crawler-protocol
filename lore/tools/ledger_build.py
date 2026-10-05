#!/usr/bin/env python3
"""Builds CANON-LEDGER.md (Pass 4, 2026-10-03). Every quote is pulled programmatically from a local source file;
run `python3 tools/ledger_check.py` afterwards to re-verify.  NOTE: future passes APPEND to the ledger by hand
(see ledger-rules.md); do NOT re-run this script over a ledger that has had manual appends -- it writes to
work/ledger-rebuild.md unless --force is given."""
import sys,re,os,collections,datetime
sys.path.insert(0,'/workspace/dcc-lore/tools')
from wk import D,cats,find_templates,fields,clean
from ledger_lib import *
from ledger_ach import build_achievements
from ledger_spec_mech import MECH
from ledger_spec_other import *
TODAY='2026-10-03'
COUNTS=collections.OrderedDict()
def q(s): return '"'+esc(s)+'"' if s else '—'
def ibox(title):
    t=D.get(title)
    if not t: return {}
    for nm,b,i,j in find_templates(t):
        if nm.lower() in ('character info','spells','skills','race infobox','class','item','achievement'):
            f=fields(b); out={}
            for k,v in f.items():
                c=clean(v); c=re.sub(r'\[B\d+ ch[^\]]*\]','',c); c=re.sub(r'\[B\d+ [^\]]*\]','',c); c=re.sub(r'\s+',' ',c).strip(' ;')
                if c: out[k]=c
            return out
    return {}
def short(s,n=90): 
    s=s.strip()
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'…'
def conf_for(qte,cites,page_cites,extra_ok):
    if qte is None: return 'UNVERIFIED'
    if cites: return 'VERIFIED (cite %s)'%fmt_cite(cites[0])
    if extra_ok: return 'VERIFIED (2 sources)'
    if page_cites: return 'VERIFIED (page cite %s)'%fmt_cite(page_cites[0])
    return 'WIKI-ONLY'
def tally(sec,conf):
    c=conf.split(' ')[0]
    COUNTS.setdefault(sec,collections.Counter())[c]+=1
def extras_ok(extras):
    tags=[];ok=False
    for tag,kw in extras:
        t=src_text(tag)
        if t and kw.lower() in t.lower(): tags.append(tag);ok=True
    return ok,tags
def page_cites(title):
    return cites_in(page(title) or '')
def pq(title,pattern=None):
    """best quote for a page"""
    if pattern:
        r=find_sentence(title,pattern)
        if r[0]: return r
    r=ai_quote(title)
    if r[0]: return r
    return lead_quote(title)
out=[]
W=out.append
# ---------------- header
W('''# Canon Ledger - Dungeon Crawler Carl
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: 2026-10-03
Summary: Master "hard memory" of DCC canon findings, each with a source quote (<=25 words), source tag and VERIFIED / WIKI-ONLY / UNVERIFIED confidence. Spoilers through Book 8.

## 0. How to read this ledger (rules in brief; full procedure in `ledger-rules.md`)
- **Nothing here was checked against the novels' text.** Every source is a fan wiki mirror, a fan site, or a YouTube recap/transcript kept in this folder (`raw/pages/`, `sources/`). "VERIFIED" is therefore a *bookkeeping label with a defined meaning*, not proof from the book.
- **Confidence labels**
  - **VERIFIED** = (a) the wiki page/row carries a book-chapter citation (shown as `cite B# ch#`; `page cite` = a chapter cite exists elsewhere on the same page but not on the quoted sentence; `chapter-summary row` = the row comes from the wiki's per-chapter summary table), **or** (b) two independent source families agree (shown as `2 sources`; families: Fandom wiki, dungeon-crawler-carl.wiki `FW2`, dungeoncrawlercarl.nl `NL`, YouTube recap `YT`). The Fandom wiki's master `Achievement` page and its per-achievement pages are the *same* family and never count as two sources.
  - **WIKI-ONLY** = one wiki source, no chapter citation.
  - **UNVERIFIED** = no usable quote, incomplete wiki infobox, unresolved conflict, single fan-site claim, or a claim the sources themselves hedge.
- **Quotes** are exact substrings of the cited local file (cites and whitespace normalised; a leading/trailing `…` marks trimming; max 25 words). Wiki prose is a *wiki* quote, not novel text; achievement/AI text is the wiki's transcription of System text. `tools/ledger_check.py` re-verifies every quote mechanically.
- **Source tags**: `W:<page>` = `raw/pages/<page>.txt` (Fandom wiki mirror); `FW2:<file>` = `sources/fanwiki/`; `NL:<file>` = `sources/nl/`; `YT:<id>` = `sources/youtube/<id>.txt` (auto-captions; garbled names). Reddit was blocked (403) and is only referenced in the Conflicts section as unread snippets.
- **IDs** are permanent (A-, M-, L-, S-/P-/I-/C-/R-, B-, H-, T-, X-). **Date** column = date the entry was added. Never renumber; append (see `ledger-rules.md`).
- Chapter cite style `B1 ch5` = Book 1, chapter 5 as cited by the wiki. Floor ordinals: F3 = Third Floor. Book to floors: B1 F1-2, B2 F3, B3 F4, B4 F5, B5 F6-7, B6 F8, B7 F9, B8 F10-11.

''')
# ---------------- 1 achievements
rows,stats,conflicts,noquote,fw2=build_achievements()
W('## 1. Achievements\n')
W('Columns: ID | Name | Floor / Book(s) cited | Trigger (wiki infobox) | System text quote (<=25 words) | Reward (infobox, else System text) | Source tag | Confidence | Date\n')
W('| ID | Name | Floor / Book | Trigger | System text (exact quote) | Reward | Source | Confidence | Date |\n|---|---|---|---|---|---|---|---|---|')
for n,r in enumerate(rows,1):
    aid='A-%03d'%n
    fl=('; '+'; '.join(r['flags'])) if r['flags'] else ''
    qt=q(r['quote'])
    if r['quote'] is None: qt='— (none captured)'
    W(f"| {aid} | {esc(r['name'])} | {r['loc']} | {esc(r['trig'])} | {qt} | {esc(r['reward'])} | {'; '.join(r['tags'])} | {r['conf']}{esc(fl)} | {TODAY} |")
    tally('1 Achievements',r['conf'])
W('')
W(f"_Second-source agreement (Fandom + FW2 fan wiki, same reward box) found for: {', '.join(sorted({k.replace(' Achievement','') for k,_ in fw2}))}. FW2 text for other Book 3/4 achievements says 'Unknown' or has no reward text, so they gain no second source._\n")
# ---------------- 2 mechanics
W('## 2. Mechanics rulings\n')
W('| ID | Ruling (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|')
for i,r,p,pat,ex,n in MECH:
    qte,c=find_sentence(p,pat)
    ok,tags=extras_ok(ex)
    if i=='M-005': ok,tags=False,[]
    cf=conf_for(qte,c,page_cites(p),ok)
    src=['W:'+resolve(p)]+tags
    W(f"| {i} | {esc(r)} | {q(qte)} | {'; '.join(src)} | {cf} | {TODAY} |")
    tally('2 Mechanics rulings',cf)
W('')
# ---------------- 3 loot boxes
W('## 3. Loot box facts\n')
W('| ID | Fact (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|')
for i,f,p,pat,ex in LOOT:
    qte,c=find_sentence(p,pat)
    cf=conf_for(qte,c,page_cites(p),False)
    W(f"| {i} | {esc(f)} | {q(qte)} | W:{resolve(p)} | {cf} | {TODAY} |")
    tally('3 Loot box facts',cf)
# box-type index
W('\n### 3b. Loot box type index (from `catalog/loot-boxes.md`; one row per box page)\n')
W('| ID | Box | Quote (wiki lead, <=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|')
boxes=[]
for line in open(ROOT+'/catalog/loot-boxes.md'):
    m=re.match(r'^\| ([^|]+?) \|',line)
    if m and not line.startswith('| Box') and not line.startswith('|---'): boxes.append(m.group(1).strip())
n=0
for b in boxes:
    if b=='Loot Boxes': continue
    cand=[b,b.replace("'",'’')]
    pg=next((c for c in cand if exists(c)),None)
    if not pg: continue
    qte,c=lead_quote(pg)
    if not qte: qte,c=ai_quote(pg)
    cf=conf_for(qte,c,page_cites(pg),False)
    n+=1
    W(f"| L-B{n:02d} | {esc(b)} | {q(qte)} | W:{resolve(pg)} | {cf} | {TODAY} |")
    tally('3b Loot box type index',cf)
W('')
# ---------------- 4 highlights
def hi_table(title,idp,spec,kind):
    W(f'\n### {title}\n')
    W('| ID | Name | Key facts (wiki infobox) | Quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|---|')
    keys={'skill':['cost','casting','cooldown','target','duration','effect','users'],'spell':['cost','casting','cooldown','target','duration','effect','users'],
          'item':['type','effects','source'],'class':['type','prerequisites','crawlers'],'race':['type','bonuses','penalties','floors']}[kind]
    for i,label,p,pat in spec:
        ib=ibox(resolve(p))
        facts='; '.join(f'{k}: {short(ib[k],60)}' for k in keys if k in ib)[:200] or '—'
        qte,c=pq(p,pat)
        cf=conf_for(qte,c,page_cites(p),False)
        W(f"| {i} | {esc(label)} | {esc(facts)} | {q(qte)} | W:{resolve(p)} | {cf} | {TODAY} |")
        tally(title,cf)
W('## 4. Skills / Spells / Items / Classes / Races highlights')
hi_table('4a Skills','S',SKILLS,'skill'); hi_table('4b Spells','P',SPELLS,'spell'); hi_table('4c Items','I',ITEMS,'item')
hi_table('4d Classes','C',CLASSES,'class'); hi_table('4e Races','R',RACES,'race')
# ---------------- 5 bosses
W('\n## 5. Bosses\n')
W('Tier ladder entry is M-014. Level / species / status come from the wiki infobox; the quote is the page\'s own text.\n')
W('| ID | Boss | Level / species / status (infobox) | Quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|---|')
bn=0
for b in BOSSES:
    if not exists(b): continue
    ib=ibox(resolve(b)); bn+=1
    facts='; '.join(f'{k}: {short(ib[k],50)}' for k in ('level','species','status','first_appearance') if k in ib) or '—'
    qte,c=find_sentence(b,r'[Ll]evel \d+|boss|Boss')
    if not qte: qte,c=pq(b)
    cf=conf_for(qte,c,page_cites(b),False)
    W(f"| B-{bn:03d} | {esc(b)} | {esc(facts)} | {q(qte)} | W:{resolve(b)} | {cf} | {TODAY} |")
    tally('5 Bosses',cf)
# ---------------- 6 characters
W('\n## 6. Characters\n')
W('| ID | Character | Species / class / level / status (infobox) | Quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|---|')
hn=0
for ch in CHARS:
    if not exists(ch): continue
    ib=ibox(resolve(ch)); hn+=1
    facts='; '.join(f'{k}: {short(ib[k],55)}' for k in ('species','class','level','status') if k in ib) or '—'
    qte,c=lead_quote(ch)
    cf=conf_for(qte,c,page_cites(ch),False)
    W(f"| H-{hn:03d} | {esc(ch)} | {esc(facts)} | {q(qte)} | W:{resolve(ch)} | {cf} | {TODAY} |")
    tally('6 Characters',cf)
# ---------------- 7 plot beats
W('\n## 7. Plot beats by book\n')
W('Quote = the wiki chapter-summary row (first <=25 words). Basis: `chapter-summary row` (cites the book chapter) and, where a Mana Toast/Bookborn recap transcript also contains the beat keyword, `+YT` (2 sources). Transcript keyword match is a weak check (auto-captions).\n')
W('| ID | Book / chapter | Beat (paraphrase) | Wiki chapter-summary quote (<=25 words) | Source | Confidence | Date |\n|---|---|---|---|---|---|---|')
def crow(b,ch):
    t=page(f'Book {b} Chapter Summaries')
    for m in re.finditer(r'\|-\n\|([^\n|]*)\n\|([^\n]*)',t):
        if re.match(r'^%s(\s|$|-)'%re.escape(ch),m.group(1).strip()): return m.group(2)
pn=0
for b,ch,beat,yt,kw in PLOT:
    raw=crow(b,ch)
    if not raw: print('MISSING',b,ch);continue
    pn+=1
    qt=trim_words(strip_cites(raw),25)
    src=[f'W:Book {b} Chapter Summaries']
    basis='chapter-summary row'
    if yt:
        t=src_text('YT:'+yt)
        if t and kw.lower() in t.lower(): src.append('YT:'+yt); basis+=' +YT'
    cf='VERIFIED (%s)'%basis if '+YT' in basis else 'VERIFIED (%s)'%basis
    lab=f'B{b} ch{ch}' if ch[0].isdigit() else f'B{b} {ch}'
    W(f"| T-{pn:03d} | {lab} | {esc(beat)} | {q(qt)} | {'; '.join(src)} | {cf} | {TODAY} |")
    tally('7 Plot beats',cf)
W('')
# ---------------- 8 conflicts
W('## 8. Conflicts / Unverified\n')
W('Status: OPEN = unresolved; PREFERRED = one reading chosen but not proven; REJECTED = claim dropped. "—" in a quote column means no verbatim source line was available (claim came from a catalog note, a recap paraphrase or an unread snippet).\n')
W('| ID | Topic | Reading A (quote or note) | Source A | Reading B (quote or note) | Source B | Status | Date |\n|---|---|---|---|---|---|---|---|')
CONF=[]
def cq(p,pat): 
    r=find_sentence(p,pat)[0]; return r
def fq(tag,pat,maxw=25):
    t=src_text(tag)
    if not t: return None
    t=norm_ws(t)
    m=re.search(r'[^.]*'+pat+r'[^.]*\.?',t,flags=re.I)
    if not m: return None
    return trim_words(m.group(0).strip(),maxw)
def rowq(book,ch,kw,maxw=25):
    raw=crow(book,ch)
    st=strip_cites(raw)
    for s in split_sentences(st):
        if kw.lower() in s.lower():
            return trim_words(s.strip(),maxw)
    return None

CONF=[
("Hunter trophy: claw or hand?",q(rowq(5,'8','receives a claw')),'W:Book 5 Chapter Summaries',q(find_sentence('Gore Golem Spell','trade hunter hands')[0]),'W:Gore Golem Spell','PREFERRED: hands (item/prize pages + recap); chapter summary wording likely slip'),
("Who marked Miriam Dom with a Ring (B5 ch47)?",q(find_sentence("Enchanted Night Wyrm's Ring of Divine Suffering",'activated Prepotente')[0]),"W:Enchanted Night Wyrm's Ring of Divine Suffering",'— (Mana Toast B5 recap says Carl secretly marked her; recap paraphrase, not re-read for this pass)','YT:TKcMxF2dA3w (paraphrase)','OPEN'),
("Gate loan return date",q(rowq(5,'3','give up the Gate temporarily')),'W:Book 5 Chapter Summaries',q(find_sentence('Gate of the Feral Gods','receipt promising its return')[0]),'W:Gate of the Feral Gods','PREFERRED: return on the ninth floor (Gate page); ch1 summary phrase "until level 9" is in catalog notes, row text above does not repeat it'),
("Mimic Rex kill method",q(fq('FW2:book3-events-mimic-rex-confrontation',"Doomsday Nuke")),'FW2:book3-events-mimic-rex-confrontation',q(rowq(3,'33','Grull kills the Mimic')),'W:Book 3 Chapter Summaries','PREFERRED: Fandom (Grull kills the Mimic); FW2 rejected'),
("Carl's level at end of Book 8",'— wiki infobox level field: '+ibox('Carl')['level'],'W:Carl','— (a Reddit snippet summary said L81; thread text not read, Reddit 403)','R (unread)','OPEN: prefer wiki L84'),
("Floor 11 headcount: 23 vs 31",q(rowq(8,'88','23 remaining crawlers')),'W:Book 8 Chapter Summaries','— (Mana Toast B8 recap: 203 reached / 172 deals / 31 undecided at an earlier moment; recap numbers not re-quoted)','YT:kk6nspvVf_M (paraphrase)','OPEN (likely different moments)'),
("Denise origin (Floor 7 goose?)",'— (fan-wiki claims a Floor 7 origin; no quote kept)','FW2 (catalog note)','— (Floor 7 is a ~10 minute pod level with no mobs)','W:Seventh Floor (M-040)','REJECTED/UNVERIFIED: single fan-wiki source'),
("Meadow Lark descent (B1 ch41 vs ch47)",'— (catalog note: wiki says group descends to the Third Floor at both ch41 and ch47)','W:Book 1 Chapter Summaries (catalog note)','— (page header lists Floors 1-2 only)','W:Book 1 Chapter Summaries','OPEN'),
("Ball of Swine tier","— (wiki: Borough boss)",'W:Ball of Swine',"— (Mana Toast caption 'burrow boss')",'YT:j6jRXuCgsAA','PREFERRED: Borough boss (caption error)'),
("Cookbook numbering (25th holder vs 24th edition)",'— (Crawler\'s Cookbook site: 25th holder, authored in season 15)','FS (catalog note)','— (FW2: 24th Ed.)','FW2 (catalog note)','OPEN'),
("Which child is the Scavenger's Daughter",'— (B8 ch69 Rosetta myth: Nekhebit had three children)','W (reconciliation)','— (B7 ch78 War Mages claim to have found the Scavenger\'s Daughter)','W (reconciliation)','OPEN'),
("XP curve","— (no published table; wiki says formula never defined, per Pass 3 notes)",'W (catalog note; phrase not in local mirror)','— (Reddit users assume steep curve; explicitly an assumption)','R (unread snippets)','OPEN'),
("Unconscious threshold","— (Half-Splat leaves 5%; Survivor's Box <10% Carl / <5% Donut; Martyr's Path at 5%)",'W (catalog note)','— (wiki Health page lists ~6% under Speculation)','W:Health','OPEN'),
("Mongo/Kiwi pack size 40 vs 36 vs 30","— (B5 recap numbers vary)",'YT:TKcMxF2dA3w','— (attrition plausible)','—','OPEN'),
("Li Na stat cap 300",q(find_sentence("Enchanted Night Wyrm's Ring of Divine Suffering",'maxing every base stat')[0]),"W:Enchanted Night Wyrm's Ring of Divine Suffering",'— (a recap said "max level 300")','YT (catalog note)','PREFERRED: stats maxed at 300, not level'),
("Orthrus parentage",'— (FW2: pet of a god named Geyrun)','FW2 (catalog note)','— (no Fandom corroboration read)','—','UNVERIFIED: single fan source'),
("Book 8 title","— (an early request listed Book 8 as 'The Perfect Scramble'; no such DCC book found)",'INDEX.md (Pass 1 correction note)','— (Fandom wiki, PRH, Goodreads, publisher: A Parade of Horribles)','W/WEB (INDEX.md)','RESOLVED: A Parade of Horribles'),
("Book 9 release date","— (no announced date; working title 'The Beautiful Place')",'WEB (reconciliation D)','— (fan claims of 2027)','WEB (unverified)','OPEN: do not cite a date'),
("Gate of the Feral Gods other components","— (fate of other components/watches not stated)",'W (reconciliation)','—','—','OPEN'),
("Celestial tax explains Celestial scarcity","— (wiki Loot Boxes/Celestial pages state it)",'W:Celestial','— (not confirmed against text)','—','WIKI-ONLY / OPEN'),
("Skills level via d20 checks","— (YouTube short claim)",'YT (search summary)','— (wiki: skills level by use)','W:Skills','REJECTED'),
("Hekla's death accidental?","— (consensus yes: Katia's misaimed Rush)",'W; FS; R snippets','—','—','PREFERRED (consensus), not book-checked'),
("Signet 'Ink Marauder' spell at her death","— (wiki ch74/75: self-sacrifice opens the seal)",'W:Book 5 Chapter Summaries','— (recap adds an ink marauder spell; caption-level only)','YT:TKcMxF2dA3w','OPEN'),
("Mana Toast 'extra Pineapple Cabaret chapters' (B8)","— (bonus chapters not covered by any local source)",'YT:kk6nspvVf_M','—','—','OPEN (gap)'),
("Fan stat estimate for Carl after Book 8","— (fan guess: STR ~115 base etc.)",'R (unread snippet)','— (no official stat sheets)','—','REJECTED as canon; parked'),
]
for i,(t,a,sa,b,sb,st) in enumerate(CONF,1):
    W(f"| X-{i:03d} | {esc(t)} | {a} | {esc(sa)} | {b} | {esc(sb)} | {esc(st)} | {TODAY} |")
    COUNTS.setdefault('8 Conflicts (hand-curated)',collections.Counter())['rows']+=1
# generated achievement conflicts
W('\n### 8b. Achievement-table flags (generated)\n')
W('| ID | Achievement | Flag | Date |\n|---|---|---|---|')
for i,(nm,fl) in enumerate(conflicts,1):
    W(f"| X-A{i:02d} | {esc(nm)} | {esc('; '.join(fl))} | {TODAY} |")
COUNTS.setdefault('8b Achievement flags',collections.Counter())['rows']=len(conflicts)
unv=[r for r in rows if r['conf'].startswith('UNVERIFIED')]
W(f"\nAchievements with UNVERIFIED confidence: {', '.join(r['name'] for r in unv)}.\n")
# ---------------- appendix: counts + append area
W('## 9. Append log (future passes add entries below; see `ledger-rules.md`)\n')
W('<!-- APPEND-ONLY BELOW THIS LINE. Use the next free ID in the section prefix; put the date in the Date column; add a line to the Pass log. -->\n')
W('### Pass log\n| Date | Pass | Who | Summary |\n|---|---|---|---|\n| 2026-10-03 | 4 | DCC Lore | Initial ledger built from catalog/, raw/pages/ and sources/ by tools/ledger_build.py. |\n')
tbl=['## Section counts (as of 2026-10-03)\n','| Section | Entries | VERIFIED | WIKI-ONLY | UNVERIFIED |','|---|---|---|---|---|']
tot=collections.Counter()
for k,v in COUNTS.items():
    if 'rows' in v: tbl.append(f"| {k} | {v['rows']} | - | - | - |"); continue
    tbl.append(f"| {k} | {sum(v.values())} | {v['VERIFIED']} | {v['WIKI-ONLY']} | {v['UNVERIFIED']} |"); tot.update(v)
tbl.append(f"| **Total (excluding conflict rows)** | {sum(tot.values())} | {tot['VERIFIED']} | {tot['WIKI-ONLY']} | {tot['UNVERIFIED']} |\n")
idx=out.index('## 1. Achievements\n')
out[idx:idx]=tbl
open(sys.argv[1] if len(sys.argv)>1 else ROOT+'/work/ledger-rebuild.md','w').write('\n'.join(out))
for k,v in COUNTS.items(): print(k,dict(v),sum(v.values()))
