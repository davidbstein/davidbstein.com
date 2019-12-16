cd _jekyll
bundle exec jekyll build --destination ../docs
cd ..

echo "---
permalink: /404.html
---" | cat - docs/404.html > _tmp; mv _tmp docs/404.html

echo "---
permalink: /index.html
---" | cat - docs/index.html > _tmp; mv _tmp docs/index.html
