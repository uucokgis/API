import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT UPDM Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [OluKMTool]


class DeadKMReport:
    """

    :dataclass fields
    OluKmReport reportOluKm = new OluKmReport
        {
            ID = (int)_result[0],
            MESAFE = (double)_result[1],
            SURE = (double)_result[2],
            GUZERGAH_ID = (int)_result[3],
            HAT_KODU = (string)_result[4],
            KESIT_KODU = (string)_result[5],
            ENVARTER_KODU = (string)_result[6],
            DURAK_KODU = (string)_result[7],
            XB = (string)_result[8],
            YB = (string)_result[9],
            XA = (string)_result[10],
            YA = (string)_result[11],
            GUZERGAH_KODU = (string)_result[12],
        };
    """


class OluKMTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Ölü KM Rapor Aracı"
        self.description = "Garaj -> Hat başı ve Hat sonu -> Garaj arasındaki " \
                           "şöförün yolcu taşımadığı kat edilen yolun raporu"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
