# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      john.f.kennedy
#
# Created:     03/03/2024
# Copyright:   (c) john.f.kennedy 2024
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os
import sys
import traceback
import inspect
import arcpy


def feature_sharing_draft_report(sd_draft=""):
    try:
        import xml.dom.minidom as DOM

        docs = DOM.parse(sd_draft)
        key_list = docs.getElementsByTagName("Key")
        value_list = docs.getElementsByTagName("Value")

        for i in range(key_list.length):
            value = (
                f"Value: {value_list[i].firstChild.nodeValue}"
                if value_list[i].firstChild
                else "Value is missing"
            )

            arcpy.AddMessage(f"\t\tKey: {key_list[i].firstChild.nodeValue:<45} {value}")
            # arcpy.AddMessage(f"\t\tKey: {key_list[i].firstChild.nodeValue:<45} {value[:50]}")
            del i, value

        del DOM, key_list, value_list, docs
        del sd_draft

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk


def create_feature_class_layers(project_folder=""):
    try:
        # Import
        from arcpy import metadata as md
        from dismap_tools import dataset_title_dict

        # Set varaibales
        project_gdb = os.path.join(project_folder, os.path.basename(project_folder) + ".gdb")
        project_name = os.path.basename(project_folder)
        csv_data_folder = os.path.join(project_folder, "CSV_Data")
        scratch_folder = os.path.join(project_folder, "Scratch")
        scratch_workspace = os.path.join(project_folder, "Scratch\\scratch.gdb")

        # Set basic workkpace variables
        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"

        aprx = arcpy.mp.ArcGISProject(rf"{project_folder}\{project_name}.aprx")

        del scratch_folder, scratch_workspace

        arcpy.AddMessage("Loading the Dataset Title Dictionary. Please wait")

        datasets_dict = dataset_title_dict(project_folder)

        datasets = []

        # datasets.extend(arcpy.ListFeatureClasses("AI_IDW_Sample_Locations"))
        # datasets.extend(arcpy.ListFeatureClasses("*Sample_Locations"))
        # datasets.extend(arcpy.ListFeatureClasses("DisMAP_Regions"))
        datasets.extend(arcpy.ListTables("Indicators"))
        # datasets.extend(arcpy.ListTables("Species_Filter"))
        # datasets.extend(arcpy.ListTables("DisMAP_Survey_Info"))
        # datasets.extend(arcpy.ListTables("SpatialGroup_SpeciesPersistenceIndicator"))
        # datasets.extend(arcpy.ListTables("SpeciesPersistenceIndicatorPercentileBin"))
        # datasets.extend(arcpy.ListTables("SpeciesPersistenceIndicatorTrend"))


        for dataset in sorted(datasets):

            feature_service_title = datasets_dict[dataset]["Dataset Service Title"]

            arcpy.AddMessage(f"Dataset: {dataset}")
            arcpy.AddMessage(f"\tTitle: {feature_service_title}")

            desc = arcpy.da.Describe(dataset)

            feature_class_path = rf"{project_gdb}\{dataset}"

            if desc["dataType"] == "FeatureClass":

                arcpy.AddMessage("\tMake Feature Layer")
                feature_class_layer = arcpy.management.MakeFeatureLayer(feature_class_path, feature_service_title)

                feature_class_layer_file = (rf"{project_folder}\Layers\{feature_class_layer}.lyrx")

                arcpy.AddMessage("\tSave Layer File")
                _result = arcpy.management.SaveToLayerFile(in_layer = feature_class_layer, out_layer = feature_class_layer_file, is_relative_path = "RELATIVE", version="CURRENT",)
                del _result

                arcpy.management.Delete(feature_class_layer)
                del feature_class_layer

                # Test if time field exists
                if [f.name for f in arcpy.ListFields(feature_class_path) if f.name == "StdTime"]:
                    arcpy.AddMessage("\tSet Time Enabled if time field is in dataset")
                    # Get time information from a layer in a layer file
                    layer_file = arcpy.mp.LayerFile(feature_class_layer_file)
                    layer = layer_file.listLayers()[0]
                    layer.enableTime("StdTime", "StdTime", True)
                    layer.time.timeZone = arcpy.mp.ListTimeZones("(UTC) Coordinated Universal Time")[0]
                    layer_file.save()
                    del layer

                    for layer in layer_file.listLayers():
                        if layer.supports("TIME"):
                            if layer.isTimeEnabled:
                                lyrTime = layer.time
                                startTime = lyrTime.startTime
                                endTime = lyrTime.endTime
                                timeDelta = endTime - startTime
                                startTimeField = lyrTime.startTimeField
                                endTimeField = lyrTime.endTimeField
                                arcpy.AddMessage(f"\tLayer: {layer.name}")
                                arcpy.AddMessage(f"\t\tStart Time Field: {startTimeField}")
                                arcpy.AddMessage(f"\t\tEnd Time Field: {endTimeField}")
                                arcpy.AddMessage(
                                    f"\t\tStart Time: {str(startTime.strftime('%m-%d-%Y'))}"
                                )
                                arcpy.AddMessage(
                                    f"\t\tEnd Time:   {str(endTime.strftime('%m-%d-%Y'))}"
                                )
                                arcpy.AddMessage(
                                    f"\t\tTime Extent: {str(timeDelta.days)} days"
                                )
                                arcpy.AddMessage(
                                    f"\t\tTime Zone:   {str(layer.time.timeZone)}"
                                )
                                del lyrTime, startTime, endTime, timeDelta
                                del startTimeField, endTimeField
                            else:
                                arcpy.AddMessage(
                                    "No time properties have been set on the layer"
                                )
                        else:
                            arcpy.AddMessage("Time is not supported on this layer")
                        del layer
                    del layer_file
                else:
                    arcpy.AddMessage("\tDataset does not have a time field")

                del feature_class_layer_file

            elif desc["dataType"] == "Table":

                arcpy.AddMessage("\tMake Table View")
                table_view_layer = arcpy.management.MakeTableView(in_table=feature_class_path, out_view=feature_service_title,)
                table_view_layer_file = rf"{project_folder}\Layers\{table_view_layer}.lyrx"

                arcpy.AddMessage("\tSave Layer File")
                arcpy.management.SaveToLayerFile(in_layer = table_view_layer, out_layer = table_view_layer_file, is_relative_path = "RELATIVE", version = "CURRENT",)

                arcpy.management.Delete(table_view_layer)
                del table_view_layer

            elif desc["dataType"] == "RasterDataset":
                arcpy.AddMessage("\tRaster Dataset")


            elif desc["dataType"] == "MosaicDataset":
                arcpy.AddMessage("\tMosaic Dataset")

            else:
                pass


##            # aprx.listBasemaps() to get a list of available basemaps
##            #
##            #    ['Charted Territory Map',
##            #     'Colored Pencil Map',
##            #     'Community Map',
##            #     'Dark Gray Canvas',
##            #     'Firefly Imagery Hybrid',
##            #     'GEBCO Basemap (NOAA NCEI Visualization)',
##            #     'GEBCO Basemap/Contours (NOAA NCEI Visualization)',
##            #     'GEBCO Gray Basemap (NOAA NCEI Visualization)',
##            #     'GEBCO Gray Basemap/Contours (NOAA NCEI Visualization)',
##            #     'Human Geography Dark Map',
##            #     'Human Geography Map',
##            #     'Imagery',
##            #     'Imagery Hybrid',
##            #     'Light Gray Canvas',
##            #     'Mid-Century Map',
##            #     'Modern Antique Map',
##            #     'National Geographic Style Map',
##            #     'Navigation',
##            #     'Navigation (Dark)',
##            #     'Newspaper Map',
##            #     'NOAA Charts',
##            #     'NOAA ENC® Charts',
##            #     'Nova Map',
##            #     'Oceans',
##            #     'OpenStreetMap',
##            #     'Streets',
##            #     'Streets (Night)',
##            #     'Terrain with Labels',
##            #     'Topographic']
##
##            if aprx.listMaps(feature_service_title):
##                aprx.deleteItem(aprx.listMaps(feature_service_title)[0])
##                aprx.save()
##            else:
##                pass
##
##            arcpy.AddMessage(f"\tCreating Map: {feature_service_title}")
##            aprx.createMap(f"{feature_service_title}", "Map")
##            aprx.save()
##
##            current_map = aprx.listMaps(feature_service_title)[0]
##
##            basemap = "Terrain with Labels"
##            current_map.addLayer(layer_file)
##            current_map.addBasemap(basemap)
##            aprx.save()
##            del basemap
##
##            arcpy.AddMessage("\t\tCreate map thumbnail and update metadata")
##            current_map_view = current_map.defaultView
##            current_map_view.exportToPNG(
##                rf"{project_folder}\Layers\{feature_service_title}.png",
##                width=288,
##                height=192,
##                resolution=96,
##                color_mode="24-BIT_TRUE_COLOR",
##                embed_color_profile=True,
##            )
##            del current_map_view
##
##            fc_md = md.Metadata(feature_class_path)
##            #fc_md.title = feature_service_title
##            arcpy.AddMessage("*" * 50)
##            arcpy.AddMessage(fc_md.title)
##            arcpy.AddMessage("*" * 50)
##            if not fc_md.thumbnailUri:
##                fc_md.thumbnailUri = rf"{project_folder}\Layers\{feature_service_title}.png"
##            else:
##                pass
##            fc_md.save()
##            fc_md.reload()
##            fc_md.saveAsXML(
##                rf"{project_folder}\Metadata_Export\{feature_service_title}.xml"
##            )
##            del fc_md
##
##            # parse_xml_file_format_and_save(
##            #     csv_data_folder=csv_data_folder,
##            #     xml_file=rf"{project_folder}\Metadata_Export\{feature_service_title}.xml",
##            #     sort=True,
##            # )
##            # parse_xml_file_format_and_save(csv_data_folder=csv_data_folder, xml_file="", sort=True)
##
##            in_md = md.Metadata(feature_class_path)
##            layer_file.metadata.copy(in_md)
##            layer_file.metadata.save()
##            layer_file.save()
##            current_map.metadata.copy(in_md)
##            current_map.metadata.save()
##            aprx.save()
##            del in_md
##
##            arcpy.AddMessage(f"\t\tLayer File Path:     {layer_file.filePath}")
##            arcpy.AddMessage(f"\t\tLayer File Version:  {layer_file.version}")
##            arcpy.AddMessage("\t\tLayer File Metadata:")
##            arcpy.AddMessage(
##                f"\t\t\tLayer File Title:              {layer_file.metadata.title}"
##            )
##            # arcpy.AddMessage(f"\t\t\tLayer File Tags:               {layer_file.metadata.tags}")
##            # arcpy.AddMessage(f"\t\t\tLayer File Summary:            {layer_file.metadata.summary}")
##            # arcpy.AddMessage(f"\t\t\tLayer File Description:        {layer_file.metadata.description}")
##            # arcpy.AddMessage(f"\t\t\tLayer File Credits:            {layer_file.metadata.credits}")
##            # arcpy.AddMessage(f"\t\t\tLayer File Access Constraints: {layer_file.metadata.accessConstraints}")
##
##            arcpy.AddMessage("\t\tList of layers or tables in Layer File:")
##            if current_map.listLayers(feature_service_title):
##                layer = current_map.listLayers(feature_service_title)[0]
##            elif current_map.listTables(feature_service_title):
##                layer = current_map.listTables(feature_service_title)[0]
##            else:
##                arcpy.AddWarning("Something wrong")
##
##            in_md = md.Metadata(feature_class_path)
##            layer.metadata.copy(in_md)
##            layer.metadata.save()
##            layer_file.save()
##            aprx.save()
##            del in_md
##
##            arcpy.AddMessage(f"\t\t\tLayer Name: {layer.name}")
##            arcpy.AddMessage("\t\t\tLayer Metadata:")
##            arcpy.AddMessage(
##                f"\t\t\t\tLayer Title:              {layer.metadata.title}"
##            )
##            # arcpy.AddMessage(f"\t\t\t\tLayer Tags:               {layer.metadata.tags}")
##            # arcpy.AddMessage(f"\t\t\t\tLayer Summary:            {layer.metadata.summary}")
##            # arcpy.AddMessage(f"\t\t\t\tLayer Description:        {layer.metadata.description}")
##            # arcpy.AddMessage(f"\t\t\t\tLayer Credits:            {layer.metadata.credits}")
##            # arcpy.AddMessage(f"\t\t\t\tLayer Access Constraints: {layer.metadata.accessConstraints}")
##            del layer
##            del layer_file
##            del feature_class_layer_file
##            del feature_class_path
##
##            aprx.deleteItem(current_map)
##            del current_map
##            aprx.save()
##
##            # del dataset_code, point_feature_type, feature_class_name, region, season
##            # del date_code, distribution_project_code
##            # del feature_class_path
##
##            del desc
##            del feature_service_title
##            del dataset

        del datasets_dict
        del datasets

        # Declared Variables set in function
        del aprx
        del csv_data_folder, project_folder, project_name

        # Imports
        del dataset_title_dict, md

        # Function Parameters
        del project_gdb

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk


def create_feature_class_services(project_folder=""):
    try:
        # Import
        from lxml import etree
        from arcpy import metadata as md
        from dismap_tools import dataset_title_dict

        # Set basic workkpace variables
        project_name      = os.path.basename(project_folder)
        project_gdb       = os.path.join(project_folder, f"{project_name}.gdb")
        csv_data_folder   = os.path.join(project_folder, "CSV_Data")
        scratch_folder    = os.path.join(project_folder, "Scratch")
        scratch_workspace = os.path.join(project_folder, "Scratch\\scratch.gdb")

        # Set basic workkpace variables
        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"

        aprx = arcpy.mp.ArcGISProject(rf"{project_folder}\{project_name}.aprx")

        del scratch_folder, scratch_workspace

        arcpy.AddMessage("Loading the Dataset Title Dictionary. Please wait")
        datasets_dict = dataset_title_dict(project_folder)

        datasets = []

        # datasets.extend(arcpy.ListFeatureClasses("AI_IDW_Sample_Locations"))
        # datasets.extend(arcpy.ListFeatureClasses("HI_IDW_Sample_Locations"))
        # datasets.extend(arcpy.ListFeatureClasses("*Sample_Locations"))
        # datasets.extend(arcpy.ListFeatureClasses("DisMAP_Regions"))
        datasets.extend(arcpy.ListTables("Indicators"))
        # datasets.extend(arcpy.ListTables("Species_Filter"))
        # datasets.extend(arcpy.ListTables("DisMAP_Survey_Info"))
        # datasets.extend(arcpy.ListTables("SpeciesPersistenceIndicatorPercentileBin"))
        # datasets.extend(arcpy.ListTables("SpeciesPersistenceIndicatorTrend"))
        # datasets.extend(arcpy.ListTables("SpatialGroup_SpeciesPersistenceIndicator"))

        for dataset in sorted(datasets):

            feature_service = datasets_dict[dataset]["Dataset Service"]
            feature_service_title = datasets_dict[dataset]["Dataset Service Title"]

            arcpy.AddMessage(f"Dataset: {dataset}")
            arcpy.AddMessage(f"\tFS:  {feature_service}")
            arcpy.AddMessage(f"\tFST: {feature_service_title}")

            feature_class_layer_file = os.path.join(project_folder, f"Layers\\{feature_service_title}.lyrx")

            layer_file = arcpy.mp.LayerFile(feature_class_layer_file)

            # Loop through layers inside the layer file (usually contains one main layer)
            for lyr in layer_file.listLayers():
                if lyr.isFeatureLayer or lyr.isRasterLayer:
                    # Access the CIM definition (Use 'V3' for ArcGIS Pro 3.x)
                    lyr_cim = lyr.getDefinition('V3')

                    # Explicitly assign the static unique ID
                    new_id = 0
                    #lyr_cim.serviceLayerID = new_id
                    lyr_cim.serviceLayerID = new_id

                    # Push the modified CIM back to the layer
                    lyr.setDefinition(lyr_cim)

                    arcpy.AddMessage(f"Assigned ID {new_id} to layer: {lyr.name}")

            # Save the modifications back to the file
            layer_file.save()

            del feature_class_layer_file

            # aprx.listBasemaps() to get a list of available basemaps
            #
            #    ['Charted Territory Map',
            #     'Colored Pencil Map',
            #     'Community Map',
            #     'Dark Gray Canvas',
            #     'Firefly Imagery Hybrid',
            #     'GEBCO Basemap (NOAA NCEI Visualization)',
            #     'GEBCO Basemap/Contours (NOAA NCEI Visualization)',
            #     'GEBCO Gray Basemap (NOAA NCEI Visualization)',
            #     'GEBCO Gray Basemap/Contours (NOAA NCEI Visualization)',
            #     'Human Geography Dark Map',
            #     'Human Geography Map',
            #     'Imagery',
            #     'Imagery Hybrid',
            #     'Light Gray Canvas',
            #     'Mid-Century Map',
            #     'Modern Antique Map',
            #     'National Geographic Style Map',
            #     'Navigation',
            #     'Navigation (Dark)',
            #     'Newspaper Map',
            #     'NOAA Charts',
            #     'NOAA ENC® Charts',
            #     'Nova Map',
            #     'Oceans',
            #     'OpenStreetMap',
            #     'Streets',
            #     'Streets (Night)',
            #     'Terrain with Labels',
            #     'Topographic']

            if aprx.listMaps(feature_service_title):
                aprx.deleteItem(aprx.listMaps(feature_service_title)[0])
                aprx.save()
            else:
                pass

            arcpy.AddMessage(f"\tCreating Map: {feature_service_title}")
            aprx.createMap(feature_service_title, "Map")
            aprx.save()

            current_map = aprx.listMaps(feature_service_title)[0]

            map_cim = current_map.getDefinition('V3')
            map_cim.useServiceLayerIDs = True
            current_map.setDefinition(map_cim)
            del map_cim

            current_map.addLayer(layer_file)

            aprx.save()

            del layer_file

            arcpy.AddMessage("\t\tList of layers or tables in Layer File:")
            if current_map.listLayers(feature_service_title):
                lyr = current_map.listLayers(feature_service_title)[0]

            elif current_map.listTables(feature_service_title):
                lyr = current_map.listTables(feature_service_title)[0]

            else:
                arcpy.AddWarning("Something wrong")

            #lyr_md = md.Metadata(lyr)
            #arcpy.AddMessage(lyr.dataSource)
            lyr_md = md.Metadata(lyr.dataSource)

            current_map_md = md.Metadata(current_map)
            current_map_md.copy(lyr_md)
            current_map_md.save()
            aprx.save()

            del current_map_md
            del lyr_md

            arcpy.AddMessage("\tGet Web Layer Sharing Draft")
            # Get Web Layer Sharing Draft
            server_type = "HOSTING_SERVER"  # FEDERATED_SERVER
            #            m.getWebLayerSharingDraft (server_type, service_type, service_name, {layers_and_tables})
            # sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name, [selected_layer, selected_table])
            # https://pro.arcgis.com/en/pro-app/latest/arcpy/sharing/featuresharingdraft-class.htm#GUID-8E27A3ED-A705-4ACF-8C7D-AA861327AD26
            sddraft = current_map.getWebLayerSharingDraft(
                server_type=server_type,
                service_type="FEATURE",
                service_name=feature_service,
                layers_and_tables=lyr,
            )
            del server_type

            sddraft.allowExporting              = True
            sddraft.allowUpdateWithoutMValues   = True   # Default
            sddraft.approvePublicDataCollection = False
            sddraft.checkUniqueIDAssignment     = True
            # sddraft.credits                     = lyr.metadata.credits
            # sddraft.description                 = lyr.metadata.description
            sddraft.featureCapabilities         = "Query,Extract"
            sddraft.maxRecordCount              = 10000
            sddraft.offline                     = False
            sddraft.offlineTarget               = None
            sddraft.overwriteExistingService    = True
            sddraft.portalFolder                = f"DisMAP {project_name}"
            sddraft.preserveEditUsersAndTimestamps = False # Default
            # sddraft.serverType
            # sddraft.serviceName
            # sddraft.sharing.groups
            # sddraft.sharing.sharingLevel
            # sddraft.summary                  = lyr.metadata.summary
            # sddraft.tags                     = lyr.metadata.tags
            sddraft.timezone.ID                = "UTC"
            sddraft.timezone.DaylightSavingTime = True
            # sddraft.timezone.preferredTimezoneID
            # sddraft.timezone.preferredTimezoneIDDaylightSavingTime
            # sddraft.useCIMSymbols
            # sddraft.useLimitations           = lyr.metadata.accessConstraints
            # sddraft.zDefault.enable
            # sddraft.zDefault.value

            del lyr

            arcpy.AddMessage(f"\t\tAllow Exporting:                     {sddraft.allowExporting}")
            arcpy.AddMessage(f"\t\tAllow allow Update Without M Values: {sddraft.allowUpdateWithoutMValues}")
            arcpy.AddMessage(f"\t\tApprove Public Data Collection:      {sddraft.approvePublicDataCollection}")
            arcpy.AddMessage(f"\t\tCheck Unique ID Assignment:          {sddraft.checkUniqueIDAssignment}")
            arcpy.AddMessage(f"\t\tCredits:                             {sddraft.credits}")
            arcpy.AddMessage(f"\t\tDescription:                         {sddraft.description}")
            arcpy.AddMessage(f"\t\tFeature Capabilities:                {sddraft.featureCapabilities}")
            arcpy.AddMessage(f"\t\tMaxRecordCount:                      {sddraft.maxRecordCount}")
            arcpy.AddMessage(f"\t\tOffline:                             {sddraft.offline}")
            arcpy.AddMessage(f"\t\tOffline Target:                      {sddraft.offlineTarget}")
            arcpy.AddMessage(f"\t\tOverwrite Existing Service:          {sddraft.overwriteExistingService}")
            arcpy.AddMessage(f"\t\tPortal Folder:                       {sddraft.portalFolder}")
            arcpy.AddMessage(f"\t\tPreserveEditUsersAndTimestamps:      {sddraft.preserveEditUsersAndTimestamps}")
            arcpy.AddMessage(f"\t\tServer Type:                         {sddraft.serverType}")
            arcpy.AddMessage(f"\t\tService Name:                        {sddraft.serviceName}")
            arcpy.AddMessage(f"\t\tSharing Groups:                      {sddraft.sharing.groups}")
            arcpy.AddMessage(f"\t\tSharing Levek:                       {sddraft.sharing.sharingLevel}")
            arcpy.AddMessage(f"\t\tSummary:                             {sddraft.summary}")
            arcpy.AddMessage(f"\t\tTags:                                {sddraft.tags}")
            arcpy.AddMessage(f"\t\tTimezone ID:                         {sddraft.timezone.ID}")
            arcpy.AddMessage(f"\t\tTimezone Daylight Saving Time:       {sddraft.timezone.DaylightSavingTime}")
            # arcpy.AddMessage(f"\t\tPreferred Timezone ID:                   {sddraft.timezone.preferredTimezoneID}")
            # arcpy.AddMessage(f"\t\tPreferred Timezone Daylight Saving Time: {sddraft.timezone.preferredTimezoneID}")
            arcpy.AddMessage(f"\t\tUse CIM Symbols:                         {sddraft.useCIMSymbols}")
            arcpy.AddMessage(f"\t\tUse Limitations:                         {sddraft.useLimitations}")
            arcpy.AddMessage(f"\t\tZ Default Enable:                        {sddraft.zDefault.enable}")
            arcpy.AddMessage(f"\t\tZ Default Value:                         {sddraft.zDefault.value}")

            arcpy.AddMessage("\tExport to SD Draft")
            # Create Service Definition Draft file
            sd_draft = os.path.join(project_folder, f"Publish\\{feature_service}.sddraft")

            sddraft.exportToSDDraft(sd_draft)

            etree.parse(sd_draft, parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)).write(sd_draft, pretty_print=True, xml_declaration=True, encoding="UTF-8")

            del sddraft

##            arcpy.AddMessage("\tModify SD Draft")
##            # https://pro.arcgis.com/en/pro-app/latest/arcpy/sharing/featuresharingdraft-class.htm
##            # https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/streamline-your-code-with-new-properties-in-arcpy-sharing
##            import xml.dom.minidom as DOM
##
##            docs = DOM.parse(sd_draft)
##            key_list = docs.getElementsByTagName("Key")
##            value_list = docs.getElementsByTagName("Value")
##
##            for i in range(key_list.length):
##                if key_list[i].firstChild.nodeValue == "maxRecordCount":
##                    arcpy.AddMessage("\t\tUpdating maxRecordCount from 2000 to 10000")
##                    value_list[i].firstChild.nodeValue = 2000
##                if key_list[i].firstChild.nodeValue == "ServiceTitle":
##                    arcpy.AddMessage(
##                        f"\t\tUpdating ServiceTitle from {value_list[i].firstChild.nodeValue} to {feature_service_title}"
##                    )
##                    value_list[i].firstChild.nodeValue = feature_service_title
##                # Doesn't work
##                # if key_list[i].firstChild.nodeValue == "GeodataServiceName":
##                #    arcpy.AddMessage(f"\t\tUpdating GeodataServiceName from {value_list[i].firstChild.nodeValue} to {feature_service}")
##                #    value_list[i].firstChild.nodeValue = feature_service
##                del i
##
##            # Write to the .sddraft file
##            f = open(sd_draft, "w")
##            docs.writexml(f)
##            f.close()
##            del f
##
##            del DOM, docs, key_list, value_list

            FeatureSharingDraftReport = False
            if FeatureSharingDraftReport:
                arcpy.AddMessage(f"\tReport for {os.path.basename(sd_draft)} SD File")
                feature_sharing_draft_report(sd_draft)
            del FeatureSharingDraftReport

            StageService = True
            if StageService:
                arcpy.AddMessage(f"\tCreate/Stage {os.path.basename(sd_draft)} SD File")
                arcpy.server.StageService(
                    in_service_definition_draft=sd_draft,
                    out_service_definition=sd_draft.replace("sddraft", "sd"),
                    staging_version=5,
                )
            del StageService

            UploadServiceDefinition = True
            if UploadServiceDefinition:
                arcpy.AddMessage(f"\tUpload {os.path.basename(sd_draft).replace('sddraft', 'sd')} Service Definition")
                arcpy.server.UploadServiceDefinition(
                    in_sd_file=sd_draft.replace("sddraft", "sd"),
                    in_server           = "HOSTING_SERVER",  # in_service_name = "", #in_cluster      = "",
                    in_folder_type      = "FROM_SERVICE_DEFINITION",  # EXISTING #in_folder       = "",
                    in_startupType      = "STARTED",
                    in_override         = "OVERRIDE_DEFINITION",
                    in_my_contents      = "NO_SHARE_ONLINE",
                    in_public           = "PRIVATE",
                    in_organization     = "NO_SHARE_ORGANIZATION",  # in_groups       = ""
                )

            del UploadServiceDefinition

            del sd_draft

            # aprx.deleteItem(current_map)
            del current_map
            aprx.save()

            del feature_service, feature_service_title
            del dataset
        del datasets
        del datasets_dict

        # TODO: Possibly create a dictionary that can be saved to JSON

        aprx.save()

        current_maps = aprx.listMaps()

        if current_maps:
            arcpy.AddMessage("\nCurrent Maps\n")
            for current_map in current_maps:
                arcpy.AddMessage(f"\tProject Map: {current_map.name}")
                del current_map
        else:
            arcpy.AddWarning("No maps in Project")

        del current_maps

        # Declared Variables set in function for aprx

        # Save aprx one more time and then delete
        aprx.save()
        del aprx

        # Declared Variables set in function
        del project_folder, project_name, csv_data_folder

        # Imports
        del dataset_title_dict, md, etree

        # Function Parameters
        del project_gdb

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk
    finally:
        pass

##def update_metadata_from_published_md(project_gdb=""):
##    try:
##        # Import
##        import dismap_tools
##
##        arcpy.env.overwriteOutput = True
##        arcpy.env.parallelProcessingFactor = "100%"
##        arcpy.SetLogMetadata(True)
##        arcpy.SetSeverityLevel(2)
##        arcpy.SetMessageLevels(['NORMAL']) # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION
##
##        LogInAGOL = False
##        if LogInAGOL:
##            try:
##                portal = "https://noaa.maps.arcgis.com/"
##                user = "John.F.Kennedy_noaa"
##
##                # Sign in to portal
##                #arcpy.SignInToPortal("https://www.arcgis.com", "MyUserName", "MyPassword")
##                # For example: 'http://www.arcgis.com/'
##                arcpy.SignInToPortal(portal)
##
##                arcpy.AddMessage(f"###---> Signed into Portal: {arcpy.GetActivePortalURL()} <---###")
##                del portal, user
##            except:
##                arcpy.AddError(f"###---> Signed into Portal faild <---###")
##        del LogInAGOL
##
##        aprx = arcpy.mp.ArcGISProject(base_project_file)
##        home_folder = aprx.homeFolder
##        del aprx
##
##        project_gdb = rf"{project_folder}\{project}.gdb"
##
##
##
##        # DatasetCode, CSVFile, TransformUnit, TableName, GeographicArea, CellSize,
##        # PointFeatureType, FeatureClassName, Region, Season, DateCode, Status,
##        # DistributionProjectCode, DistributionProjectName, SummaryProduct,
##        # FilterRegion, FilterSubRegion, FeatureServiceName, FeatureServiceTitle,
##        # MosaicName, MosaicTitle, ImageServiceName, ImageServiceTitle
##
##        # Get values for table_name from Datasets table
##        #fields = ["FeatureClassName", "FeatureServiceName", "FeatureServiceTitle"]
##        fields = ["DatasetCode", "PointFeatureType", "FeatureClassName", "Region", "Season", "DateCode", "DistributionProjectCode"]
##        datasets = [row for row in arcpy.da.SearchCursor(os.path.join(project_gdb, "Datasets"), fields, where_clause = f"FeatureClassName IS NOT NULL AND DistributionProjectCode NOT IN ('GLMME', 'GFDL')")]
##        #datasets = [row for row in arcpy.da.SearchCursor(os.path.join(project_gdb, "Datasets"), fields, where_clause = f"FeatureClassName IN ('AI_IDW_Sample_Locations', 'DisMAP_Regions')")]
##        del fields
##
##        for dataset in datasets:
##            dataset_code, point_feature_type, feature_class_name, region_latitude, season, date_code, distribution_project_code = dataset
##
##            feature_service_name  = f"{dataset_code}_{point_feature_type}_{date_code}".replace("None", "").replace(" ", "_").replace("__", "_")
##
##            if distribution_project_code == "IDW":
##                feature_service_title = f"{region_latitude} {season} {point_feature_type} {date_code}".replace("None", "").replace("  ", " ")
##            #elif distribution_project_code in ["GLMME", "GFDL"]:
##            #    feature_service_title = f"{region_latitude} {distribution_project_code} {point_feature_type} {date_code}".replace("None", "").replace("  ", " ")
##            else:
##                feature_service_title = f"{feature_service_name}".replace("_", " ")
##
##            map_title = feature_service_title.replace("GRID Points", "").replace("Sample Locations", "").replace("  ", " ")
##
##            feature_class_path = f"{project_gdb}\{feature_class_name}"
##
##            arcpy.AddMessage(f"Dataset Code: {dataset_code}")
##            arcpy.AddMessage(f"\tFeature Service Name:   {feature_service_name}")
##            arcpy.AddMessage(f"\tFeature Service Title:  {feature_service_title}")
##            arcpy.AddMessage(f"\tMap Title:              {map_title}")
##            arcpy.AddMessage(f"\tLayer Title:            {feature_service_title}")
##            arcpy.AddMessage(f"\tFeature Class Name:     {feature_class_name}")
##            arcpy.AddMessage(f"\tFeature Class Path:     {feature_class_path}")
##
##            if arcpy.Exists(rf"{project_folder}\Publish\{feature_service_name}.xml"):
##                arcpy.AddMessage(f"\t###--->>> {feature_service_name}.xml Exists <<<---###")
##
##                from arcpy import metadata as md
##                in_md = md.Metadata(rf"{project_folder}\Publish\{feature_service_name}.xml")
##                fc_md = md.Metadata(feature_class_path)
##                fc_md.copy(in_md)
##                fc_md.save()
##                del in_md, fc_md
##                del md
##
##            else:
##                arcpy.AddWarning(f"\t###--->>> {feature_service_name}.xml Does Not Exist <<<---###")
##
##            del dataset_code, point_feature_type, feature_class_name, region_latitude, season
##            del date_code, distribution_project_code
##
##            del feature_service_name, feature_service_title
##            del map_title, feature_class_path
##            del dataset
##        del datasets
##
##        arcpy.AddMessage(f"\n{'-' * 90}\n")
##
##        # Declared Variables set in function
##        del project_gdb
##        del home_folder
##
##        # Imports
##        del dismap
##
##        # Function Parameters
##        del base_project_file, project
##
##    except arcpy.ExecuteWarning:
##        arcpy.AddWarning(
##            f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}"
##        )
##    except arcpy.ExecuteError:
##        arcpy.AddError(
##            f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}"
##        )
##        arcpy.AddError("Traceback:\n")
##        traceback.print_exc()
##    except SystemExit:
##        # This is not an error, so we allow the script to exit.
##        pass
##    except Exception as e:
##        arcpy.AddError(
##            f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}"
##        )
##        arcpy.AddError("Traceback:")
##        traceback.print_exc()
##    else:
##        # While in development, leave here. For test, move to finally
##        rk = [key for key in locals().keys() if not key.startswith("__")]
##        if rk:
##            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
##        del rk
##    finally:
##        pass

def create_image_services(project_folder=""):
    try:
        # Import
        from lxml import etree
        from arcpy import metadata as md
        from dismap_tools import dataset_title_dict, date_code, import_metadata

        # Set basic workkpace variables
        project_name      = os.path.basename(project_folder)
        project_gdb       = os.path.join(project_folder, f"{project_name}.gdb")
        crfs_folder       = os.path.join(project_folder, "CRFs")
        scratch_folder    = os.path.join(project_folder, "Scratch")
        scratch_workspace = os.path.join(project_folder, "Scratch\\scratch.gdb")

        # Set basic workkpace variables
        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"

        #aprx = arcpy.mp.ArcGISProject(rf"{project_folder}\{project_name}.aprx")

        del scratch_folder, scratch_workspace

        arcpy.AddMessage("Loading the Dataset Title Dictionary. Please wait")
        datasets_dict = dataset_title_dict(project_folder)

        arcpy.env.workspace = crfs_folder

        #print(arcpy.ListRasters("*"))

        #for crf in sorted(arcpy.ListRasters("*")):
        #for crf in sorted([c for c in arcpy.ListRasters("*") if c.startswith("HI")]):
        for crf in sorted([c for c in arcpy.ListRasters("*") if c in ["NEUS_FAL_IDW_CRF.crf", "NEUS_SPR_IDW_CRF.crf", "SEUS_FAL_IDW_CRF.crf", "SEUS_SPR_IDW_CRF.crf", "SEUS_SUM_IDW_CRF.crf", "WC_ANN_IDW_CRF.crf", "WC_TRI_IDW_CRF.crf"]]):
            feature_service = datasets_dict[crf.replace(".crf", "")]["Dataset Service"].replace("_CRF", "")
            feature_service_title = datasets_dict[crf.replace(".crf", "")]["Dataset Service Title"]

            source_path = os.path.join(crfs_folder, crf)

            arcpy.AddMessage(f"Dataset: {crf}")
            arcpy.AddMessage(f"\tFS:  {feature_service}")
            arcpy.AddMessage(f"\tFST: {feature_service_title}")

            # Add boilerplate metadata to dataset
            # Version Code
            version_code = date_code(project_name)
            # Boilerplate
            # contacts = rf"{home_folder}\Initial-Data\DisMAP-Contacts-{version_code}.xml"
            crf_metadata_template = os.path.join(project_folder, "Metadata_ArcGIS\\Fish and Invertebrate Interpolated Biomass Distribution Surfaces 20260601.xml")

            # Reads XML, pretty format, and write back the crf_metadata_template XML
            etree.parse(crf_metadata_template, parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)).write(crf_metadata_template, pretty_print=True, xml_declaration=True, encoding="UTF-8") # pyright: ignore[reportAttributeAccessIssue]

            # Create Metadata object for new table
            crf_metadata_template_md = md.Metadata(crf_metadata_template)
            dataset_md = md.Metadata(source_path)
            dataset_md.copy(crf_metadata_template_md)
            dataset_md.save()
            dataset_md.synchronize("ACCESSED")
            dataset_md.save()
            dataset_md.title = feature_service_title
            print(dataset_md.title)
            dataset_md.save()
            del dataset_md
            del crf_metadata_template, crf_metadata_template_md

            sddraft_filename = feature_service + ".sddraft"
            sddraft_output_filename = os.path.join(project_folder, "Publish", sddraft_filename)
            sd_filename = feature_service + ".sd"
            sd_output_filename = os.path.join(project_folder, "Publish", sd_filename)

            # Create ImageSharingDraft and set metadata, portal folder, and server folder properties
            federated_server_url = "https://maps.fisheries.noaa.gov/image"
            sddraft = arcpy.sharing.CreateSharingDraft(server_type  = "FEDERATED_SERVER",
                                                       service_type = "WEB_IMAGERY_LAYER",
                                                       service_name = feature_service,
                                                       draft_value  = source_path)

            sddraft.targetServer         = federated_server_url
##            sddraft.credits              = "These are credits"
##            sddraft.description          = "This is description"
##            sddraft.summary              = "This is summary"
##            sddraft.tags                 = "tag1, tag2"
##            sddraft.useLimitations       = "These are use limitations"
            sddraft.portalFolder         = "DisMAP June 1 2026"
            sddraft.serverFolder         = "DisMAP"
            sddraft.sharing.sharingLevel = "EVERYONE"
            sddraft.sharing.groups       = ""  # Group names = "group1,group2"
            sddraft.allowAnalysis        = True
            sddraft.allowedItemMetadata  = "Full"
            sddraft.overwriteExistingService = True

            # Create Service Definition Draft file

            sddraft.exportToSDDraft(sddraft_output_filename)

            # Stage Service
            arcpy.AddMessage("Start Staging")
            arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

            # Share to portal
            arcpy.AddMessage("Start Uploading")
            arcpy.server.UploadServiceDefinition(sd_output_filename, federated_server_url)

            arcpy.AddMessage("Finish Publishing")

            del feature_service, feature_service_title, version_code
            del sddraft_filename, sddraft_output_filename, sd_filename
            del sd_output_filename, federated_server_url
            del sddraft
            del source_path
            del crf

        # del project_gdb

        # Declared Variables set in function for aprx
        # del home_folder
        # Save aprx one more time and then delete
        # aprx.save()
        # del aprx

        # Declared Variables set in function
        del project_folder, project_name, crfs_folder, datasets_dict

        # Imports
        del etree, md
        del dataset_title_dict, date_code, import_metadata

        # Function Parameters
        del project_gdb

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk
    finally:
        pass


def create_thumbnails(project_folder=""):
    try:
        # Import
        from arcpy import metadata as md
        from dismap_tools import dataset_title_dict

        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"

        home_folder      = os.path.dirname(project_folder)
        home_folder_file = os.path.join(home_folder, "DisMAP.aprx")
        project_name     = os.path.basename(project_folder)
        project_gdb      = os.path.join(project_folder, f"{project_name}.gdb")
        metadata_folder  = os.path.join(project_folder, "Metadata_Export")
        scratch_folder   = os.path.join(project_folder, "Scratch")

        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = os.path.join(scratch_folder, "scratch.gdb")

        aprx = arcpy.mp.ArcGISProject(home_folder_file)

        # arcpy.AddMessage(f"\n{'-' * 90}\n")

        metadata_dictionary = dataset_title_dict(project_folder)

        datasets = list()

        walk = arcpy.da.Walk(project_gdb)

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                datasets.append(os.path.join(dirpath, filename))
                del filename
            del dirpath, dirnames, filenames
        del walk

        for dataset_path in sorted(datasets):
            arcpy.AddMessage(dataset_path)
            dataset_name = os.path.basename(dataset_path)
            data_type = arcpy.Describe(dataset_path).dataType
            arcpy.AddMessage(f"Dataset Name: {dataset_name}")
            arcpy.AddMessage(f"\tData Type: {data_type}")

            if data_type == "Table":


                if "IDW" in dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if "Indicators" in dataset_name:
                        arcpy.AddMessage("\tRegion Indicators")

                    elif "LayerSpeciesYearImageName" in dataset_name:
                        arcpy.AddMessage("\tRegion Layer Species Year Image Name")

                    else:
                        arcpy.AddMessage("\tRegion Table")

                else:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if "Indicators" in dataset_name:
                        arcpy.AddMessage("\tMain Indicators Table")

                    elif "LayerSpeciesYearImageName" in dataset_name:
                        arcpy.AddMessage("\tLayer Species Year Image Name")

                    elif "Datasets" in dataset_name:
                        arcpy.AddMessage("\tDataset Table")

                    elif "Species_Filter" in dataset_name:
                        arcpy.AddMessage("\tSpecies Filter Table")

                    else:
                        arcpy.AddMessage(f"\tDataset Name: {dataset_name}")

            elif data_type == "FeatureClass":
                # arcpy.AddMessage(f"\tData Type: {data_type}")

                if "IDW" in dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if dataset_name.endswith("Boundary"):
                        arcpy.AddMessage("\tBoundary")

                    elif dataset_name.endswith("Extent_Points"):
                        arcpy.AddMessage("\tExtent_Points")

                    elif dataset_name.endswith("Fishnet"):
                        arcpy.AddMessage("\tFishnet")

                    elif dataset_name.endswith("Lat_Long"):
                        arcpy.AddMessage("\tLat_Long")

                    elif dataset_name.endswith("Region"):
                        arcpy.AddMessage("\tRegion")

                    elif dataset_name.endswith("Sample_Locations"):
                        arcpy.AddMessage("\tSample_Locations")

                    else:
                        pass

                elif "DisMAP_Regions" == dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if dataset_name.endswith("Regions"):
                        arcpy.AddMessage("\tDisMAP Regions")

                else:
                    arcpy.AddMessage(f"Else Dataset Name: {dataset_name}")

            elif data_type == "RasterDataset":

                if "IDW" in dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if dataset_name.endswith("Bathymetry"):
                        arcpy.AddMessage("\tBathymetry")

                    elif dataset_name.endswith("Latitude"):
                        arcpy.AddMessage("\tLatitude")

                    elif dataset_name.endswith("Longitude"):
                        arcpy.AddMessage("\tLongitude")

                    elif dataset_name.endswith("Raster_Mask"):
                        arcpy.AddMessage("\tRaster_Mask")
                else:
                    pass

            elif data_type == "MosaicDataset":

                if "IDW" in dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if dataset_name.endswith("Mosaic"):
                        arcpy.AddMessage("\tMosaic")
                    else:
                        pass

                elif "CRF" in dataset_name:
                    arcpy.AddMessage(f"Dataset Name: {dataset_name}")
                    if dataset_name.endswith("CRF"):
                        arcpy.AddMessage("\tCRF")

                else:
                    pass
            else:
                pass

            del data_type

            del dataset_name, dataset_path
        del datasets

        # Declared Variables set in function for aprx
        del home_folder
        # Save aprx one more time and then delete
        aprx.save()
        del aprx

        # Declared Variables set in function
        del metadata_folder
        del project_folder, scratch_folder
        del metadata_dictionary

        # Imports
        del dataset_title_dict, md

        # Function Parameters
        del project_gdb

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk
    finally:
        pass


def script_tool(project_folder=""):
    try:
        from time import gmtime, localtime, strftime, time

        # Set a start time so that we can see how log things take
        start_time = time()
        arcpy.AddMessage(f"{'-' * 80}")
        arcpy.AddMessage(f"Python Script:  {os.path.basename(__file__)}")
        arcpy.AddMessage(f"Location:       .. {'/'.join(__file__.split(os.sep)[-4:])}")
        arcpy.AddMessage(f"Python Version: {sys.version}")
        arcpy.AddMessage(f"Environment:    {os.path.basename(sys.exec_prefix)}")
        arcpy.AddMessage(f"Start Time:     {strftime('%a %b %d %I:%M %p', localtime(start_time))}")
        arcpy.AddMessage(f"{'-' * 80}\n")

        CreateFeatureClassLayers = False
        if CreateFeatureClassLayers:
            create_feature_class_layers(project_folder)
        del CreateFeatureClassLayers

        CreateFeaturClasseServices = False
        if CreateFeaturClasseServices:
            create_feature_class_services(project_folder)
        del CreateFeaturClasseServices

        CreateImagesServices = False
        if CreateImagesServices:
            create_image_services(project_folder)
        del CreateImagesServices

        # UpdateMetadataFromPublishedMd = False
        # if UpdateMetadataFromPublishedMd:
        #    update_metadata_from_published_md(project_folder)
        # del UpdateMetadataFromPublishedMd

##        CreateThumbnails = False
##        if CreateThumbnails:
##            create_thumbnails(project_folder)
##        del CreateThumbnails

    ##            CreateBasicTemplateXMLFiles = False
    ##            if CreateBasicTemplateXMLFiles:
    ##                create_basic_template_xml_files(project_folder)
    ##            del CreateBasicTemplateXMLFiles
    ##
    ##            ImportBasicTemplateXmlFiles = False
    ##            if ImportBasicTemplateXmlFiles:
    ##                import_basic_template_xml_files(project_folder)
    ##            del ImportBasicTemplateXmlFiles

        # Variable created in function

        # Function Parameters
        del project_folder

        # Elapsed time
        end_time = time()
        elapse_time = end_time - start_time
        hours, rem = divmod(end_time - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        arcpy.AddMessage(f"\n{'-' * 80}")
        arcpy.AddMessage(f"Python script: {os.path.basename(__file__)}")
        arcpy.AddMessage(f"Start Time:    {strftime('%a %b %d %I:%M %p', localtime(start_time))}")
        arcpy.AddMessage(f"End Time:      {strftime('%a %b %d %I:%M %p', localtime(end_time))}")
        arcpy.AddMessage(f"Elapsed Time   {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f} (H:M:S)")
        arcpy.AddMessage(f"{'-' * 80}")
        del hours, rem, minutes, seconds
        del elapse_time, end_time, start_time
        del gmtime, localtime, strftime, time

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}")
    except arcpy.ExecuteError:
        arcpy.AddError(f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}")
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}")
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##")
        del rk
    finally:
        arcpy.AddMessage(f"{'--End' * 10}--")


if __name__ == "__main__":
    try:

        project_folder = arcpy.GetParameterAsText(0)
        if not project_folder:
            # project_name = "February-1-2026"
            # project_name = "August-1-2025"
            project_name = "June-1-2026"
            project_folder = os.path.join(os.path.expanduser('~'), f"Documents\\ArcGIS\\Projects\\DisMAP\\ArcGIS-Analysis-Python\\{project_name}")
            del project_name
        else:
            pass

        script_tool(project_folder)

        arcpy.SetParameterAsText(1, "Result")

        del project_folder

    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
    except Exception:
        traceback.print_exc()
    else:
        pass

# This is an autogenerated comment.
