import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "IETT Report Generator Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ReportGenerator]


class ReportGenerator(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Report Generator"
        self.description = "Sartnamedeki tum raporlarin uretim araci. Bir cogu viewlardan beslenir."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        report_param = arcpy.Parameter(
            displayName="Rapor",
            datatype="GPString",
            name="Rapor",
            parameterType="Required",
            direction="Input"
        )

        out_excel = arcpy.Parameter(
            displayName="Output Report",
            datatype="GPDataFile",
            name="Output",
            parameterType="Derived",
            direction="Output"
        )

        report_param.filter.list = [
            "Durak Cephe Ölçüleri",
            "Duraklar Arası Mesafe Süre",
            "Duraklar için Engelli Erişim Listesi",
            "Duraklar",
            "Durakların Güzergah Raporu",
            "Fotoğraf Olmayan Durak Raporu",
            "Garajlar Raporu",
            "Güzergah Ölü KM Raporu",
            "Güzergahların ilk Son Durak Raporu",
            "Güzergahsız Durak Raporu",
            "Güzergahtan Bağımsız Segmentler Raporu",
            "Güzergahlar Raporu",
            "Hat Başı Hat Sonu Raporu",  # şartnamede var appde yok
            "Hatlar Raporu",
            "BA Raporu",
            # "Proje Alanı Raporu",
            # "İlçe Kartı Raporu",
            "Koordinatlı Hat Durak Sıra Liste Raporu"
            "Peronlar Raporu",
            # "Güzergah Değişim Raporu",
            # "Durak Değişim Raporu"

        ]

        parameters = [report_param, out_excel]
        return parameters

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
