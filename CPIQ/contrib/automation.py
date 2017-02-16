# Automation of CPIQ metric extraction from Imatest 4.4.x

# Produced by Yixuan Wang on behalf of NVIDIA - Published 2016-09-15

# You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, 
# with or without modifications, and in Source or Object form, provided that You retain, in the 
# Source form of any Derivative Works that You distribute, all attribution notices from the Source 
# form of the Work, excluding those notices that do not pertain to any part of the Derivative Works.


import os
import numpy
import re
import glob
import csv
import sys
from xlrd import *
from xlwt import *
import pdb
import json

wb = Workbook()



# chroma
# add sheets
ws_chromaQL = wb.add_sheet("Chroma QL")
ws_chromaOM = wb.add_sheet("Chroma OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\CCSG*_multitest.json')


for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[2]+'_'+f.split("_")[3]+'_'+f.split("_")[4]
    ws_chromaQL.write(row,col,name)
    ws_chromaOM.write(row, col, name)
    col = col + 1

    data_ChromaQL = str(jdata["jsonResults"]["CPIQ_chroma_quality_loss"])
    data_ChromaOM = str(jdata["jsonResults"]["mean_chroma_level_CPIQ_Pct"])
    ws_chromaQL.write(row,col,data_ChromaQL)
    ws_chromaOM.write(row, col, data_ChromaOM)
    col = col + 1


    row = row+1
    col = 0



# color uniformity
# add sheets
ws_QL = wb.add_sheet("Uniformity QL")
ws_OM = wb.add_sheet("Uniformity OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\Diffuser*.json')


for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[2]+'_'+f.split("_")[3]+'_'+f.split("_")[4]
    ws_QL.write(row,col,name)
    ws_OM.write(row, col, name)
    col = col + 1

    data_QL = str(jdata["uniformityResults"]["QL_quality_loss_color_nonuniformity_CPIQ"])
    data_OM = str(jdata["uniformityResults"]["Dc_max_color_nonuniformity_CPIQ"])
    ws_QL.write(row,col,data_QL)
    ws_OM.write(row, col, data_OM)
    col = col + 1


    row = row+1
    col = 0



# MTF
# add sheets
ws_QL = wb.add_sheet("MTF QL")
ws_OM = wb.add_sheet("MTF OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\MTF*.json')


for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[3]+'_'+f.split("_")[4]+'_'+f.split("_")[5]+'_'+f.split("_")[6]
    ws_QL.write(row,col,name)
    ws_OM.write(row, col, name)
    col = col + 1

    data_QL = str(jdata["sfrResults"]["CPIQ"]["sfrComputerMonitor"]["qualityLoss"])
    data_OM = str(jdata["sfrResults"]["CPIQ"]["sfrComputerMonitor"]["acutance"])
    ws_QL.write(row,col,data_QL)
    ws_OM.write(row, col, data_OM)
    col = col + 1


    row = row+1
    col = 0






        # Texture
        # add sheets
ws_QL = wb.add_sheet("Texture QL")
ws_OM = wb.add_sheet("Texture OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\Texture*.json')

for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[2] + '_' + f.split("_")[3] + '_' + f.split("_")[4]
    ws_QL.write(row, col, name)
    ws_OM.write(row, col, name)
    col = col + 1

    data_QL = str(jdata["jsonResults"]["CPIQ"]["textureComputerMonitor"]["qualityLoss"])
    data_OM = str(jdata["jsonResults"]["CPIQ"]["textureComputerMonitor"]["acutance"])
    ws_QL.write(row, col, data_QL)
    ws_OM.write(row, col, data_OM)
    col = col + 1

    row = row + 1
    col = 0




    # LGD
    # add sheets
ws_QL = wb.add_sheet("LGD QL")
ws_OM = wb.add_sheet("LGD OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\Dots*.json')

for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[2] + '_' + f.split("_")[3]
    ws_QL.write(row, col, name)
    ws_OM.write(row, col, name)
    col = col + 1

    data_QL = str(jdata["jstr"]["CPIQ"]["lensGeometricDistortion"]["qualityLoss"])
    data_OM = str(jdata["jstr"]["CPIQ"]["lensGeometricDistortion"]["metric"])
    ws_QL.write(row, col, data_QL)
    ws_OM.write(row, col, data_OM)
    col = col + 1

    row = row + 1
    col = 0


    # Chromatic aberration
    # add sheets
ws_QL = wb.add_sheet("CA QL")
ws_OM = wb.add_sheet("CA OM")
row = 0
col = 0

# glob files
files = glob.glob('Results\\Dots*.json')

for f in files:
    jdata = json.loads(open(f).read())
    name = f.split("_")[2] + '_' + f.split("_")[3]
    ws_QL.write(row, col, name)
    ws_OM.write(row, col, name)
    col = col + 1

    data_QL = str(jdata["jstr"]["CPIQ"]["lateralChromaticDisplacement"]["qualityLoss"])
    data_OM = str(jdata["jstr"]["CPIQ"]["lateralChromaticDisplacement"]["metric"])
    ws_QL.write(row, col, data_QL)
    ws_OM.write(row, col, data_OM)
    col = col + 1

    row = row + 1
    col = 0


wb.save('results.xls')