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
# HTMLの生成（モダンなCSSを適用）
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>アンテナページ</title>
    <style>
        /* カラーパレットの定義 */
        :root {
            --bg-color: #f3f4f6;
            --text-color: #1f2937;
            --card-bg: #ffffff;
            --link-color: #2563eb;
            --link-hover: #1d4ed8;
            --meta-color: #6b7280;
            --border-color: #e5e7eb;
        }
        
        /* ダークモード対応 */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #111827;
                --text-color: #f9fafb;
                --card-bg: #1f2937;
                --link-color: #60a5fa;
                --link-hover: #93c5fd;
                --meta-color: #9ca3af;
                --border-color: #374151;
            }
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            max-width: 800px;
            margin: 0 auto;
            padding: 24px 16px;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        h1 {
            text-align: center;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            letter-spacing: -0.025em;
        }

        .update-time {
            text-align: center;
            color: var(--meta-color);
            font-size: 0.875rem;
            margin-bottom: 2rem;
        }

        .container {
            display: flex;
            flex-direction: column;
            gap: 16px; /* カード間の余白 */
        }

        /* カードデザイン */
        .item {
            background: var(--card-bg);
            padding: 16px 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        /* ホバー時のアニメーション */
        .item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.05);
            border-color: var(--link-color);
        }

        .item-title {
            color: var(--link-color);
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            line-height: 1.4;
        }

        .item-title:hover {
            color: var(--link-hover);
        }

        /* サイト名のバッジ風デザイン */
        .site-name {
            display: inline-block;
            background-color: var(--border-color);
            color: var(--text-color);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            align-self: flex-start;
        }
    </style>
</head>
<body>
    <h1>アンテナページ</h1>
    <div class="update-time">最終更新: {update_time}</div>
    <div class="container">
"""

# 取得したアイテムをHTMLに埋め込む
for item in all_items:
    html_content += f"""
        <div class="item">
            <a href="{item['link']}" class="item-title" target="_blank" rel="noopener noreferrer">{item['title']}</a>
            <span class="site-name">{item['site_name']}</span>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# 現在時刻を取得してHTMLに埋め込む（先ほど修正した部分）
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
html_content = html_content.replace("{update_time}", current_time)


# index.htmlとして保存
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html successfully generated.")
