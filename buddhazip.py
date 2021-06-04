import pyzipper
import os
import traceback
import argparse
import random


def motivational_quote():
    quotes = (
        '"You know it’s a bad day when you jump out of bed and miss the floor!" – Anonymous',
        '"I know you believe you understand what I said, but I am not sure you realize that what you heard is not '
        'what I meant!" – Robert McCloskey',
        '"To say of what is that it is not, or of what is not that it is, is false, while to say of what is that it '
        'is, and of what is not that it is not, is true." – Aristotle',
        '"If you don’t know where you are going, you might wind up someplace else." – Yogi Berra',
        '"Sometimes when I close my eyes, I can\'t see." - Anonymous',
        '"Nothing is impossible unless you can\'t do it." - Anonymous'
    )
    return random.choice(quotes)


def zip_folder(source_path, destination_path, password):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """

    source_path = os.path.abspath(source_path)

    if not destination_path:
        destination_path = source_path + ".zip"

    if not destination_path.endswith(".zip"):
        destination_path += ".zip"

    try:
        parent_folder = os.path.dirname(source_path)
        contents = os.walk(source_path)

        if password:
            z = pyzipper.AESZipFile(destination_path + "\\", 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
            z.setpassword(password)
        else:
            z = pyzipper.ZipFile(destination_path + "\\", 'w', compression=pyzipper.ZIP_LZMA)

        try:
            for root, folders, files in contents:
                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(parent_folder + '\\', '')
                    print(f"Adding {absolute_path} to archive.")
                    z.write(absolute_path, relative_path)
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(parent_folder + '\\', '')
                    print(f"Adding {absolute_path} to archive.")
                    z.write(absolute_path, relative_path)
            print(f"{destination_path} created successfully.")

        except Exception:
            tb = traceback.format_exc()
            print("Something went wrong")
            print(tb)

        finally:
            z.close()

    except Exception:
        tb = traceback.format_exc()
        print("Something went wrong")
        print(tb)


def zip_single(source_path, destination_path, password):
    """Zip a single file"""

    if not destination_path:
        destination_path = source_path

    if not destination_path.endswith(".zip"):
        suffix = destination_path.split(".")[1]
        if destination_path.endswith("." + suffix):
            destination_path = destination_path.replace("." + suffix, '')
        destination_path += ".zip"

    if password:
        z = pyzipper.AESZipFile(destination_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
        z.setpassword(password)
    else:
        z = pyzipper.ZipFile(destination_path, 'w', compression=pyzipper.ZIP_LZMA)

    try:
        z.write(source_path)
        print(f"{destination_path} created successfully.")
    except Exception:
        tb = traceback.format_exc()
        print("Something went wrong")
        print(tb)
    finally:
        z.close()


def unzip_item(source_path, destination_path, password):
    """Unzip a file or folder"""

    if not destination_path:
        destination_path = source_path.replace(".zip", "")
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    else:
        destination_path += "_unzipped"
        if not os.path.isdir(destination_path):
            os.makedirs(destination_path)

    try:
        with pyzipper.AESZipFile(source_path) as z:
            members = z.infolist()
            for i, member in enumerate(members):
                z.extract(member, destination_path, pwd=password)
                print(f"Unpacked {member.filename} from archive.")
        print(f"{source_path} unpacked successfully to {destination_path}.")
    except Exception:
        tb = traceback.format_exc()
        print("Something went wrong")
        print(tb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=f"BuddhaZip - {motivational_quote()}\t")
    parser.add_argument('-u', action="store_true", help="Unzip")
    parser.add_argument('source', nargs='*', help="Source file or folder path (Required)")
    parser.add_argument('-d', '--destination', nargs='*', help="Destination folder path")
    parser.add_argument('-p', '--password', nargs='*', help="Zip password")
    args = parser.parse_args()

    is_unzip = True if args.u else False
    source_arg = ' '.join(args.source) if args.source else ''
    destination_arg = ' '.join(args.destination) if args.destination else ''
    password_arg = ' '.join(args.password).encode() if args.password else None

    if is_unzip and source_arg:
        if os.path.isfile(source_arg) and source_arg.endswith(".zip"):
            unzip_item(source_arg, destination_arg, password_arg)
        else:
            print("Invalid file type in source path")

    elif source_arg:
        if os.path.isdir(source_arg):
            zip_folder(source_arg, destination_arg, password_arg)
        elif os.path.isfile(source_arg):
            zip_single(source_arg, destination_arg, password_arg)
        else:
            print("Must be a valid source file or folder")

    else:
        parser.print_help()
