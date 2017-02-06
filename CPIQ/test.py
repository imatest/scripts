# Import the ImatestLibrary class from the imatest.it package 
import os
import json
import ConfigParser
import log
import sys, traceback
import enum

import pprint
from imatest.it import ImatestLibrary

################### Parameters #####################

root_dir = os.path.dirname(os.path.realpath(__file__))
ini_file = os.path.join(root_dir, os.pardir, 'ini_file', r'imatest-v2.ini')
tempINI = os.path.join(root_dir, os.pardir, 'ini_file', r'imatest-multicharts-roi.ini')
images_dir = os.path.join(root_dir, os.pardir,'RoundRobin')
op_mode = ImatestLibrary.OP_MODE_SEPARATE
led5k = "5000KLED_1000lux"
tl84 = "TL84_100lux"
tung = "Tung_10lux"
ERROR_RESULT = -65535
VN_NOT_FOUND = -65534
lightSourceFiles = [led5k,tl84,tung]

################### Support Functions #####################

def get_config(path):                                           # Used make ConfigParser case sensitive
    config = ConfigParser.ConfigParser()
    config.optionxform=str
    try:
        config.read(os.path.expanduser(path))
        return config
    except Exception, e:
        log.error(e)

def setROI(roi):
    global ini_file
    imatestini = get_config(ini_file)

    imatestini.set('ccsg', 'roi', roi)
    with open(tempINI, 'w') as outfile:
        imatestini.write(outfile)
    return


################### End Support Functions #################


def dotpattern(base):
    global images_dir, ini_file, lightSourceFiles, op_mode
    output = {}

    for lightSource in [led5k]:
        print('Testing ' + base + ' at ' + lightSource)
        input_file = os.path.join(images_dir, base, base+'_Dot_'+lightSource+'.jpg')

        if os.path.exists(input_file) != True:
            print('File ' + input_file + 'not found!')
            return

        print('opening ' + input_file)
        result = imatest.dotpattern_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[lightSource] = data['dotpatternResults'];

    return output

def esfriso(base):
    global images_dir, ini_file, lightSourceFiles, op_mode
    output = {}

    for lightSource in lightSourceFiles:
        print('Testing ' + base + ' eSFR ISO at ' + lightSource)
        input_file = os.path.join(images_dir, base, base+'_eSFR_'+lightSource+'.jpg')

        if os.path.exists(input_file) != True:
            print('File ' + input_file + 'not found!')
            return

        print('opening ' + input_file)
        result = imatest.esfriso_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[lightSource] = data['esfrisoResults'];

    return output

def uniformity(base):
    input_file = os.path.join(images_dir, base, base+'_Unif_100lux.jpg')

    print('Testing ' + base + ' Uniformity')

    if os.path.exists(input_file) != True:
        print('File ' + input_file + 'not found!')
        return

    result = imatest.uniformity_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
    data = json.loads(result)
    return data['uniformityResults']


def random(base):
    global images_dir, ini_file, lightSourceFiles, op_mode
    output = {}
    for lightSource in lightSourceFiles:
        print('Testing ' + base + ' Texture Blur at ' + lightSource)
        input_file = os.path.join(images_dir, base, base+'_Coins_'+lightSource+'.jpg')

        if os.path.exists(input_file) != True:
            print('File ' + input_file + 'not found!')
            return

        print('opening ' + input_file)

        result = imatest.random_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[lightSource] = data['randomResults'];
    return output;

def multitest(base):
    global images_dir, ini_file, lightSourceFiles, op_mode, setROI, tempINI
    output = {}

    # ROI overrides exist in these JSON files (what a pain, autodetection will be forthcoming...)
    roiOverrides = {}
    roiOverridesLower = {}
    roiOverrideFile = os.path.join(images_dir,base,'multicharts-rois.json')
    if os.path.exists(roiOverrideFile):
        with open(roiOverrideFile,'r') as fh:
            roiOverrides = json.load(fh)

        #convert to lower
        for override, rois in roiOverrides.iteritems():
            roiOverridesLower[override.lower()] = rois
    else:
        raise Exception('File Not Found','ROI override ' + roiOverrideFile + ' not found.')

    for lightSource in lightSourceFiles:
        print('Testing ' + base + ' Colorchecker SG at ' + lightSource)
        image_file = base + '_SG_' + lightSource + '.jpg'
        input_file = os.path.join(images_dir, base, image_file)

        if image_file.lower() in roiOverridesLower:
            setROI(roiOverridesLower[image_file.lower()])
            selectedINI = tempINI
        else:
            selectedINI = ini_file


        if os.path.exists(input_file) != True:
            print('File ' + input_file + 'not found!')
            return

        print('opening ' + input_file)
        result = imatest.multitest_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=selectedINI)
        data = json.loads(result)
        output[lightSource] = data['multitestResults'];
    return output

# ... 
# Calculate results for a phone
# ...

def calcPhone(phone):
    global esfriso,multitest,dotpattern,random,uniformity,lightSourceFiles
    print('Calculating Metrics for '+phone+ ' *****************************')
    uniformityResults = uniformity(phone)              # Uniformity
    multitestResults  = multitest(phone)               # Multitest
    dotpatternResults = dotpattern(phone)              # Dot Pattern
    esfrisoResults    = esfriso(phone)                 # eSFR ISO
    randomResults     = random(phone)                  # Random

    # Output Data
    filename = os.path.join(images_dir, phone, phone + '.json')
    with open(filename, 'w') as outfile:
        fullData = {'multitest':multitestResults,
                    'dotpattern':dotpatternResults,
                    'esfriso':esfrisoResults,
                    'random':randomResults,
                    'uniformity':uniformityResults}
        json.dump(fullData, outfile, indent=4, separators=(',',': '))
    return fullData

##############
# PROCESSING #
##############
def processPhone(phone):
    filename = os.path.join(images_dir, phone, phone + '.json')
    TB_QL = {}
    CL_QL = {}
    SFR_QL = {}
    VN_QL = {'count':0}
    try:
        with open(filename, 'r') as input:
            data = json.load(input)
    except:
        print("Can't read input file '" + filename + "'")
        return

    global esfriso,multitest,dotpattern,random,uniformity,lightSourceFiles

    print('Calculating Metrics for '+phone+ ' *****************************')
    # CU
    try:
        uniformityResults = data['uniformity']
        CU_QL = uniformityResults['QL_quality_loss_color_nonuniformity_CPIQ'][0]
        print('CU QL '  + str(CU_QL) + ' JND')
    except:
        print("***ERROR Can't find CU")

    # CL
    try:
        multitestResults = data['multitest']
        CL_QL = {}
        for lightSource in multitestResults:
            try:
                CL_QL[lightSource] = multitestResults[lightSource]['CPIQ_chroma_quality_loss'][0]
                print('CL QL ' + str(CL_QL[lightSource]) + ' JND at ' + lightSource)
            except:
                print("***ERROR Can't find CL at " + lightSource)
    except:
        print("***ERROR Can't find CL")

    # LGD
    try:
        dotpatternResults = data['dotpattern']
        LGD_QL = dotpatternResults[led5k]['CPIQ']['lensGeometricDistortion']['qualityLoss'][0]
        print('LGD QL ' + str(LGD_QL) + ' JND')
    except:
        print("***ERROR Can't find LGD")

    # LCD
    try:
        LCD_QL = dotpatternResults[led5k]['CPIQ']['lateralChromaticDisplacement']['qualityLoss'][0]
        print('LCD QL ' + str(LCD_QL) + ' JND')
    except:
        print("***ERROR Can't find LCD")

    # TB
    try:
        randomResults = data['random']
        TB_QL = {}
        for lightSource in randomResults:
            try:
                TB_QL[lightSource] = randomResults[lightSource]['CPIQ']['textureComputerMonitor']['qualityLoss'][0]
                print('TB QL ' + str(TB_QL[lightSource]) + ' JND at ' + lightSource)
            except:
                print("***ERROR Can't find TB at " + lightSource)
    except:
        print("***ERROR Can't find TB")

    # eSFR
    try:
        esfrisoResults = data['esfriso']
        SFR_QL = {}
        VN_QL = {}
        for lightSource in esfrisoResults:
            # SFR
            try:
                SFR_QL[lightSource] = esfrisoResults[lightSource]['CPIQ']['sfrComputerMonitor']['qualityLoss'][0] # +
                #      esfrisoResults[lightSource]['CPIQ']['sfrComputerMonitor']['qualityLoss'][1]) / 2
                print('SFR QL ' + str(SFR_QL[lightSource]) + ' JND at ' + lightSource)
            except:
                print("***ERROR Can't find SFR at " + lightSource)

            # VN
            try:
                VN_QL[lightSource] = esfrisoResults[lightSource]['VN_CPIQ_Quality_Loss_QL_1'][0]
                print('VN QL ' + str(VN_QL[lightSource]) + ' JND')
            except:
                print("Missing VN at " + lightSource)
    except:
        print("***ERROR Can't find eSFR ISO")


# Make Combined Score
    light_dependent_QL = {}
    combined_QL =  LGD_QL + LCD_QL + CU_QL
    VN_combined = 0
    SFR_combined = 0
    TB_combined = 0
    CL_combined = 0
    VN_QL['count'] = 0
    for lightSource in lightSourceFiles:
        # VN
        try:
            VN_combined = VN_combined + VN_QL[lightSource]
            VN_QL['count'] = VN_QL['count'] + 1
        except:
            print(' *** WARNING missing ' + lightSource + ' VN')

        # SFR
        try:
            SFR_combined = SFR_combined + SFR_QL[lightSource]
        except:
            print(' *** ERROR missing ' + lightSource + ' SFR')

        # TB
        try:
            TB_combined = TB_combined + TB_QL[lightSource]
        except:
            print(' *** ERROR missing ' + lightSource + ' TB')
        # CL
        try:
            CL_combined = CL_combined + CL_QL[lightSource]
        except:
            print(' *** ERROR missing ' + lightSource + ' CL')

    try:
        if VN_QL['count'] > 0:
            VN_combined = VN_combined / VN_QL['count']

        SFR_combined = SFR_combined / 3
        CL_combined = CL_combined / 3
        TB_combined = TB_combined / 3
    except:
        raise('Rebalancing error')

    #except:
    #    print("***ERROR Can't Combine Light Dependant score")

    # Finish the calcs
    try:
        combined_QL = combined_QL  + VN_combined + SFR_combined + TB_combined + CL_combined
        return {'SFR QL':SFR_QL, 'LGD QL':LGD_QL, 'LCD QL':LCD_QL, 'VN QL':VN_QL,
                'TB_QL':TB_QL, 'LGD QL':LGD_QL, 'CU QL':CU_QL, 'CL QL':CL_QL, 'Combined QL':combined_QL}
    except:
        print('***ERROR computing QL')
    #  MAIN #######


def percentScore(combined_JND):
    return round(100-(4*combined_JND/7),0)

#Calculate all the phones
phones = ['Apple_iPhone4',
          'Apple_iPhone5s',
          'Apple_iPhone6sPlus',
          'Google_Nexus6P',
          'HTC_OneM8',
          'Nokia_Lumia1020',
          'Samsung_GalaxyS7edge',
          'Sony_XperiaZ5',
          'LG_G2']

# override phones
#phones = ['Sony_XperiaZ5']

doCalc = 1
doProcess = 1

if doCalc:
    # Initialize Imatest Library - This may take a few seconds while the Matlab MCR is initialized
    imatest = ImatestLibrary()

    for phone in phones:
        calcPhone(phone)

    imatest.terminate_library()
    print('*************** CALCULATION DONE *********************** ')

if doProcess:
    data = {}
    for phone in phones:
        data[phone] = processPhone(phone)

    print('*************** PROCESSING DONE *********************** ')
    with open('fulldata.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '))

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    print('Combined JNDS:')

    for phone in phones:
        print(phone + ": " + str(data[phone]['Combined QL']) + ' JND')

    for phone in phones:
        print(phone + " Score: " + str(percentScore(data[phone]['Combined QL'])) + '')

#score = processPhone('Sony_XperiaZ5')
#print('score:'+str(score))
# When finished, terminate the library - This will unload the Matlab MCR and free up memory 
