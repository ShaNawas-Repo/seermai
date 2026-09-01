#!/usr/bin/env python3
import json

with open('/home/workdir/artifacts/seermai_full.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))

genres = sorted(set(b.get('genre', '') for b in books if b.get('genre')))
categories = sorted(set(b.get('category', '') for b in books if b.get('category')))
subjects = sorted(set(b.get('subject', '') for b in books if b.get('subject')))

genre_opts = '\n'.join(f'          <option value="{esc(g)}">{esc(g)}</option>' for g in genres)
cat_opts = '\n'.join(f'          <option value="{esc(c)}">{esc(c)}</option>' for c in categories)
subj_opts = '\n'.join(f'          <option value="{esc(s)}">{esc(s)}</option>' for s in subjects)

rows = []
for b in books:
    search_blob = ' '.join([
        b['title'], b.get('subtitle', ''), b['author'], b.get('translator', ''),
        b.get('translit', ''), b.get('isbn', ''), b.get('source', ''), b.get('language', ''),
        b.get('binding', ''), b.get('size', ''), str(b.get('year', '')), str(b.get('price', '')),
        b.get('genre', ''), b.get('category', ''), b.get('subject', '')
    ]).lower()

    author_display = esc(b['author'])
    if b.get('translator'):
        author_display += f'<br><span class="meta">தமிழில்: {esc(b["translator"])}</span>'

    subtitle_html = f'<div class="subtitle">{esc(b["subtitle"])}</div>' if b.get('subtitle') else ''
    translit_html = f'<div class="translit">{esc(b["translit"])}</div>' if b.get('translit') else ''
    lang_badge = (
        f'<span class="badge lang-{esc(b.get("language", ""))}">{esc(b.get("language", ""))}</span>'
        if b.get('language') else ''
    )

    genre_html = f'<span class="badge genre">{esc(b["genre"])}</span>' if b.get('genre') else '—'
    cat_html = f'<span class="badge category">{esc(b["category"])}</span>' if b.get('category') else '—'
    subj_html = f'<span class="badge subject">{esc(b["subject"])}</span>' if b.get('subject') else '—'

    img = b.get('image') or ''
    if img:
        cover = (
            f'<img class="cover" src="{esc(img)}" alt="" loading="lazy" '
            f'referrerpolicy="no-referrer" '
            f"onerror=\"this.replaceWith(Object.assign(document.createElement('div'),{{className:'cover-ph'}}))\">"
        )
    else:
        cover = '<div class="cover-ph"></div>'

    extra = []
    if b.get('isbn'):
        extra.append(f'ISBN: {esc(b["isbn"])}')
    if b.get('source'):
        extra.append(f'Source: {esc(b["source"])}')
    if b.get('size'):
        extra.append(f'Size: {esc(b["size"])}')
    if b.get('binding'):
        extra.append(esc(b['binding']))
    if b.get('edition') and b['edition'] > 1:
        extra.append(f'Ed. {b["edition"]}')
    extra_html = ' · '.join(extra)

    rows.append(
        f'''          <tr data-search="{esc(search_blob)}"
              data-serial="{b['serial']}"
              data-title="{esc(b['title'].lower())}"
              data-price="{b['price']}"
              data-year="{b['year']}"
              data-pages="{b['pages']}"
              data-author="{esc(b['author'].lower())}"
              data-language="{esc(b.get('language', ''))}"
              data-binding="{esc(b.get('binding', ''))}"
              data-size="{esc(b.get('size', ''))}"
              data-genre="{esc(b.get('genre', ''))}"
              data-category="{esc(b.get('category', ''))}"
              data-subject="{esc(b.get('subject', ''))}">
            <td class="num">{b['serial']}</td>
            <td class="cover-cell">{cover}</td>
            <td>
              <div class="title-main">{esc(b['title'])}</div>
              {subtitle_html}
              {translit_html}
              <div style="margin-top:0.2rem">{lang_badge}</div>
            </td>
            <td class="author-line">{author_display}</td>
            <td class="price">₹{b['price']}</td>
            <td class="tag-cell">{genre_html}</td>
            <td class="tag-cell">{cat_html}</td>
            <td class="tag-cell">{subj_html}</td>
            <td class="pages hide-md">{b['pages'] or '—'}</td>
            <td class="year hide-md">{b['year'] or '—'}</td>
            <td class="hide-md">
              <details class="extra">
                <summary>More</summary>
                {extra_html}
              </details>
            </td>
          </tr>
'''
    )

rows_html = '\n'.join(rows)

html = f'''<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>சீர்மை நூல் பட்டியல் | Seermai Complete Catalogue</title>
  <style>
    :root {{
      --primary: #8B6914;
      --primary-dark: #5c4508;
      --primary-light: #c9a227;
      --bg: #f7f3eb;
      --card: #ffffff;
      --text: #1f1f1f;
      --muted: #5a5a5a;
      --border: #e0d6c4;
      --hover: #fdf6e3;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Segoe UI", "Noto Sans Tamil", "Latha", "Noto Sans", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
      min-height: 100vh;
    }}
    header {{
      background: linear-gradient(135deg, #6B4F0A 0%, #8B6914 50%, #a67c00 100%);
      color: white;
      padding: 1.4rem 1rem 1.2rem;
      text-align: center;
      box-shadow: 0 3px 14px rgba(0,0,0,0.18);
    }}
    header h1 {{ font-size: 1.75rem; font-weight: 700; }}
    header p {{ opacity: 0.92; font-size: 0.92rem; margin-top: 0.25rem; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 1.2rem 1rem 3rem; }}

    .controls {{
      background: var(--card);
      border-radius: 14px;
      padding: 1rem 1.1rem;
      margin-bottom: 1.1rem;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      border: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
    }}
    .search-row {{
      display: flex;
      gap: 0.7rem;
      flex-wrap: wrap;
      align-items: center;
      margin-bottom: 0.75rem;
    }}
    #search {{
      flex: 1;
      min-width: 240px;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      border: 2px solid var(--border);
      border-radius: 10px;
      outline: none;
      transition: border-color .2s, box-shadow .2s;
    }}
    #search:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(139,105,20,0.18);
    }}
    .stats {{
      font-size: 0.9rem;
      color: var(--muted);
      white-space: nowrap;
    }}
    .stats strong {{ color: var(--primary-dark); font-size: 1.05rem; }}

    .filter-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem 0.7rem;
      align-items: center;
    }}
    .filter-row label {{
      font-size: 0.8rem;
      color: var(--muted);
      font-weight: 600;
    }}
    select {{
      padding: 0.4rem 0.6rem;
      border: 1.5px solid var(--border);
      border-radius: 8px;
      background: white;
      font-size: 0.85rem;
      cursor: pointer;
      max-width: 160px;
    }}
    select:focus {{ outline: 2px solid var(--primary-light); }}

    .table-wrap {{
      background: var(--card);
      border-radius: 14px;
      overflow-x: auto;
      box-shadow: 0 2px 16px rgba(0,0,0,0.06);
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      min-width: 1100px;
    }}
    thead {{
      background: var(--primary);
      color: white;
    }}
    th {{
      padding: 0.7rem 0.55rem;
      text-align: left;
      font-weight: 600;
      font-size: 0.8rem;
      white-space: nowrap;
    }}
    th.num, td.num {{ text-align: center; width: 38px; }}
    th.price, td.price {{ text-align: right; white-space: nowrap; font-weight: 700; color: var(--primary-dark); }}
    th.pages, td.pages {{ text-align: center; width: 50px; }}
    th.year, td.year {{ text-align: center; width: 50px; }}
    td.cover-cell {{ width: 56px; padding: 0.5rem; }}
    img.cover {{
      width: 48px;
      height: 68px;
      object-fit: cover;
      border-radius: 4px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.15);
      background: #eee;
      display: block;
    }}
    .cover-ph {{
      width: 48px;
      height: 68px;
      border-radius: 4px;
      background: #e8e0d0;
    }}

    td {{
      padding: 0.65rem 0.55rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    tbody tr {{ transition: background .12s; }}
    tbody tr:hover {{ background: var(--hover); }}
    tbody tr.hidden {{ display: none; }}

    .title-main {{ font-weight: 650; color: var(--text); margin-bottom: 0.12rem; }}
    .subtitle {{ font-size: 0.8rem; color: var(--muted); font-style: italic; margin-bottom: 0.15rem; }}
    .meta {{ font-size: 0.78rem; color: var(--muted); }}
    .author-line {{ font-size: 0.84rem; color: #3a3a3a; }}
    .translit {{ font-size: 0.76rem; color: #777; }}
    .tag-cell {{ font-size: 0.78rem; }}
    .badge {{
      display: inline-block;
      font-size: 0.68rem;
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      background: #f0e6d0;
      color: var(--primary-dark);
      margin: 0.1rem 0.15rem 0.1rem 0;
      font-weight: 600;
      white-space: nowrap;
    }}
    .badge.lang-Tamil {{ background: #e8f5e9; color: #2e7d32; }}
    .badge.lang-Arabic {{ background: #e3f2fd; color: #1565c0; }}
    .badge.lang-English {{ background: #fce4ec; color: #c2185b; }}
    .badge.lang-Urdu {{ background: #fff3e0; color: #e65100; }}
    .badge.lang-Malayalam {{ background: #f3e5f5; color: #7b1fa2; }}
    .badge.genre {{ background: #e8eaf6; color: #3949ab; }}
    .badge.category {{ background: #e0f2f1; color: #00695c; }}
    .badge.subject {{ background: #fbe9e7; color: #bf360c; }}

    .group-header {{
      background: #efe6d4 !important;
      font-weight: 700;
      font-size: 0.92rem;
      color: var(--primary-dark);
    }}
    .group-header td {{ border-bottom: 2px solid var(--primary-light); padding: 0.6rem 0.8rem !important; }}

    .no-results {{
      text-align: center;
      padding: 2.5rem 1rem;
      color: var(--muted);
      display: none;
    }}
    footer {{
      text-align: center;
      padding: 1.4rem 1rem;
      color: var(--muted);
      font-size: 0.82rem;
    }}
    footer a {{ color: var(--primary); text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}

    details.extra {{
      margin-top: 0.2rem;
      font-size: 0.76rem;
      color: var(--muted);
    }}
    details.extra summary {{
      cursor: pointer;
      color: var(--primary);
      font-weight: 500;
    }}

    @media (max-width: 1000px) {{
      .hide-md {{ display: none; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>சீர்மை நூல் பட்டியல்</h1>
    <p>Seermai Complete Catalogue — 164 Titles · Search · Sort · Group · Genre / Category / Subject</p>
  </header>

  <div class="container">
    <div class="controls">
      <div class="search-row">
        <input type="search" id="search" placeholder="தேடுங்கள்: தலைப்பு, ஆசிரியர், Genre, Category, Subject, ISBN, transliteration..." autocomplete="off">
        <div class="stats"><strong id="count">164</strong> / 164 நூல்கள்</div>
      </div>
      <div class="filter-row">
        <label>Sort</label>
        <select id="sortBy">
          <option value="serial">Serial #</option>
          <option value="title">Title (A→Z)</option>
          <option value="title-desc">Title (Z→A)</option>
          <option value="price">Price ↑</option>
          <option value="price-desc">Price ↓</option>
          <option value="year">Year ↑</option>
          <option value="year-desc" selected>Year ↓</option>
          <option value="pages">Pages ↑</option>
          <option value="pages-desc">Pages ↓</option>
          <option value="author">Author</option>
          <option value="genre">Genre</option>
          <option value="category">Category</option>
          <option value="subject">Subject</option>
        </select>

        <label>Group</label>
        <select id="groupBy">
          <option value="none" selected>None</option>
          <option value="year">Year</option>
          <option value="language">Language</option>
          <option value="genre">Genre</option>
          <option value="category">Category</option>
          <option value="subject">Subject</option>
          <option value="binding">Binding</option>
          <option value="size">Size</option>
          <option value="author">Author</option>
        </select>

        <label>Language</label>
        <select id="filterLang">
          <option value="">All</option>
          <option value="Tamil">Tamil</option>
          <option value="Arabic">Arabic</option>
          <option value="English">English</option>
          <option value="Urdu">Urdu</option>
          <option value="Malayalam">Malayalam</option>
        </select>

        <label>Genre</label>
        <select id="filterGenre">
          <option value="">All</option>
{genre_opts}
        </select>

        <label>Category</label>
        <select id="filterCategory">
          <option value="">All</option>
{cat_opts}
        </select>

        <label>Subject</label>
        <select id="filterSubject">
          <option value="">All</option>
{subj_opts}
        </select>

        <label>Binding</label>
        <select id="filterBinding">
          <option value="">All</option>
          <option value="Paperback">Paperback</option>
          <option value="Hardbound">Hardbound</option>
        </select>

        <label>Size</label>
        <select id="filterSize">
          <option value="">All</option>
          <option value="Crown">Crown</option>
          <option value="Demy">Demy</option>
          <option value="Royal">Royal</option>
        </select>
      </div>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th class="num">#</th>
            <th></th>
            <th>புத்தகம் / Title</th>
            <th>ஆசிரியர் / Author</th>
            <th class="price">விலை</th>
            <th>Genre</th>
            <th>Category</th>
            <th>Subject</th>
            <th class="pages hide-md">பக்கம்</th>
            <th class="year hide-md">ஆண்டு</th>
            <th class="hide-md">Details</th>
          </tr>
        </thead>
        <tbody id="book-list">
'''

# The above incorrectly mixed - rewrite more carefully without duplication
# Actually the f-string already started with header - I need only one header.
# Re-do cleanly in a simpler way.

raise SystemExit('rebuild cleanly')
PYEOF