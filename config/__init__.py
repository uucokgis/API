import os

DEBUG = True

sde_prod = os.path.abspath('IETTPROD.sde')
sde_test = os.path.abspath('IETTORIGIN - SDE.sde')

if DEBUG:
    print("DEBUG MODE")
    arcpy.env.workspace = sde_test
else:
    print("PROD MODE")
    arcpy.env.workspace = sde_prod
