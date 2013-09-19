from os.path import dirname, abspath, isdir, realpath
from os import makedirs


main_dir = abspath(dirname(dirname(realpath(__file__))))

def __chkdir__(dirpath):
    if not isdir(abspath(main_dir + dirpath)):
        makedirs(abspath(main_dir + dirpath))

def __getfile__(filepath):
    # Remove slash at beginning and split into dirs
    dirs = filepath[1:].split('/')
    path = '/'
    for cdir in dirs:
        if '.' in cdir:
            # ignore files
            continue
        path += cdir
        __chkdir__(path)
    return abspath(main_dir + filepath)

COOKIES_FILE = __getfile__('/data/cookies.lwp')
LOG_FILE = __getfile__('/log/neopets-api.log')
CORE_CONFIG_FILE = __getfile__('/config/core.conf')
