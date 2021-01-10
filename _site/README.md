# davidbstein.com

It's where my homepage live.

## Build notes

I don't update this much and I keep forgetting how to build it.

### Dependencies

 - (`fish`)[https://fishshell.com/]
 - (`jekyll`)[https://jekyllrb.com/docs/installation/#requirements]
   - updating fish path is different than jekyll install instructions. 
     <br/> add `set -x GEM_HOME ~/.gems; set -x PATH ~/.gems/bin $PATH` to `~/.config/fish/config.fish`

### Building

 `fish build.fish`

> There's a good chance this fails because `can't find gem bundler (>= 0.a) with executable bundle`. Your ruby install is old. run `sudo gem update --system`

