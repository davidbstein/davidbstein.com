# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "feedgen",
#     "markdown-it-py[plugins]",
#     "libsass",
#     "python-liquid",
# ]
# ///
from feedgen.feed import FeedGenerator
from datetime import datetime
from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_plugin
from pathlib import Path
import os
import shutil
import sass
from xml.sax.saxutils import escape
import liquid
from liquid import Environment, FileSystemLoader
from datetime import datetime, timezone

md = MarkdownIt().use(attrs_plugin)
ROOT = Path("src")
LAYOUTS = ROOT / "_layouts"

BUILD_TARGET = Path("content")
SASS_DIR = ROOT / '_sass'

import shutil
shutil.rmtree(BUILD_TARGET)

def date_to_xmlschema(value):
  if isinstance(value, str):
    try:
      value = datetime.fromisoformat(value)
    except ValueError:
      value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
  try:
    if value.tzinfo is None:
      value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()
  except:
    return ''
def relative_url(path, context=None):
  if not context:
    return path
  baseurl = context.get("site", {}).get("baseurl", "/")
  baseurl = "/" + baseurl.strip("/")
  path = "/" + path.lstrip("/")
  return baseurl + path

def feed_meta_filter(_, context):
  site = context.get("site", {})
  title = site.get("title", "Site")
  baseurl = site.get("baseurl", "")
  url = site.get("url", "") + baseurl
  href = f"{url}/feed.xml".replace("//", "/")
  return f'<link type="application/atom+xml" rel="alternate" href="{href}" title="{title}">'

def xml_escape_filter(value):
  return escape(str(value), {"'": "&apos;"})  # Optional: escape apostrophes too

def absolute_url_filter(path, context=None):
  if not context:
    return path
  site = context.get("site", {})
  site_url = site.get("url", "").rstrip("/")
  baseurl = "/" + site.get("baseurl", "").strip("/")
  path = "/" + path.lstrip("/")
  return f"{site_url}{baseurl}{path}"

def split_metadata(content):
  metadata = {}
  if content.startswith("---\n"):
    _metadata_raw, *content_raw = [p.strip() for p in content.split("\n---\n") if p.strip()]
    for line in _metadata_raw.split("\n"):
      k, *v = line.split(":")
      val = ':'.join(v).strip()
      if k and val:
        metadata[k] = val
    content = "\n---\n".join(content_raw)
  return metadata, content
  
def compile_css(target):
  with open(target) as f:
    raw_content = f.read()
  metadata, content = split_metadata(raw_content)
  return sass.compile(
    string=content,
    include_paths=[str(SASS_DIR)]
  )
  
def render_html(metadata, content):
  liquid_env = Environment(
    loader=FileSystemLoader(ROOT / "_includes", ext=".html")
  )
  liquid_env.add_filter("absolute_url", absolute_url_filter)
  liquid_env.add_filter("date_to_xmlschema", date_to_xmlschema)
  liquid_env.add_filter("relative_url", relative_url)
  liquid_env.add_filter("feed_meta", lambda _, ctx=None: feed_meta_filter(_, ctx or {}))  
  liquid_env.add_filter("xml_escape", xml_escape_filter)
  liquid_env.get_template("header")
  
  original_get_template = liquid_env.get_template
  
  def debug_get_template(name, **kwargs):
    try:
      return original_get_template(name, **kwargs)
    except:
      import traceback
      traceback.print_exc()
      print(f"📄 Trying to load template: {name!r}, {kwargs}")
      display(liquid.context.RenderContext.__dict__)
      return original_get_template("default", **kwargs)
  
  liquid_env.get_template = debug_get_template

  if 'layout' not in metadata:
    return liquid_env.render(content)
  with open(LAYOUTS / f"{metadata['layout']}.html") as f:
    layout_metadata, template = split_metadata(f.read())
  rendered_content = liquid_env.render(
    template,
    **{
      'content': content,
      'page': metadata,
    }
  )
  if 'layout' in layout_metadata:
    return render_html(layout_metadata, rendered_content)
  else:
    return rendered_content

def gen_html_from_md(metadata, content):
  html = render_html(metadata, md.render(content))
  return metadata, html

def gen_html_from_md_file(root, subpath):
  path = root/subpath
  with open(path) as f:
    raw_content = f.read()
  metadata = {
    "permalink": str(subpath.parent / path.parts[-1].replace(".md", ".html"))
  }
  file_metadata, content = split_metadata(raw_content)
  metadata.update(file_metadata)
  return gen_html_from_md(metadata, content)
  

def crawl_path(path):
  for cur in path.iterdir():
    if cur.is_dir():
      yield from crawl_path(cur)
    else:
      yield cur

def build_static_content():
  for path in crawl_path(ROOT):
    try:
      ext = str(path).split(".")[-1]
      subpath = Path(*path.parts[len(ROOT.parts):])
      dst = BUILD_TARGET / subpath
      if ext == "md":
        metadata, html = gen_html_from_md_file(ROOT, subpath)
        link = metadata.get('permalink')
        if link and not link.startswith("_"):
          if link.startswith('/'):
            link = link[1:]
          if link.endswith('/'):
            link = link + 'index.html'
          link = Path(link)
          if '.' not in link.parts[-1]:
            link = Path(str(link) + '.html')
          dst = (BUILD_TARGET / link)
          print('    ', dst)
          os.makedirs(dst.parent, exist_ok=True)
          with open(dst, 'w') as f:
            f.write(html)
      elif subpath.parts[0].startswith("_"):
        # print("skip", subpath)
        pass
      elif ext == "scss":
        dst = Path(str(dst)[:-4]+"css")
        os.makedirs(dst.parent, exist_ok=True)
        with open(dst, 'w') as f:
          f.write(compile_css(path))
      elif ext in ("xml", "html", "htm"):
        with open(path) as f:
          raw_content = f.read()
        metadata, content = split_metadata(raw_content)
        os.makedirs(dst.parent, exist_ok=True)
        with open(dst, "w") as f:
          print(dst)
          f.write(render_html(metadata, content))
      else:
        os.makedirs(dst.parent, exist_ok=True)
        print(dst)
        shutil.copyfile(path, dst)
    except:
      import traceback
      traceback.print_exc()

def gen_posts():
  post_dir = ROOT / "_posts"
  post_list = []
  for fname in os.listdir(post_dir):
    with open(post_dir / fname) as f:
      raw_content = f.read()
    metadata, content = split_metadata(raw_content)
    sep = metadata.get("excerpt_separator", "<!--more-->")
    summary = content.split(sep)[0][:1000]
    metadata, html = gen_html_from_md(metadata, content)
    full_path = f'{fname.split(".")[0].replace("-", "/")}'
    dst = f'blog/{full_path}.html'
    print(dst)
    metadata['uri'] = dst
    metadata['content'] = html
    metadata['summary'] = summary
    metadata['tags'] = [tag for tag in metadata.get('tags', '[]')[1:-1].split(",") if tag]
    post_list.append(metadata)
  fg = FeedGenerator()
  fg.title("stein's blog")
  fg.link(href='https://stein.fyi/', rel='alternate')
  fg.description('random stuff posted by stein')
  fg.language('en')
  
  blog_home = ""
  for post in reversed(sorted(post_list, key=lambda e: e['uri'])):
    item = f'''
    <li>
      <div class="post-info">
        <div class="post-title">
          <a class="post-link" href="/{post.get('uri', "#")}">{post.get('title', '...')}</a>
        </div>
        <div class="post-meta">{post.get('date', 'YYYY-MM-DD')}</div>
      </div>
      <div class="post-exerpt">
        <p>{post.get("summary", "")}</p>
      </div>
      <div class="post-tags">
        <ul class="post-tag-list">          
          <li>{"</li>&nbsp;<li>".join(post.get("tags", []))}</li>
        </ul>
      </div>
    </li>
    '''
    blog_home += item
    dst = BUILD_TARGET / post['uri']
    print(dst)
    os.makedirs(dst.parent, exist_ok=True)
    with open(dst, "w") as f:
      f.write(post['content'])  
    entry = fg.add_entry()
    entry.title(post.get('title', 'untitled post'))
    entry.link(href=f'https://davidbstein.com/{post.get("uri", "blog")}')
    entry.description(post.get('summary', "(no description)"))
    dt = datetime.fromisoformat(post.get('date'))
    if dt.tzinfo is None:
      dt = dt.replace(tzinfo=timezone.utc)
    entry.pubDate(dt)
  dst = BUILD_TARGET / "blog" / "index.html"
  os.makedirs(dst.parent, exist_ok=True)
  with open(dst, "w") as f:
    print(dst)
    f.write(render_html({
      'layout': 'post_list',
      'title': 'blog',
    }, blog_home))
  dst = BUILD_TARGET / "feed.xml"
  os.makedirs(dst.parent, exist_ok=True)
  with open(dst, "w") as f:
    print(dst)
    f.write(fg.rss_str(pretty=True).decode('utf-8'))

build_static_content()
gen_posts()