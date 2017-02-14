import os
import json
import ConfigParser
import log

import pprint
from ImatestModules import *
from math import *
from TestGlobals import *
from CPIQScore import *
import TestGlobals




# ... 
# Calculate results for a phone
# ...

def calcPhone(phone):
    global esfriso,multitest,dotpattern,random,uniformity,lightSourceFiles,imatest
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



# This array defines a set of devices we want to test
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
#phones = ['Apple_iPhone6sPlus']

doCalc = 1
doProcess = 1

if doCalc:

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

    #
    print('Combined JNDS:')
    for phone in phones:
        score = multivariateScore(data[phone])
        combined_QL = data[phone]['Combined_QL']
        print(phone + ", %.0f" ) % percentScoreClean(score)

