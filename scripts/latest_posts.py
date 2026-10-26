"""Write the 5 newest issues of The AI Engineer into README.md, skipping course pages."""
import re
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://theaiengineer.substack.com/feed"
SKIP = re.compile(r"/p/(hardware-and-inference|rag-and-search|the-ai-engineer-courses)")

req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = [i for i in root.findall("./channel/item") if not SKIP.search(i.findtext("link"))][:5]
lines = "\n".join(f"- [{i.findtext('title').strip()}]({i.findtext('link').strip()})" for i in items)

with open("README.md") as f:
    readme = f.read()
readme = re.sub(r"(<!-- BLOG-POST-LIST:START -->).*?(<!-- BLOG-POST-LIST:END -->)",
                lambda m: f"{m.group(1)}\n{lines}\n{m.group(2)}", readme, flags=re.S)
with open("README.md", "w") as f:
    f.write(readme)
