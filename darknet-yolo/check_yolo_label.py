from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw

import sys
from argparse import ArgumentParser


def surround_by_bbox(img_path: str) -> None:
    img = Path(img_path)
    txt = img.with_suffix(".txt")

    if not (img.exists() and txt.exists()):
        print(f"'{img}' or '{txt}' is not exist.")
        return

    def calc_offset(origin: float, offset: float) -> Tuple[float, float]:
        return (origin - offset, origin + offset)

    with Image.open(str(img)) as im:
        draw = ImageDraw.Draw(im, "RGBA")  # with alpha channel

        lines = txt.open().readlines()
        for line in lines:
            cls_id, *params = line.split(" ")
            x_center, y_center, width, height = map(float, params)

            # proportion -> pixel
            w, h = im.size
            x_center *= w
            y_center *= h
            width *= w
            height *= h

            x_offset = width * 0.5
            y_offset = height * 0.5

            left, right = calc_offset(x_center, x_offset)
            top, bottom = calc_offset(y_center, y_offset)
            bbox = (left, top, right, bottom)

            draw.rectangle(xy=bbox, fill=(255, 128, 0, 128), outline=(0, 0, 0), width=2)  # type: ignore
            draw.text((x_center, y_center), cls_id, fill=(0, 0, 0))  # type: ignore

        # im.save("out.jpg", quality=95)
        im.show()


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        argv.append(input("enter img path>"))

    argv = argv[1:]  # ignore *.py
    for img_path in argv:
        p = Path(img_path)
        if p.is_dir():
            for x in p.glob("*.*[!txt]"):  # exclude txt file
                surround_by_bbox(str(x))
        else:
            surround_by_bbox(img_path)
