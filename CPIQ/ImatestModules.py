import json

from TestGlobals import *

def dotpattern(base):
    global images_dir, ini_file, lightConditions, op_mode
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
    global images_dir, ini_file, lightConditions, op_mode
    output = {}

    for lightSource in lightConditions:
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
    global imatest, op_mode, ini_file
    input_file = os.path.join(images_dir, base, base+'_Unif_100lux.jpg')

    print('Testing ' + base + ' Uniformity')

    if os.path.exists(input_file) != True:
        print('File ' + input_file + 'not found!')
        return

    result = imatest.uniformity_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
    data = json.loads(result)
    return data['uniformityResults']


def random(base):
    global images_dir, ini_file, lightConditions, op_mode, imatest
    output = {}
    for lightSource in lightConditions:
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
    global images_dir, ini_file, lightConditions, op_mode, setROI, tempINI
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

    for lightSource in lightConditions:
        print('Testing ' + base + ' Colorchecker SG at ' + lightSource)
        image_file = base + '_SG_' + lightSource + '.jpg'
        input_file = os.path.join(images_dir, base, image_file)

        if image_file.lower() in roiOverridesLower:
            setROI(roiOverridesLower[image_file.lower()], roiOverrides['width'], roiOverrides['height'])
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