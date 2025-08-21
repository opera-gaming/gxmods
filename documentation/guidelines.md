# Guidelines

## General

1. Optimize resources to limit download size.
2. Keep audio files in mp3 format, joint stereo, variable bitrate 145-180kbps.

## Music

1. Provide at least one music track that is perfectly looped.
2. If possible, use [vertical remixing](mods.md#background-music) to achieve a dynamic music effect.
3. Follow volume of music from [Mod_Template](Mod_Template/music).

## Browser Sounds

1. Provide sounds for all categories.
2. If possible, have more than one sound for each type, varying pitch/volume, etc.
3. Be mindful of sounds that are played more frequently. Opening and closing tabs, clicks, and hovers will be heard often. Make sure it's an enjoyable experience.
4. Sounds need to be short and start immediately to feel responsive. Make sure there's no silence at the beginning.
5. Folow volume of browser sounds from [Mod_Template](Mod_Template/sound).

## Keyboard Sounds

1. Provide sounds for ENTER, BACKSPACE, SPACE, and other keys.
2. If possible, have more than one sound for each type, varying pitch/volume, etc.
3. Make sure that typing is enjoyable.
4. Sounds need to be short and start immediately to feel responsive. Make sure there's no silence at the beginning. It's important for keyboard sounds, as any delay will feel laggy. It's advised to use WAV format.
5. Folow volume of keyboard sounds from [Mod_Template](Mod_Template/keyboard).

## Shaders

1. Optimize your shaders to use as little GPU as possible.
2. If you create an animated shader, make sure to limit the framerate as much as possible to avoid useless GPU usage. For example, a clock that changes display every second doesn't need to run at 60fps.
3. Use as few uniforms as possible.
4. Don't use iMouse uniform unless you need it - it has performance implications.
5. Consider including a non-animated version of the shader to limit GPU usage (mods can include more than one shader).

## Theme

1. Provide light and dark versions. If a wallpaper is included, make sure it creates an enjoyable composition.
2. Note that too light or too dark colors are not available. It's advised to use the built-in color picker.

## Wallpaper

Follow [GX wallpapers guildelines](GXWallpaperGuidelines.pdf) that explain safe zones, composition and coloring. 

1. The resolution should be at least 1920x1080.
2. Keep images in JPG format to limit the size of the mod.
3. Provide light and dark versions.
4. Be mindful of content that is shown over the wallpaper. Ensure that it's not distracting. Move key objects to sides that are not going to be covered with content. Think about lower resolutions and different aspect ratios.
5. Pick color and shadow color (for light and dark themes) for elements displayed on the start page.
6. For animated wallpapers, please stick with a maximum 1920x1080 resolution; otherwise, it might be too resource-hungry. Keep them short and perfectly looped to keep mod size under control. Use VP9 video format if possible for best performance.
7. For video wallpapers, always provide the first frame.

## Icon

1. To keep it future ready, provide 512x512 PNG format.

## Credits

1. Credit authors of resources that you use and, if required, include the license.


_Guidelines ver 4_
