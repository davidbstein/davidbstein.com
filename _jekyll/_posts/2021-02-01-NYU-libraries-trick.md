---
layout: post
title:  "Proxying papers through NYU libraries"
date:   2021-02-01
author: David Stein
tags: [howto]
excerpt_separator: <!--more-->
---

<style>
.fakebutton {
  border: 1px solid #333;
  background: #ddd;
  display: inline-block;
  color: black;
  text-decoration: none;
  border-radius: 2px;
  padding: 0px 4px;
}
.fakebutton:hover {
  background: #ccc;
  cursor: move;
  cursor: -webkit-grab;
  cursor: -moz-grab;
  cursor: grab;
  text-decoration: none;
}
</style>

Quick post. Super useful. Only works if you have an NYU login.


This is a "bookmarklet". Drag it into your bookmarks bar on your browser. You can rename it. It'll still work.

<a class='fakebutton' href="javascript:location.href='http://proxy.library.nyu.edu/login?url='+location.href"> NYU proxy </a>


Click it when you it a paywall (e.g., on HeinOnline or an Elsevier journal or whatever), it will remove the paywall if NYU libraries has access.


If you aren't logged in to your NYU account, it will make you log in and then bring you page to the page. If NYU libraries doesn't have access, it will bring you to an error page.