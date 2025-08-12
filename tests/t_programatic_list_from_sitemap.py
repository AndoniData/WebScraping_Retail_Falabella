import xml.etree.ElementTree as ET
import pathlib as path

sitemap_path = path.Path('data/collection_xml/collections_cl_FA_COM-0.xml')
config_urls_path = path.Path('config/url_base.json')

with open(sitemap_path, 'r', encoding='utf-8') as f:
    tree = ET.parse(f)
    root = tree.getroot()

# The namespace in your XML
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Extract all <loc> elements
urls = [loc.text for loc in root.findall('.//ns:loc', ns)]

# Extract name of the collection
names = [loc.text.split('/')[-1] for loc in root.findall('.//ns:loc', ns)]


with open(config_urls_path, 'w', encoding='utf-8') as f:
    f.write('{\n    "urls": {\n')
    for url, name in zip(urls, names):
        f.write(f'        "{name}": "{url}",\n')
    f.write('    }\n}\n')
