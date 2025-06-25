#!/usr/bin/env fish


set directory_to_watch "./src"

while true
    inotifywait -r -e modify,create,delete $directory_to_watch
    echo "Directory has changed, running script..."

    echo "building site"

    uv run build.py
end