"""Write the 5 newest issues of The AI Engineer into README.md, skipping course pages."""
import re
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://theaiengineer.substack.com/feed"
SKIP = re.compile(r"/p/(hardware-and-inference|rag-and-search|the-ai-engineer-courses)")

import subprocess
xml = subprocess.run(["curl", "-sfL", "--compressed", "-A",
                      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
                      "-H", "Accept: application/rss+xml,application/xml;q=0.9,*/*;q=0.8", FEED],
                     capture_output=True, check=True).stdout
root = ET.fromstring(xml)
items = [i for i in root.findall("./channel/item") if not SKIP.search(i.findtext("link"))][:5]
lines = "\n".join(f"- [{i.findtext('title').strip()}]({i.findtext('link').strip()})" for i in items)

with open("README.md") as f:
    readme = f.read()
readme = re.sub(r"(<!-- BLOG-POST-LIST:START -->).*?(<!-- BLOG-POST-LIST:END -->)",
                lambda m: f"{m.group(1)}\n{lines}\n{m.group(2)}", readme, flags=re.S)
with open("README.md", "w") as f:
    f.write(readme)
