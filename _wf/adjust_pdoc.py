#!/usr/bin/env python3
import os
from datetime import UTC
from datetime import datetime
from pathlib import Path

from lxml import etree
from markdown import markdown

cur = Path.cwd()
rootPath = cur.parent
docPath = os.getenv("cur", "docs")
docFile = Path(f"{cur}/{docPath}/enhanced_logging.html")

readme_md = Path(f"{cur}/README.md").read_text(encoding="utf-8")

# Render README.md -> HTML and wrap it in a <section> so it’s easy to style.
readme_html = markdown(
    readme_md,
    extensions=[
        "fenced_code",
        "tables",
        "toc",
        "codehilite",
    ],
    output_format="html5",
)

insert_html = f"""
<section id="readme" style="margin-top: 2rem;">
    <p style="opacity: 0.8; font-size: 0.95em;">
        Last updated: <span id="update_date"></span>
    </p>
    {readme_html}
</section>
<hr/><hr/>
"""

insert = etree.fromstring(insert_html, parser=etree.HTMLParser())
date = datetime.now(UTC).strftime("%a %b %d %Y, %H:%M:%S %Z")
insert.find('.//span[@id="update_date"]').text = date

contents = etree.fromstring(
    docFile.read_text(),
    parser=etree.HTMLParser(),
)
main = contents.find(".//main")
main.insert(0, insert)

with docFile.open(mode="w", encoding="utf-8") as file:
    file.write(etree.tostring(contents).decode())
    file.close()
