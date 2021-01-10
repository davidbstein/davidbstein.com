# davidbstein.com

It's where my homepage live.

## Build notes

I don't update this much and I keep forgetting how to build it.

### Dependencies

 - `ruby` (`gem`) - `brew install ruby` or `apt install ruby`
 - `bundler` - `gem install bundler`
 - `fish`

### Building

 `fish build.fish`

> There's a good chance this fails because `can't find gem bundler (>= 0.a) with executable bundle`. Your ruby install is old. run `sudo gem update --system`

