##### Written by Gemini
# slight modification...

import os
from bs4 import BeautifulSoup

site_dir = "site"  # Change to your Zensical output directory if different
web_app_url = "https://script.google.com/a/macros/asdrp.org/s/AKfycbzQia5pYurgSWFVuKUSYlSWNTUdWpt28VS2fk0JkSI/dev/"

for root, dirs, files in os.walk(site_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            # Inject <base> tag into <head> to fix relative path resolution in iframes
            if soup.head:
                base_tag = soup.new_tag("base", href=web_app_url)
                soup.head.insert(0, base_tag)

            # Inline CSS files
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href")
                if href and not href.startswith("http"):
                    css_path = os.path.normpath(os.path.join(root, href))
                    if os.path.exists(css_path):
                        with open(css_path, "r", encoding="utf-8") as css_f:
                            style_tag = soup.new_tag("style")
                            style_tag.string = css_f.read()
                            link.replace_with(style_tag)

            # Inline JS files
            for script in soup.find_all("script", src=True):
                src = script.get("src")
                if src and not src.startswith("http"):
                    js_path = os.path.normpath(os.path.join(root, src))
                    if os.path.exists(js_path):
                        with open(js_path, "r", encoding="utf-8") as js_f:
                            script_tag = soup.new_tag("script")
                            script_tag.string = js_f.read()
                            script.clear()
                            script.replace_with(script_tag)

            # # those fucking dots
            # for link in soup.find_all("a"):
            #     print(link)
            #     href = str(link.get("href")).replace("./","").replace(".","")


            with open(filepath, "w", encoding="utf-8") as f:
                f.write(str(soup))

print("Successfully inlined all local assets into HTML files.")
