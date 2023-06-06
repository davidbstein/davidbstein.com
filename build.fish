#!/usr/bin/env fish


set directory_to_watch _jekyll

while true
    inotifywait -r -e modify,create,delete $directory_to_watch
    echo "Directory has changed, running script..."

    echo "building site"

    cd _jekyll
    bundle exec jekyll build --destination ../docs
    cd ..


    echo "setting up 404"
    echo "---
permalink: /404.html
---" | cat - docs/404.html > _tmp; mv _tmp docs/404.html

     echo "setting up index"
     echo "---
permalink: /index.html
---" | cat - docs/index.html > _tmp; mv _tmp docs/index.html

     echo "setting CNAME"
     echo "davidbstein.com" > docs/CNAME
     echo "done"
end