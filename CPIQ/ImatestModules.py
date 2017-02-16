import json
from TestGlobals import *

# Dot Pattern is used to test Lateral Chromatic Displacement (LGD) and Lateral Geometric Distortion (LGD)
def dotpattern(base):
    global images_dir, ini_file, light_conditions, op_mode
    output = {}
    for light_source in [led5k]:
        print('Testing ' + base + ' at ' + light_source)
        input_file = os.path.join(images_dir, base, base+'_Dot_'+light_source+'.jpg')
        if os.path.exists(input_file) != True:
            raise Exception('File Not Found', 'File ' + input_file + 'not found!')

        print('opening ' + input_file)
        result = imatest.dotpattern_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[light_source] = data['dotpatternResults'];

    return output

# eSFR ISO (ISO 12233:2014) is used to test Visual Noise (VN) and Spatial Frequency Response (SFR)
def esfriso(base):
    global images_dir, ini_file, light_conditions, op_mode
    output = {}
    for light_source in light_conditions:
        print('Testing ' + base + ' eSFR ISO at ' + light_source)
        input_file = os.path.join(images_dir, base, base+'_eSFR_'+light_source+'.jpg')
        if os.path.exists(input_file) != True:
            raise('File ' + input_file + 'not found!')
        print('opening ' + input_file)
        result = imatest.esfriso_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[light_source] = data['esfrisoResults'];

    return output

# Uniformity is currently tested under one illuminant
def uniformity(base):
    global imatest, op_mode, ini_file
    input_file = os.path.join(images_dir, base, base+'_Unif_100lux.jpg')
    print('Testing ' + base + ' Uniformity')
    if os.path.exists(input_file) != True:
        raise('File ' + input_file + 'not found!')
    result = imatest.uniformity_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
    data = json.loads(result)

    return data['uniformityResults']

# Texture Blur (TB) is obtained from random analysis of the Spilled Coins test chart
def random(base):
    global images_dir, ini_file, light_conditions, op_mode, imatest
    output = {}
    for lightSource in light_conditions:
        print('Testing ' + base + ' Texture Blur at ' + lightSource)
        input_file = os.path.join(images_dir, base, base+'_Coins_'+lightSource+'.jpg')
        if os.path.exists(input_file) != True:
            raise('File ' + input_file + 'not found!')
        print('opening ' + input_file)
        result = imatest.random_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=ini_file)
        data = json.loads(result)
        output[lightSource] = data['randomResults']

    return output

def multitest(base):
    global images_dir, ini_file, light_conditions, op_mode, setROI, tempINI
    output = {}
    # Manually selected ROI's for Colorchecker SG are contained in these JSON files
    # TODO add colorchecker SG autodetection then remove all of this
    roi_overrides = {}
    roi_overrides_lower = {}
    roi_override_file = os.path.join(images_dir,base,'multicharts-rois.json')
    if os.path.exists(roi_override_file):
        with open(roi_override_file,'r') as fh:                     # read ROI override file
            roi_overrides = json.load(fh)
        for override, rois in roi_overrides.iteritems():            # convert to lowercase
            roi_overrides_lower[override.lower()] = rois
    else:
        raise Exception('File Not Found','ROI override ' + roi_override_file + ' not found.')

    for lightSource in light_conditions:
        print('Testing ' + base + ' Colorchecker SG at ' + lightSource)
        image_file = base + '_SG_' + lightSource + '.jpg'
        input_file = os.path.join(images_dir, base, image_file)

        # Check our
        if image_file.lower() in roi_overrides_lower:
            setROI(roi_overrides_lower[image_file.lower()], roi_overrides['width'], roi_overrides['height'])
            selectedINI = tempINI
        else:
            raise Exception('Missing ROI Override', 'Missing ROI override for ' + image_file)

        if os.path.exists(input_file) != True:
            raise Exception('File Not Found','File ' + input_file + 'not found!')

        print('opening ' + input_file)
        result = imatest.multitest_json(input_file=input_file, root_dir=root_dir, op_mode=op_mode, ini_file=selectedINI)
        data = json.loads(result)
        output[lightSource] = data['multitestResults'];

    return output