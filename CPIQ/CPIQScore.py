import json

from math import *
from TestGlobals import *

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

    global esfriso,multitest,dotpattern,random,uniformity,lightConditions

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
    for lightSource in lightConditions:
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
        return {'SFR_QL':SFR_QL, 'LGD_QL':LGD_QL, 'LCD_QL':LCD_QL, 'VN_QL':VN_QL,
                'TB_QL':TB_QL,   'CU_QL':CU_QL,    'CL_QL':CL_QL,  'Combined_QL':combined_QL}
    except:
        print('***ERROR computing QL')
    #  MAIN #######

def multivariateScore(dev):
    scores = [dev['SFR_QL'][led5k],dev['SFR_QL'][tung],dev['SFR_QL'][tl84],
              dev['CL_QL'][led5k], dev['CL_QL'][tung], dev['CL_QL'][tl84],
              dev['VN_QL'][led5k], dev['VN_QL'][tung], dev['VN_QL'][tl84],
              dev['TB_QL'][led5k], dev['TB_QL'][tung], dev['TB_QL'][tl84],
              dev['CU_QL'],        dev['CU_QL'],       dev['CU_QL'],
              dev['LGD_QL'],       dev['LGD_QL'],      dev['LGD_QL'],
              dev['LCD_QL'],       dev['LCD_QL'],      dev['LCD_QL']]

    scoreMod = []
    deltaQmax = 30
    quotientDividend = 16.9
    Nm = 1 + 2 * tanh(deltaQmax/quotientDividend)

    for score in scores:
        if score < 0:
            print("** ERROR negative score: " + str(score))
            score=0
        scoreMod.append(score ** Nm)

    return -((sum(scoreMod)) ** (1/Nm))

def percentScoreAugmented(combined_JND):
    return 100+(4*combined_JND/7)

def percentScoreClean(multivariate_JND):
    return 100+multivariate_JND