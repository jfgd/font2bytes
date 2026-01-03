# font2bytes

Python program to create new fonts for e-Paper / e-Ink
displays. Generate C font files for e-Paper from TTF files.


## Acknowledgments

Forked from [TheHeXstyle's font2byte](https://github.com/theHEXstyle/font2bytes).

## Rational

I am super happy of my e-ink display from Waveshare, but their library only offers basic fonts types, and only 5 fonts sizes (font8, font12, font16, font20 and font24). This is unfortunately very limiting :(

This python script is inspired by the waveshare blogpost [this](https://wavesharejfs.blogspot.com/2018/08/make-new-larger-font-for-waveshare-spi.html). But they do not provide any code to use...

On the other hand the font2bytes from [Dominik Kapusta](https://github.com/ayoy/font2bytes/tree/master) is available but requires C++ compilers.

This is a version in Python. It converts a .ttf font file into a C
file compatible with Waveshare/STMicroelectronics
[fonts.h](https://github.com/STMicroelectronics/STM32CubeL1/blob/master/Utilities/Fonts/fonts.h)
(`sFONT` type struct).
It only recreates ASCII caracters, but you can use any font and specify any size.


## Requirements

* Python 3
* [Pillow](https://pillow.readthedocs.io/en/stable/index.html#) library  (NOTE: Pillow and PIL cannot co-exist in the same environment. Before installing Pillow, please uninstall PIL.)
* [numpy](https://numpy.org/install/) library

The simplest way is probably to run it with
[uv](https://docs.astral.sh/uv/) thanks to the pyproject.toml file:

```
uv run font2bytes.py
```

## Use

1. Get any font you want to use (.tff). Some are available in the ./fonts folder.

2. Run font2bytes, example for 40 pixel Roboto Bold font:
```
uv run font2bytes.py --ttf-input-file ./fonts/Roboto-Bold.ttf --height 40 --output-dir output/
```

3. C font file is created under `--output-dir` directory. Name is
   derived from TTF filename, in the example: `output/FontRobotoBold40.c`

4. Copy this C file within you project source folder (Arduino, STM32,
   ...)

5. Modify `fonts.h` to add a new `extern`, example: `extern sFONT
   FontRobotoBold40;`

6. Use the new font and enjoy!

```
Paint_DrawString_EN(5, 0, "Made with font2bytes!", &FontRobotoBold40, BLACK, WHITE);
```

## Examples

Within the ./output folder there are already a couple of .c files
already generated that can be used without running `font2bytes` program.


## font2bytes Usage

```
usage: font2bytes [-h] [-t TTF_INPUT_FILE] [-o OUTPUT_FILE | -d OUTPUT_DIR] [-n FONT_NAME]
                  [--height HEIGHT] [--width WIDTH] [--threshold THRESHOLD]
                  [--font-offset FONT_OFFSET] [-b BMP_DIR]

Generate C font files for e-Paper (WaveShare like) from .ttf files

options:
  -h, --help            show this help message and exit
  -t TTF_INPUT_FILE, --ttf-input-file TTF_INPUT_FILE
                        A .ttf font file (default: ./fonts/Roboto-Regular.ttf)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        C output filename (default: None)
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
                        C output directory. Use --font-name as file name or guess it.
                        (default: ./output/)
  -n FONT_NAME, --font-name FONT_NAME
                        Name of the sFONT object in the C file. If unspecified derive it
                        form input file name. (default: None)
  --height HEIGHT       Height of the generated font in pixel (default: 36)
  --width WIDTH         Width of the generated font in pixel. Defaults to 3/5 of --height.
                        (default: None)
  --threshold THRESHOLD
                        Image intensity threshold for binary conversion. It changes the
                        contrast of the final font. (default: 120)
  --font-offset FONT_OFFSET
                        Font offset, recommended to be at least 4. (default: 4)
  -b BMP_DIR, --bmp-dir BMP_DIR
                        Folder to save BMP intermediate image, if unspecified BMP image are
                        not saved. Useful for debugging. (default: None)
```

## Authors

 - TheHeXstyle
 - jfgd

## License

GPL v3.0, see LICENSE for details.
