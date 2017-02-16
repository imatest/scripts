import json

from math import *
from TestGlobals import *

##############
# PROCESSING #
##############

def process_phone(phone):
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

    global esfriso,multitest,dotpattern,random,uniformity,light_conditions

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
        multitest_results = data['multitest']
        CL_QL = {}
        for light_source in multitest_results:
            try:
                CL_QL[light_source] = multitest_results[light_source]['CPIQ_chroma_quality_loss'][0]
                print('CL QL ' + str(CL_QL[light_source]) + ' JND at ' + light_source)
            except:
                print("***ERROR Can't find CL at " + light_source)
    except:
        print("***ERROR Can't find CL")

    # LGD
    try:
        dotpattern_results = data['dotpattern']
        LGD_QL = dotpattern_results[led5k]['CPIQ']['lensGeometricDistortion']['qualityLoss'][0]
        print('LGD QL ' + str(LGD_QL) + ' JND')
    except:
        print("***ERROR Can't find LGD")

    # LCD
    try:
        LCD_QL = dotpattern_results[led5k]['CPIQ']['lateralChromaticDisplacement']['qualityLoss'][0]
        print('LCD QL ' + str(LCD_QL) + ' JND')
    except:
        print("***ERROR Can't find LCD")

    # TB
    try:
        random_results = data['random']
        TB_QL = {}
        for light_source in random_results:
            try:
                TB_QL[light_source] = random_results[light_source]['CPIQ']['textureComputerMonitor']['qualityLoss'][0]
                print('TB QL ' + str(TB_QL[light_source]) + ' JND at ' + light_source)
            except:
                print("***ERROR Can't find TB at " + light_source)
    except:
        print("***ERROR Can't find TB")

    # eSFR
    try:
        esfrisoResults = data['esfriso']
        SFR_QL = {}
        VN_QL = {}
        for light_source in esfrisoResults:
            # SFR
            try:
                SFR_QL[light_source] = esfrisoResults[light_source]['CPIQ']['sfrComputerMonitor']['qualityLoss'][0] # +
                #      esfrisoResults[light_source]['CPIQ']['sfrComputerMonitor']['qualityLoss'][1]) / 2
                print('SFR QL ' + str(SFR_QL[light_source]) + ' JND at ' + light_source)
            except:
                print("***ERROR Can't find SFR at " + light_source)

            # VN
            try:
                VN_QL[light_source] = esfrisoResults[light_source]['VN_CPIQ_Quality_Loss_QL_1'][0]
                print('VN QL ' + str(VN_QL[light_source]) + ' JND')
            except:
                print("Missing VN at " + light_source)
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
    for light_source in light_conditions:
        # VN
        try:
            VN_combined = VN_combined + VN_QL[light_source]
            VN_QL['count'] = VN_QL['count'] + 1
        except:
            print(' *** WARNING missing ' + light_source + ' VN')

        # SFR
        try:
            SFR_combined = SFR_combined + SFR_QL[light_source]
        except:
            print(' *** ERROR missing ' + light_source + ' SFR')

        # TB
        try:
            TB_combined = TB_combined + TB_QL[light_source]
        except:
            print(' *** ERROR missing ' + light_source + ' TB')
        # CL
        try:
            CL_combined = CL_combined + CL_QL[light_source]
        except:
            print(' *** ERROR missing ' + light_source + ' CL')

    try:
        if VN_QL['count'] > 0:
            VN_combined = VN_combined / VN_QL['count']

        SFR_combined = SFR_combined / 3
        CL_combined = CL_combined / 3
        TB_combined = TB_combined / 3
    except:
        raise('Rebalancing error')

    # Finish the calcs
    try:
        combined_QL = combined_QL  + VN_combined + SFR_combined + TB_combined + CL_combined
        return {'SFR_QL':SFR_QL, 'LGD_QL':LGD_QL, 'LCD_QL':LCD_QL, 'VN_QL':VN_QL,
                'TB_QL':TB_QL,   'CU_QL':CU_QL,    'CL_QL':CL_QL,  'Combined_QL':combined_QL}
    except:
        print('***ERROR computing QL')
    #  MAIN #######

