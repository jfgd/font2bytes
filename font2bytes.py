import argparse
from pathlib import Path
from PIL import ImageDraw, ImageFont, Image
from numpy import asarray, ceil, array, sum, concatenate


binary_byte = array([128, 64, 32, 16, 8, 4, 2, 1])


def createTMPimage(font, height, width, ASCII) -> Image.Image:
    image = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    if font.getlength(chr(ASCII)) > width:
        temp_image = Image.new(
            "RGB", (int(font.getlength(chr(ASCII))), height), color=(0, 0, 0)
        )
        temp_draw = ImageDraw.Draw(temp_image)
        temp_draw.text((0, 0), chr(ASCII), font=font)
        squeezed_image = temp_image.resize((width, height), Image.Resampling.HAMMING)
        image.paste(squeezed_image, (0, 0))
    else:
        draw.text((0, 0), chr(ASCII), font=font)
    return image


def readImage2Binary(image: Image.Image, ASCII):
    data = asarray(image)
    binary_map = data[:, :, 0]
    return binary_map


def convertMap2Hex(height, width, threshold, binary_map):
    hex_map = []
    for line in range(binary_map.shape[0]):
        for bit_chunks in range(int(ceil(width / 8))):
            tmp = binary_map[line][bit_chunks * 8 : (min((bit_chunks + 1) * 8, width))]
            tmp = array(list(map(lambda x: int(x > threshold), tmp)))
            tmp = concatenate((tmp, array([0] * (8 - len(tmp)))))  # padding with zeros
            binary_value = int(sum(tmp * binary_byte))
            hex_map.append(f"{binary_value:#0{4}x}")

    return hex_map


def write_file_intro(f, height, width):
    f.write(
        "/* Includes ------------------------------------------------------------------*/\n"
    )
    f.write('#include "fonts.h"\n')
    f.write(f"static const uint8_t Font{height}_Table [] = \n")
    f.write("{\n")


def write_file_closure(f, font_name, height, width):
    f.write("};\n\n")
    f.write(f"sFONT {font_name} = {{\n")
    f.write(f"\tFont{height}_Table,\n")
    f.write(f"\t{width}, /* Width */\n")
    f.write(f"\t{height}, /* Height */\n")
    f.write("};\n\n")


def write_letter(f, height, width, hex_map):
    f.write(f'\t// ASCII: {ASCII} "{chr(ASCII)}" ({width} pixels wide)\n')

    count = 0
    f.write("\t")

    for item in hex_map:
        f.write(f"{item}, ")
        count += 1
        if count == 3:
            count = 0
            f.write("\n\t")

    f.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="font2bytes",
        description="Generate C/C++ font files for e-Paper "
        "(WaveShare like) from .ttf files",
    )

    parser.add_argument(
        "-t",
        "--ttf-input-file",
        type=Path,
        default="./fonts/Roboto-Regular.ttf",
        help="A .ttf font file",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=Path,
        default="./output/FontReg36.cpp",
        help="C/C++ output filename",
    )
    parser.add_argument(
        "-n",
        "--font-name",
        type=str,
        help="Name of the sFONT object in the C file. "
        "If unspecified derive it form input file name.",
    )
    parser.add_argument(
        "--height", type=int, default=36, help="Height of the generated font in pixel"
    )
    parser.add_argument(
        "--width", type=int, default=22, help="Height of the generated font in pixel"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=120,
        help="Image intensity threshold for binary conversion. "
        "It changes the contrast of the final font.",
    )
    parser.add_argument(
        "--font-offset",
        type=int,
        default=4,
        help="Font offset, recommended to be at least 4.",
    )
    parser.add_argument(
        "-b",
        "--bmp-dir",
        type=Path,
        help="Folder to save BMP intermediate image, if unspecified "
        "BMP image are not saved. Useful for debugging.",
    )

    args = parser.parse_args()

    if not args.ttf_input_file.is_file():
        print(f"File '{args.ttf_input_file}' can not be read")
        exit(1)

    if args.font_name is None:
        font_name = "Font" + args.ttf_input_file.stem
        for i in [" ", "-"]:
            font_name = font_name.replace(i, "")
        font_name += f"{args.height}"
    else:
        font_name = args.font_name

    print(
        f"Generating font '{font_name}' in {args.output_file} from TTF file {args.ttf_input_file}"
    )

    with open(args.output_file, "w") as cfile:
        font = ImageFont.truetype(args.ttf_input_file, args.height - args.font_offset)

        write_file_intro(cfile, args.height, args.width)

        for ASCII in range(32, 127):
            print(f"working on ASCII: {ASCII}: {chr(ASCII)}")

            image = createTMPimage(font, args.height, args.width, ASCII)
            if args.bmp_dir is not None:
                image.save(args.bmp_dir / f"{ASCII}.bmp")
            binary_map = readImage2Binary(image, ASCII)
            hex_map = convertMap2Hex(
                args.height, args.width, args.threshold, binary_map
            )
            write_letter(cfile, args.height, args.width, hex_map)

        write_file_closure(cfile, font_name, args.height, args.width)
