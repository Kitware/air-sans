import os


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dirlist = []
    rootdir = rootdir.rstrip(os.sep)
    for path, dirs, _ in os.walk(rootdir):
        sublist = []
        for dir in dirs:
            item = {
                "name": dir,
                "type": "dir",
                "path": path + "/" + dir,
                "children": None,
            }
            sublist.append(item)
        if not search_replace(dirlist, path, sublist):
            for item in sublist:
                dirlist.append(item)
    return dirlist


def get_file_list(path):
    """
    Creates a list of files in a folder
    """
    filelist = os.listdir(path)
    return filelist


def search_replace(data, path, subdata):
    found = False
    for item in data:
        if item["path"] == path:
            item["children"] = subdata
            found = True
            break
    return found
