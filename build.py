import feedparser
import time
from datetime import datetime

# 取得したいRDF(RSS)のURLリストをここに記述します
RSS_URLS = [
    "https://money-life.doorblog.jp/index.rdf",
        "https://toushichannel.net/index.rdf",
        "https://kasemato.net/index.rdf",
        "https://shikaku2ch.doorblog.jp/index.rdf",
        "http://blog.livedoor.jp/itsoku/index.rdf",
        "https://somanyjobs.doorblog.jp/index.rdf",
        # "https://www.fx2ch.net/feed",

        "https://itainews.com/index.rdf",
        "https://news4vip.livedoor.biz/index.rdf",
        "http://blog.livedoor.jp/kinisoku/index.rdf",
        "https://orusoku.com/index.rdf",
        "http://blog.livedoor.jp/goldennews/index.rdf",
        "http://burusoku-vip.com/index.rdf",
        "https://nwknews.jp/index.rdf",
        "https://imihu.net/index.rdf",
        "http://chaos2ch.com/index.rdf",
        "http://ryusoku.com/index.rdf",
        "https://gahalog.2chblog.jp/index.rdf",
        "http://kyousoku.net/index.rdf",
        "https://hattatu-matome.ldblog.jp/index.rdf",
        "https://alfalfalfa.com/index.rdf",
]

all_items = []

# 各RDFからデータを取得
for url in RSS_URLS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        # titleとlinkを取得
        title = entry.title if hasattr(entry, 'title') else 'No Title'
        link = entry.link if hasattr(entry, 'link') else '#'
        
        # dc:date等のパースされた日時を取得（ソート用）
        parsed_date = entry.get('published_parsed') or entry.get('updated_parsed')
        
        all_items.append({
            'title': title,
            'link': link,
            'date': parsed_date,
            'site_name': feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown Site'
        })

# 日付の新しい順にソート（日付がない場合は一番下に）
all_items.sort(
    key=lambda x: x['date'] if x['date'] else time.localtime(0),
    reverse=True
)

# HTMLの生成
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>アンテナページ</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .item { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        .site-name { font-size: 0.8em; color: #666; }
    </style>
</head>
<body>
    <h1>アンテナページ</h1>
    <p>最終更新: {update_time}</p>
    <div class="container">
"""

# 取得したアイテムをHTMLに埋め込む
for item in all_items:
    html_content += f"""
        <div class="item">
            <a href="{item['link']}" target="_blank" rel="noopener noreferrer">{item['title']}</a><br>
            <span class="site-name">{item['site_name']}</span>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# 現在時刻を取得してHTMLに埋め込む
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
html_content = html_content.format(update_time=current_time)

# index.htmlとして保存
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html successfully generated.")
