# Disclaimer

Both Opera GX Mods and documentation are still actively developed. 

# Quick start

[Mod_Template](Mod_Template) is created to give you a quick start into creating mods. It showcases all capabilities and is a convenient starting point to create your own mods. Load it in Opera GX, look around, modify things and have fun.

![Loaded Mod Template](images/loaded_mod_template.png)

# Anatomy of GX Mod

Each mod consists of

1. manifest.json - defines what's included in mod as well as name, author, version etc.
2. resources - sounds, images, videos, css, shaders etc. 

## manifest.json 

See [manifest.json](Mod_Template/manifest.json) from Mod_Template. It should be self explanatory. In case you make a mistake, Opera GX will show you an error when trying to load such a mod.

### Background music

Opera GX uses [vertical remixing](https://gamemaker.io/en/blog/compose-video-game-music) to achieve dynamic music in the browser. However it doesn't mean you need to provide multiple music files. If only one is provided it will work as well. In such a case you can do a little trick and list the same file more than once. This will result in an increased volume when users are active in the browser.

### Keyboard sounds

You can provide a single sound for a key or a list of sounds that will be played in provided order. You can keep keys empty which means that no sound will be played or remove key and in that case default sound will be played.

### Browser sounds

The same rules apply as in keyboard sounds.

### Wallpaper

Provide light and dark versions. Mods can't block users from switching between light and dark mode.

### Theme

Provide both light and dark versions. Mods can't block users from switching between light and dark mode.

### Shaders

More than one shader can be provided in a single mod. [Read more about shaders](shaders.md).

### Web modding

Those are basically CSS styles that can be applied to web pages. Multiple pages can be modified with a single mod. Opera GX exposes primary and secondary color if you want to make web pages follow UI colors (see [opera.css](Mod_Template/webmodding/opera.css))

# Best practice

Random order.

1. Limit size of resources.
2. Music and sounds should follow volume from Mod_Template otherwise it won't be a good experience for users.
3. Keep resources in dedicated subdirectories.
4. Use a 512x512 good looking image for the icon. 
