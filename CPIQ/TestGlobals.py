####################
# Global variables #
####################
import os, log, ConfigParser
from imatest.it import ImatestLibrary    # Import the ImatestLibrary class from the imatest.it package

# Initialize Imatest Library - This may take a few seconds while the Matlab MCR is initialized
imatest = ImatestLibrary()

root_dir = os.path.dirname(os.path.realpath(__file__))
ini_file = os.path.join(root_dir, os.pardir, 'ini_file', r'imatest-v2.ini')
tempINI = os.path.join(root_dir, os.pardir, 'ini_file', r'imatest-multicharts-roi.ini')
images_dir = os.path.join(root_dir, os.pardir,'RoundRobin')
op_mode = ImatestLibrary.OP_MODE_SEPARATE
led5k = "5000KLED_1000lux"
tl84 = "TL84_100lux"
tung = "Tung_10lux"
light_conditions = [led5k, tl84, tung]
ERROR_RESULT = -65535
VN_NOT_FOUND = -65534

################### Support Functions #####################

def get_config(path):                                           # Used make ConfigParser case sensitive
    config = ConfigParser.ConfigParser()
    config.optionxform=str
    try:
        config.read(os.path.expanduser(path))
        return config
    except Exception, e:
        log.error(e)

def setROI(roi,width,height):
    global ini_file
    imatestini = get_config(ini_file)

    imatestini.set('ccsg', 'roi', roi)
    imatestini.set('ccsg', 'nwid_save', width)
    imatestini.set('ccsg', 'nht_save', height)
    with open(tempINI, 'w') as outfile:
        imatestini.write(outfile)
    return


################### End Support Functions #################