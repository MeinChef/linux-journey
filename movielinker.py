import os
import re
from string import punctuation, digits
import argparse
from pathlib import Path


def validate_source(source: Path | str) -> Path:
    
    if os.path.isabs(source):
        full = source
    else:
        full = os.path.join("/opt/jellyfin/qbits", source)
    
    if os.path.exists(full):
        return Path(full)
    else:
        raise OSError(f"Source Path ({full}) does not exist or is not permitted. Please provide a correct path.")

def validate_target(target) -> Path:

    if os.path.isabs(target):
        full = target
    else:
        full = os.path.join("/opt/jellyfin", target)
    
    if not os.path.exists(full):
        raise OSError(f"Target Path ({full}) does not exist or is not permitted. Please provide a correct path.")

    if len(os.listdir(full)) == 0 or force:
        return Path(full)
    else:
        raise ValueError(f"Target directory ({target}) is not empty. Abort. If this is desired, re-run the program with -f")


def scan_folder(path: Path) -> tuple[dict, dict]:
    files = {}
    subdirs = {}

    for obj in path.iterdir():
        if obj.is_file():
            # for more concise accessing and declaration later on
            files[obj.name] = {
                "source": obj,
                "name": None,
                "extension": obj.suffix,
                "season": None,
                "episode": None,
                "year": ""
            }

        else: 
            subdirs[obj.name] = scan_subfolder(obj)

    return files, subdirs

def scan_subfolder(folder: Path) -> list: # recursively
    contents = []
    for item in folder.iterdir():
        if item.is_file():
            contents.append(item)
        else:
            contents.append(*scan_subfolder(item)) # for a 1-D list.
    
    return contents 


def enter_showname():
    # invalid filenames: contain / or \0 or empty string
    forbidden_chars = r'[\x00/\\:*?"<>|]'
    print("For above reason, the program could not find a good showname. Please provide the one you would like to use.")
    while True:
        showname = input()
        if re.search(forbidden_chars, showname) is None and showname != "":
            return showname
        print(f"Not a valid name. Invalid chars include: {forbidden_chars}")

def infer_name(contents: list[str]) -> str:
    # split by ' ' or '.', then throw out everything with '[]' '()' '{}', and numbers, and '-'
    # ask if season correct, and if not what should be removed
    # if second time incorrect, ask for user-provided.

    def checkname(name) -> tuple[str, bool]:
        separator = " ."
        new_sep = ""
        
        for sep in separator:
            if len(name.split(sep)) <= 1:
                continue
            else:
                new_sep = sep
                break
        
        # make sure we actually found a separator
        if new_sep == "":
            print("No valid separator found")
            return enter_showname(), True

        # make guess
        pattern = re.compile("[" + re.escape(punctuation) + digits + "]")

        showname = name.split(new_sep)
        showname = [
            part for part in showname if re.search(pattern, part) is None
        ]
        return " ".join(showname), False

    # guess multiple times: reasoning maybe the first time was a bad choice.
    guess = ""
    for file in contents:
        guess, manual_name = checkname(file)
        if manual_name:
            return guess

        # check if this guess can be found in a lot the other items
        counter = sum([True for item in contents if guess in item])
        if counter >= (2/3 * len(contents)):
            break


    # just asking the user if the program did good
    while True:
        print(f"The current guess for the name of the show is: {guess}.")
        check = input("Do you want to continue with this? [Y/n] ")
        if check.lower() in ["y", "yes", ""]:
            return guess
        
        elif check.lower() in ["n", "no"]:
            return enter_showname()


def infer_episode_nr(
        name: str, 
        offset: int = 0
    ) -> str | bool:

    # episodes atm:
    # ' ## '
    # ' ##v# '
    # '[##]'
    # 'E##'
    # tldr: left and right of two numbers, with the exception of E (left) and v (right).
    # probably also should be case-insensitive
    pattern = r'(?:\s+|$|E)(\d+)(?:\s+|v\d+|$|_rev)'
    match = re.search(pattern, name)
    
    if match:
        episodenr = int(match.group(1))
        episodenr -= offset
        return str(episodenr).zfill(2)
    else:
        return False


def infer_season(target: Path) -> str | bool:
    # search for at least one digit in the parent folder name
    season = re.search(r"\d+", target.parent.name)
    if season:
        return season.group().zfill(2) # to have seasons of naming scheme [01, 02, ...]
    return False

def linker(
        content: dict, 
        subfolder: dict,
        targetdir: Path
    ) -> bool:

    # TODO: subfolder logic still missign
    # get the common filepath of content[0] and each subfolder, to remove that frome the subfolder source and replace it with the target direcotry

    for item in content.items():
        item = item[1]
        season = "S" + item["season"] if item["season"] else ""
        episode = "E" + item["episode"] if item["episode"] else item["year"]

        target = targetdir.joinpath(
                item["name"] + " " +
                season +
                episode +
                item["extension"]
        )
        target.symlink_to(item["source"])
    return True

def main() -> None:
    parser = argparse.ArgumentParser(
        description = "A program to soft-link the contents of the source folder to the target folder"
    )
    parser.add_argument("source", help = "The directory for the program to scan for files. If not in /opt/jellyfin/qbits, please provide the absolute path.")
    parser.add_argument("target", help = "The directory for the program to link the files found in source to. If not in /opt/jellyfin/, please provide the absolute path.")
    parser.add_argument("-n", "--offset", help = "Specifies an integer offset that will be applied to the Episode number.")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Increase verbosity.")
    parser.add_argument("-f", "--force", action = "store_true", help = "With this option enabled, the program will try to execute and ignore all safeguards. Not recommended.")
    args = parser.parse_args()

    global force
    force = args.force

    source_pth = validate_source(args.source)
    target_pth = validate_target(args.target)

    source_cont, subfolders = scan_folder(source_pth)
    
    season = infer_season(target_pth)
    showname = infer_name(list(source_cont.keys()))
    
    for item in source_cont.keys():
        source_cont[item]["name"] = showname
        source_cont[item]["season"] = season
        source_cont[item]["episode"] = infer_episode_nr(item, args.offset)
    
    linker(
        source_cont,
        subfolders,
        target_pth
    )
    


if __name__ == "__main__":
    main()