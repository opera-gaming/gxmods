# Disclaimer

This feature is highly experimental. Expect things to break or not to work as expected at any times. This feature is still under development. There are known bugs and certain limitations we're (or are not)aware of.

# Overview

*If you're writing shaders to be used by the Opera GX Mod you can jump directly to the next paragraph as Mods engine will apply the shaders for you.*

## Basic filter

Opera’s GPU shader CSS filters (we'll call it `shaders` or `shader filters` for simplicity) lets you apply a regular CSS filter using your own GPU shader code. From a web dev perspective applying a shader filter is as easy as adding

    filter: -opera-shader(url(source_url));

to the element's style. The `source_url` must point to the shader source written in SkSL (you'll find more on SkSL in the next chapter). It can be a data url as well.

## Passing custom args

> This feature is planned to be released in Opera GX v.95.x and later.

An extra args may be passed from the CSS straight to the shader. Use `-opera-args()` CSS function to pass any number of extra arguments to the shader. In shader, declare `iArgs[]` uniform with same exact size as the number of `-opera-args()` parameters. For example:

In stylesheet:

    filter: -opera-shader(url(source_url) -opera-args(10 20 30 40));

In shader:

    uniform float iArgs[4];

> You are allowed to use CSS variables and other functions like `calc()` as the arguments to the `-opera-args()` function.

## Animated filters

> This feature is planned to be released in Opera GX v.95.x and later.

The parameters of `-opera-args()` can be used in CSS animations. The rendering engine will interpolate actual values according to the animation definition and shader will receive interpolated values for each drawn frame. For example:

    div.filter {
        animation: sample 5s infinite;
        animation-timing-function: linear;
    }

    @keyframes sample {
        0% {
            filter: -opera-shader(url(source.sksl) -opera-args(0 0 0 1));
        }

        100% {
            filter: -opera-shader(url(source.sksl) -opera-args(1 0 0 1));
        }
  }

In the above example shader can use `iArgs[4]` array uniform where iArgs[0] will be somewhere between 0 and 1 (depending on animation timeline, etc) and the remaining values will remain same for all drawn frames.

# Writing Shaders

There are many ways of writing gpu shaders. Since our shaders are run in the browser ecosystem they must follow certain rules in order to have them injected into the browser rendering pipeline.

## Image Filtering in a Nutshell

CSS filters are regular image filters. Whenever a HTML element has a `filter` property set, the rendering engine will:
- render its contents into the separate texture
- filter it by running fragment shader on it 
- composite the filtered image into the final web page image

The filter CSS property creates a kind of filtering pipeline. Defining more than one filter will cause the image to be filtered in order of the filters appearance where output from the former filters becomes the input to the latter one.

## SkSL

Since our filters run within browser ecosystem we must follow certain rules enforced by the browser rendering engine. Browser rendering engine uses Skia as a rendering backend and therefore shaders needs to be written using SkSL (Skia Shading Language) in order to have them run in the Skia rendering pipeline. You can reed more about SkSL here: https://skia.org/docs/user/sksl but in short SkSL is kind of a subset of GLSL. There are some differences but most of the GLSL shaders can be easily rewritten into the SkSL.

## Opera Shaders Environment

In pure GLSL you are allowed to define your own uniforms (global variables) that can be accessed by the shader program. Uniforms acts like a parameters passed from the user of the shader to the shader program. In our case there is a set of uniforms defined by the engine itself and you are allowed to use them in your shader filters. You are not allowed to declare any other uniforms - this will throw a runtime error (a detailed error message is sent to the browser's dev tools console) and your shader won't be run.

> Please declare *only* those uniforms that you actually use in your shader. Some uniforms (like `iMouse`) require additional handling that costs extra CPU processing power.

Current version of shaders engine bind following uniforms:

| Uniform Name | Type | Description |
|---|---|---|
| `iChunk` | shader | `iChunk` is an input texture. You can sample pixels from `iChunk` using standard SkSL shader eval() method. In our solution the texture origin (0,0) is put in the top-left corner.  | 
| `iChunkSize` | float2 | Size of the input texture. Shaders are allowed so sample pixels within area defined by the iChunkSize. Sampling pixels outside that are will produce undefined behavior. Keep in mind that `iChunkSize` may not reflect the exact size of the filtered HTML element. In some cases it may be smaller than the filtered content (that is, it'll be a subset of the entire content) and in some cases (overflowing, non-clipped content) it may be bigger than the content as it is being defined by the filtered HTML element bounding box. In the latter case extra caution should be taken when processing pixels that are fully transparent as they may represent part of the texture with no content. |
| `iChunkOffset` | float2 | A chunk offset relative to the content origin. As mentioned above, the `iChunkSize` may be actually smaller than the filtered content itself and in fact the `iChunk` origin may not be aligned with the filtered content origin. The `iChunkOffset` tells what is the `iChunk` origin relative to filtered content. |
| `iContentSize` | float2 | The size of the filtered content passed as [`width`, `height`], defined by the filtered element bounding box. When used together with `iChunkOffset` and `iChunkSize` it can be used to determine which part of the source image is being filtered. |
|`iMouse`|float2| Mouse position over filtered element. **IMPORTANT**: Mouse position is relative to entire content image rect and not to currently processed chunk. |
|`iTick`| float | A monotonically increasing timer value with no special meaning.|
|`iDate`| float4 | Current date passed as [`year`, `month`, `day`, `seconds since midnight`]|
|`iRootViewColor`| float4 | An [`r`, `g`, `b`, `a`] value reflecting color of the viewport. Valid only when filters are applied to the `:root` element.|
|`iArgs`|float[]|A variable length array used to carry the args defined in the CSS by the `-opera-args()` function. See [Passing custom args](#passing-custom-args) for more details.|

### Deprecated uniforms

Following uniforms are deprecated and will be removed as soon as with version 95.x of Opera GX.

| Uniform Name | Type | Description |
|---|---|---|
| `iFrame` | float | A value between 0 and 100 describing current animation frame. This is used by the Opera Mods engine for shaders that are willing to animate. You can setup animation by adding the `animation` entry to the Mod's manifest and `iFrame` will be calculated for each animation frame accordingly to the animation parameters. This is similar to how [animated shaders](#animated-filters) work together with `-opera-args()` function.| 

## Example Shader

```
// Currently processed chunk (subregion) of the source image.
uniform shader iChunk;

// The dimensions of the |iChunk| texture.
uniform float2 iChunkSize;

// Offset of the chunk, relative to the image origin.
uniform float2 iChunkOffset;

// The total size of the source image. This may be bigger than the actual
// chunk size.
uniform float2 iContentSize;

// Mouse position. BE CAREFUL. The mouse position coords are in content image
// coordinates space. Depending on what you need, either:
// - compare them against iContentSize if building an effect that depends on
//   the mouse position relative to entire content
// - convert them to chunk coordinates if you want to change the chunk pixels
//   based on mouse position over the chunk. Keep in mind that mouse position
//   may be outside the chunk so you need to ignore it in this case!
uniform float2 iMouse;

float EPSILON = 0.3999999;

half4 RED = half4(1, 0, 0, 1);
half4 BLUE = half4(0, 0, 1, 1);
half4 GREEN = half4(0, 1, 0, 1);
half4 MAGENTA = half4(1, 0, 1, 1);
half4 YELLOW = half4(1, 1, 0, 1);
half4 GRAY = half4(0.2, 0.2, 0.2, 1);

bool nearly_equal(float a, float b) {
  return abs(a - b) < EPSILON;
}

float2 align(float2 xy) {
  return xy - 0.5;
}

float2 content_to_chunk(float2 xy) {
  return xy - iChunkOffset;
}

bool within_chunk_bounds(float2 xy) {
  return xy.x >= 0 && xy.x < iChunkSize.x && xy.y >= 0 && xy.y < iChunkSize.y;
}

// This example shader:
//  - draws sharp single line border around the filtered content
//  - draws colored circle under the mouse - the circle is yellow when the
//    mouse position is in the left half of the entire content. It turns orange
//    when mouse crosses the image center to th other half.
//
// You can observe how to:
//  - (1) move the pixel center from the default (0.5, 0.5) to whole number pixel offsets (0, 0)
//    in order to make it suitable for comparison with texture size and offset
//  - (2) offset the incoming xy position so that it reassembles pixel position relative
//    to source image top left corner (instead of being relative to the chunk start
//    which is always (0, 0))
//  - (3) because floats should not be compared directly use proper float comparison - consider
//    two floats equal if they are close enough to each other - you can adjust the |EPSILON|
//    to make the comparison more/less accurate
//  - (4) compare absolute mouse position to the content size
//  - (5) convert absolute mouse position to a mouse position relative to the chunk
//  - (6) ensure that the relative mouse position obtained in step (5) is valid
half4 main(float2 xy) {
  // (1) align pixel center
  float2 aligned_xy = align(xy);

  // (2) offset the |xy| so it can be compared with |iContentSize|
  float2 content_xy = aligned_xy + iChunkOffset;

  // (3) safely compare floats - here - check if we're drawing left border
  if (nearly_equal(content_xy.x, 0)) {
    // we're drawing left border
    return RED;
  }

  if (nearly_equal(content_xy.x, iContentSize.x - 1)) {
    // we're drawing right border
    return BLUE;
  }

  if (nearly_equal(content_xy.y, 0)) {
    // we're drawing top border
    return GREEN;
  }

  if (nearly_equal(content_xy.y, iContentSize.y - 1)) {
    // we're drawing bottom border
    return MAGENTA;
  }

  half4 color = YELLOW;
  // (4) - compare mouse position (absolute) to the content size - this is safe
  // as both values are in that same coordinate space
  if (iMouse.x > iContentSize.x / 2) {
    color = GRAY;
  }

  // (5) we want to draw circle under the mouse cursor therefore we need to
  // convert absolute mouse position into the relative position inside this particular
  // chunk.
  float2 mouse_in_chunk = content_to_chunk(iMouse);

  // (6) check whether mouse position is inside chunk - do not operate on chunk
  // pixels when the mouse is outside the chunk.
  if (within_chunk_bounds(mouse_in_chunk)) {
    float2 tmp = xy - mouse_in_chunk;
    if (pow(tmp.x, float(2)) + pow(tmp.y, float(2)) < 100) {
      return color;
    }
  }

  return iChunk.eval(xy);
}
```