import random
import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("dir", help="Target directory")
    parser.add_argument("-n", "--num", default=100, help="Number of files to select")
    return parser.parse_args()


def main():
    args = get_parser()

    item_dir = Path(args.dir)
    num = int(args.num)

    output_dir = Path(f"{item_dir.stem}-random_selected")
    output_dir.mkdir(exist_ok=True, parents=True)

    fp_list = list([fp for fp in item_dir.glob("*") if fp.is_file()])
    selected_list = random.sample(fp_list, num)
    print(selected_list)

    for fp in selected_list:
        shutil.move(str(fp), str(output_dir / fp.name))


if __name__ == "__main__":
    main()
