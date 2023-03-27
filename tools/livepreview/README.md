# Intro

Tool to preview GX Shaders. Comes with live reloading, useful when working with GX Shaders.


# Usage

Launch in directory that contains GX Shaders (expected in files with .txt extension). 

	$ <path-to-script>/livepreview.py <directory>

Example usage:

	$ cd livepreview
	$ ./livepreview.py

This will produce output similar to this:

	Server path:       /Users/dev/gxmods/tools/livepreview
	Preview template:  /Users/dev/gxmods/tools/livepreview/preview.html
	Static template:   /Users/dev/gxmods/tools/livepreview/shader-static.js
	Animated template: /Users/dev/gxmods/tools/livepreview/shader-animated.js
	Serving from:      /Users/dev/gxmods/tools/livepreview
	Local server at:   http://127.0.0.1:8888

	http://127.0.0.1:8888/matrix.txt.static
	http://127.0.0.1:8888/matrix.txt.animated
	http://127.0.0.1:8888/wave.txt.static
	http://127.0.0.1:8888/wave.txt.animated	

Open Opera GX and navigate to the specified URLs. Each shader is displayed in both static and animated formats. Shaders are applied to the offline version of [opera.com](https://www.opera.com). When a file is modified, the preview updates automatically. For an efficient workflow, keep the GX Shader code editor, live preview in Opera GX, and Developer Tools open concurrently. If any issues arise with the code, the shader will disappear from the preview, and a list of errors will appear in the Console. This setup is particularly useful when making adjustments to the code and requiring immediate feedback. To see the results of a change, simply modify the code, save the file, and observe the updated output in Opera GX. 

![preview](livepreview.gif)

Optional `<directory>` specifies directory with scripts. If missing it will assume serving from directory where `livepreview.py` is located. If you put `livepreview.py` in `$PATH`, you can serve scripts from current directory running:

	$ livepreview.py .


# How to use another page for preview?

Replace contents of `preview.html`. Included offlined [opera.com](https://www.opera.com) was created this way:

	$ wget -k -K  -E -r -l 10 -p -N -F --restrict-file-names=windows -nH https://www.opera.com

[Read more](https://gist.github.com/azizur/ffe8ee6a0a2bb418e5cc8ff101fad91a) about parameters and what they mean. If at some point it gets removed here's the explanation again:

	-k : convert links to relative
	-K : keep an original versions of files without the conversions made by wget
	-E : rename html files to .html (if they don’t already have an htm(l) extension)
	-r : recursive… of course we want to make a recursive copy
	-l 10 : the maximum level of recursion. if you have a really big website you may need to put a higher number, but 10 levels should be enough.
	-p : download all necessary files for each page (css, js, images)
	-N : Turn on time-stamping.
	-F : When input is read from a file, force it to be treated as an HTML file.
	-nH : By default, wget put files in a directory named after the site’s hostname. This will disabled creating of those hostname directories and put everything in the current directory.
	–restrict-file-names=windows : may be useful if you want to copy the files to a Windows PC.


# Notes

1. Tested on macOS only