# KeySmasher

A tool to help you play WoW (and probably some other MMORPGs too)  

<img src="_images/demo.gif" alt= "" width="480" height="270">

## Synopsys

This tool does a 'keysmashing' for you. You don't need to press
buttons rapidly anymore to deal good DPS. Now you can just hold a button, and 
this tool will press it every `n` ms.  
KeySmasher saves your hands and your keyboard and increases your DPS! For free!

# Installation and setup
For now only linux systems with X11 are supported.

## Dependencies:
* `python3`
* `xdotool`
* `xinput`
* `xmodmap`

### Arch
``` shell script
pacman -S xdotool xorg-xinput xorg-xmodmap python
```

## Installation
Install dependencies and then add `keysmasher` script to your PATH.

## Setup and run
1. Get your keyboard id
    * Run `xinput --list` and find your keyboard id (use `xinput test $id` to find the correct one)
2. Run script!
    * `keysmasher -d "delay in msecs" -i "keyboard id" -k "keys" "to" "smash"`

# License
All the code in this repository is released under the WTFPL license. Take a look at the [LICENSE](LICENSE) for more info.