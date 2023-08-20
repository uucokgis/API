SDE_PATH = r'C:\YAYIN\TESTS\AKTARIM\New Folder\IETTORIGIN - SDE.sde'  # PROD ile degistir
DB_SCHEMA = 'SDE'

network_service_uri = "https://cbsproxy.ibb.gov.tr/?networkws&baslangic={bas_x}%7C{bas_y}" \
                      "&ara={ara}" \
                      "&bitis={bit_x}%7C{bit_y}"
ITRF96_7932_PROJECTION = """PROJCS["ITRF96 / TM30",GEOGCS["GCS_ITRF_1996",DATUM["D_ITRF_1996",
SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],
PARAMETER["central_meridian",30.0],PARAMETER["scale_factor",1.0],PARAMETER["latitude_of_origin",0.0],
UNIT["m",1.0]]"""