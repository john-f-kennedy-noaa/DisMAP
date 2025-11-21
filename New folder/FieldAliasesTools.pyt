# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BulkAssignAliases]


class BulkAssignAliases(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Bulk Assign Aliases"
        self.description = "Bulk-assign aliases from a metadata table to gdb tables"

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []

        params.append(arcpy.Parameter(
            displayName="Input attribute table",
            name="att_table",
            datatype=["GPFeatureLayer", "GPTableView"],
            parameterType="Required",
            direction="Input"))
        params[0].description = 'This is an attribute table with cryptic field names. Aliases will be applied to these fields from the lookup table.'

        params.append(arcpy.Parameter(
            displayName="Input lookup table",
            name="lookup_table",
            datatype=["GPFeatureLayer", "GPTableView"],
            parameterType="Required",
            direction="Input"))

        params.append(arcpy.Parameter(
            displayName="Short name field",
            name="shortname_field",
            datatype="Field",
            parameterType="Required",
            direction="Input"))
        params[2].parameterDependencies = ["lookup_table"]
        params[2].filter.list = ["Text"]

        params.append(arcpy.Parameter(
            displayName="Long name field",
            name="longname_field",
            datatype="Field",
            parameterType="Required",
            direction="Input"))
        params[3].parameterDependencies = ["lookup_table"]
        params[3].filter.list = ["Text"]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

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
        # Variables
        att_table = parameters[0].valueAsText
        lookup_table = parameters[1].valueAsText
        shortname_field = parameters[2].valueAsText
        longname_field = parameters[3].valueAsText

        # Loop
        arcpy.AddMessage("Loading field names...")
        lookupDict = {}  # <Short_Name>: <Full_Name>
        with arcpy.da.SearchCursor(lookup_table, [shortname_field, longname_field]) as cursor:
                for row in cursor:
                        lookupDict[row[0]] = row[1] 

        fieldList = arcpy.ListFields(att_table)
        arcpy.AddMessage("Processing fields...")
        total_fields = len(fieldList)
        for i, field in enumerate(fieldList):
                if field.name in lookupDict.keys():
                        arcpy.AddMessage("{0} ({1}/{2})".format(field.name, i+1, total_fields))
                        arcpy.management.AlterField(in_table=att_table, field=field.name, new_field_alias=lookupDict[field.name])
                else:
                    arcpy.AddMessage("{0} not in lookup table. Skipped ({1}/{2})".format(field.name, i+1, total_fields))
        return


