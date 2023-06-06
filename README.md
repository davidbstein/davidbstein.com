# davidbstein.com

It's where my homepage live.

## Build notes

I don't update this much and I keep forgetting how to build it or find myself on a new OS

### Dependencies

 - (`fish`)[https://fishshell.com/]
 - (`jekyll`)[https://jekyllrb.com/docs/installation/#requirements]
   - _ubuntu notes_
     - ruby needs dev tools too: `sudo apt install ruby ruby-dev ruby-all-dev`
     - updating fish path is different than jekyll install instructions. 
       <br/> add `set -x GEM_HOME ~/.gems; set -x PATH ~/.gems/bin $PATH` to `~/.config/fish/config.fish`
   - _mac notes_
     - ruby needs dev tools too: `sudo apt install ruby ruby-dev ruby-all-dev`
     - updating fish path is different than jekyll install instructions. 
       <br/> add `set -x GEM_HOME ~/.gems; set -x PATH ~/.gems/bin $PATH` to `~/.config/fish/config.fish`
       
> you might have `Gemfile.lock` version mismatches in `_jekyll/Gemfile.lock`. Try deleting the lock, if everything works then just push the new lock and don't bother going on a vision question about dependency versions

### Building

  __first time__: `cd _jekyll; bundle install`

 `fish build.fish`


