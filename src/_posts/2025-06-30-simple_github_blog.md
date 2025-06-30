---
layout: post
title:  How this blog works — simplifying github pages
date:   2025-06-30
author: David Stein
categories: [Tools]
tags: [coding, howto]
excerpt_separator: <!--more-->
---

Github Pages' default rendering pipeline is a little fiddly. To preview your site, you need to install ruby and Gems and Jekyll, which takes a while if—like me—you don't use those tools in your day-to-day workflows. I converted this blog to use a pipeline that's (mostly) backwards-compatible with the default Jekyll pipeline, but much easier to use.<!--more-->

# The problem

I felt like I'm always bug-fixing Ruby or Gems or Bundler or Jekyll for half an hour when I want to make a change my personal homepage or blog. And sometimes things changed in surprising ways. But switching to a new platform would require converting all my posts to use some other templating system. 

# My solution

The entire build script for this project is contained in a single python file, [build.py](https://github.com/davidbstein/davidbstein.com/blob/master/build.py){target="_blank"}. It uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/){target="_blank"} to manage dependancies and environments, meaning you can build your blog locally by running the command `uv run build.py` and it will give you a preview without making any changes to your system or installing any python packages globally. 

Installing `uv` is a one-line command on macOS, linux, and windows (and it's also available via package installers like `brew`, `apt`, or `pipx`).

## Setup

### Folder structure

tl:dr; fork [this repo](https://github.com/davidbstein/simple-blog){target="_blank"} and move on to the next step.

The folder structure is as follows:
```
.
├── build.py                   # builds the webpage
└── src/                 # contains HTML templates used to render the webpage.
    ├── _includes/             # contains templates for re-used blocks of HTML
    │   └── default.html       # REQUIRED - the default HTML format. Can be blank.
    ├── _layouts/        # contains layout information for converting markdown files to webpages
    │   ├── default.html       # REQUIRED - sets the default template to render pages. Must contain `{{content}}`
    │   ├── null.html          # OPTIONAL - if converting from Jekyll, creating this file will prevent a common class of liquid templating issues.
    │   ├── page.html          # OPTIONAL - sets a layout for a page
    │   ├── post_list.html     # OPTIONAL - sets the layout for a list of posts (e.g., a blog's table of contents)
    │   └── post.html          # OPTIONAL - sets the layout for a post (i.e., with a date, author, etc.)
    ├── _posts/          # Contains blog posts. The name of the post must start with a date with the format YYYY-MM-DD
    │   └── 1990-01-02-Example_Post.md 
    ├── _sass/
    │   └── main.scss    # OPTIONAL - contains any scss or sass formatting configuration files.
    ├── 404.html         # OPTIONAL - overrides default error pages.
    ├── assets/          # contains any static assets, like images
    │   └── images/
    ├── index.md         # the landing page
    └── favicon.ico      # including a favicon will set the logo for the page
```

### setting up a blog.

Set up the files. 

Go to `Settings > Pages > Source` and select "GitHub Actions"

Set up a custom domain, if you have one.

Go to `Actions` and confirm that "Compile and Deploy static content to Pages" is running. You may need to run it manually the first time.

Done.
