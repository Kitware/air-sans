from nexusformat.nexus import nxload


def load(dir, file):
    """
    load nexus file
    """
    path = dir + "/" + file
    return nxload(path)
