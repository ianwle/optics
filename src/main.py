import feedparser, json, re
from tinydb import TinyDB, Query
from datetime import datetime
from time import mktime

form_424b4_url = "https://sec.report/form/424B4.rss"
form_424b5_url = "https://sec.report/form/424B5.rss"

form_424b4_entries = feedparser.parse(form_424b4_url)
form_424b5_entries = feedparser.parse(form_424b5_url)

re_number = re.compile("\d+")

db_424b4 = TinyDB("db_424b4.json")
db_424b5 = TinyDB("db_424b5.json")

def process_entries(db_obj, feed_entries, split_title=""):
    for entry in feed_entries.entries:
        id = re_number.findall(entry['id'])[0]
        title = entry['title'].split(split_title)[0].strip()
        url = entry['link']
        published_at = datetime.fromtimestamp(mktime(entry['published_parsed']))
        if not (db_obj.search(Query().url == url)):
            db_obj.insert({
                "id": id,
                "title": title,
                "url": url,
                "published_at": json.dumps(published_at, indent=4, sort_keys=4, default=str),
                "checked": False
            })
        
process_entries(db_424b4, form_424b4_entries, " - 424B4")
process_entries(db_424b5, form_424b5_entries, " - 424B5")

def investigate_entries(list, type):
    pass