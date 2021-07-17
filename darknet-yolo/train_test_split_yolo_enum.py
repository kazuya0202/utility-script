from __future__ import annotations

import random
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from pathlib import Path


def get_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("dir", help="Target directory")
    parser.add_argument(
        "-n", "--num", default=1000, help="Number of file that will be enumerated to 'test.txt'"
    )
    return parser.parse_args()


@dataclass
class FilePair:
    txt: Path

    img: Path = field(init=False)
    exts: list[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.exts = [".jpg", ".png", ".jpeg", ".gif", ".bmp"]
        self.get_paired_image_path()

    def get_paired_image_path(self) -> None:
        # check existance: paired image file with txt
        for ext in self.exts:
            img_fp = self.txt.with_suffix(ext)
            if img_fp.exists():
                self.img = img_fp
                return

        print("There is not a paired image file with txt.")


def enumerate_to_file(pair_list: list[FilePair], output_fp: Path):
    with output_fp.open("w") as f:
        for pl in pair_list:
            f.write(f"{pl.img.absolute()}\n")


def main():
    args = get_parser()

    test_itme_num = int(args.num)
    item_dir = Path(args.dir)

    if not item_dir.exists():
        print(f"'{item_dir} does not exist.")
        exit()
    if item_dir.is_file():
        print(f"'{item_dir}' is not directory.")
        exit()

    pair_list = [FilePair(x) for x in item_dir.glob("*.txt")]

    # shuffle and split list
    random.shuffle(pair_list)
    train_files = pair_list[test_itme_num:]
    test_files = pair_list[:test_itme_num]

    # make 'train.txt' and 'test.txt'
    current = Path()
    train_fp = current / "train.txt"
    test_fp = current / "test.txt"
    enumerate_to_file(train_files, output_fp=train_fp)
    enumerate_to_file(test_files, output_fp=test_fp)


if __name__ == "__main__":
    main()
