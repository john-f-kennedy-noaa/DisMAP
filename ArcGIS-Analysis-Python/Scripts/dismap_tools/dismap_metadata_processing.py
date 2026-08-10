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
import importlib
import inspect
import os
import sys
import traceback

import arcpy  # third-parties second

#sys.path.append(os.path.dirname(__file__))

def create_maps(base_project_file="", project="", dataset=""):
    try:
        # Import
        import dismap
        from arcpy import metadata as md

        importlib.reload(dismap)
        from dismap import parse_xml_file_format_and_save

        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(2)
        arcpy.SetMessageLevels(["NORMAL"])  # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        base_project_folder = rf"{os.path.dirname(base_project_file)}"
        base_project_file   = rf"{base_project_folder}\DisMAP.aprx"
        project_folder      = rf"{base_project_folder}\{project}"
        project_gdb         = rf"{project_folder}\{project}.gdb"
        metadata_folder     = rf"{project_folder}\Export Metadata"
        crfs_folder         = rf"{project_folder}\CRFs"
        scratch_folder      = rf"{project_folder}\Scratch"

        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = rf"{scratch_folder}\scratch.gdb"

        aprx = arcpy.mp.ArcGISProject(base_project_file)

        dataset_name = os.path.basename(dataset)

        print(f"Dataset Name: {dataset_name}")

        if dataset_name not in [cm.name for cm in aprx.listMaps()]:
            print(f"Creating Map: {dataset_name}")
            aprx.createMap(f"{dataset_name}", "Map")
            aprx.save()
        else:
            pass

        current_map = aprx.listMaps(f"{dataset_name}")[0]
        print(f"Current Map:  {current_map.name}")

        if dataset_name not in [lyr.name for lyr in current_map.listLayers(f"{dataset_name}")]:
            print(f"Adding {dataset_name} to Map")

            map_layer = arcpy.management.MakeFeatureLayer(dataset, f"{dataset_name}")

            # arcpy.management.Delete(rf"{project_folder}\Layers\{dataset_name}.lyrx")
            # os.remove(rf"{project_folder}\Layers\{dataset_name}.lyrx")

            map_layer_file = arcpy.management.SaveToLayerFile(map_layer, rf"{project_folder}\Layers\{dataset_name}.lyrx")
            del map_layer_file

            map_layer_file = arcpy.mp.LayerFile(rf"{project_folder}\Layers\{dataset_name}.lyrx")

            arcpy.management.Delete(map_layer)
            del map_layer

            current_map.addLayer(map_layer_file)
            del map_layer_file

            aprx.save()
        else:
            pass

        # aprx_basemaps = aprx.listBasemaps()
        # basemap = 'GEBCO Basemap/Contours (NOAA NCEI Visualization)'
        basemap = "Terrain with Labels"

        current_map.addBasemap(basemap)
        del basemap

        # Set Reference Scale
        current_map.referenceScale = 50000000

        # Clear Selection
        current_map.clearSelection()

        current_map_cim = current_map.getDefinition("V3")
        current_map_cim.enableWraparound = True
        current_map.setDefinition(current_map_cim)
##
##        # Return the layer's CIM definition
##        cim_lyr = lyr.getDefinition("V3")
##
##        # Modify the color, width and dash template for the SolidStroke layer
##        symLvl1 = cim_lyr.renderer.symbol.symbol.symbolLayers[0]
##        symLvl1.color.values = [0, 0, 0, 100]
##        symLvl1.width = 1
##
##        # Push the changes back to the layer object
##        lyr.setDefinition(cim_lyr)
##        del symLvl1, cim_lyr

        aprx.save()

        height = (arcpy.Describe(dataset).extent.YMax - arcpy.Describe(dataset).extent.YMin)
        width = (arcpy.Describe(dataset).extent.XMax - arcpy.Describe(dataset).extent.XMin)

        # map_width, map_height
        map_width, map_height = 8.5, 11

        if height > width:
            page_height = map_height
            page_width = map_width
        elif height < width:
            page_height = map_width
            page_width = map_height
        else:
            page_width = map_width
            page_height = map_height

        del map_width, map_height
        del height, width

        if dataset_name not in [cl.name for cl in aprx.listLayouts()]:
            print(f"Creating Layout: {dataset_name}")
            aprx.createLayout(page_width, page_height, "INCH", f"{dataset_name}")
            aprx.save()
        else:
            print(f"Layout: {dataset_name} exists")

        # Set the default map camera to the extent of the park boundary before opening the new view
        # default camera only affects newly opened views
        lyr = current_map.listLayers(f"{dataset_name}")[-1]

        #
        arcpy.management.SelectLayerByAttribute(lyr, "NEW_SELECTION", "DatasetCode in ('ENBS', 'HI', 'NEUS_SPR')")

        mv = current_map.openView()
        mv.panToExtent(mv.getLayerExtent(lyr, True, True))
        mv.zoomToAllLayers()
        del mv

        arcpy.management.SelectLayerByAttribute(lyr, "CLEAR_SELECTION")

        av = aprx.activeView
        av.exportToPNG(os.path.join(project_folder, f"Layers\\{dataset_name}.png"),
            width=288,
            height=192,
            resolution=96,
            color_mode="24-BIT_TRUE_COLOR",
            embed_color_profile=True,
            )
        av.exportToJPEG(os.path.join(project_folder, f"Layers\\{dataset_name}.jpg"),
            width=288,
            height=192,
            resolution=96,
            jpeg_color_mode="24-BIT_TRUE_COLOR",
            embed_color_profile=True,
            )
        del av

        # print(current_map.referenceScale)

        # export the newly opened active view to PDF, then delete the new map
        # mv = aprx.activeView
        # mv.exportToPDF(r"C:\Temp\RangerStations.pdf", width=700, height=500, resolution=96)
        # aprx.deleteItem(current_map)

        # mv = aprx.activeView
        # mv = current_map.defaultView
        # mv.zoomToAllLayers()
        # print(mv.camera.getExtent())
        # arcpy.management.Delete(rf"{project_folder}\Layers\{dataset_name}.png")
        # arcpy.management.Delete(rf"{project_folder}\Layers\{dataset_name}.jpg")

        # os.remove(rf"{project_folder}\Layers\{dataset_name}.png")
        # os.remove(rf"{project_folder}\Layers\{dataset_name}.jpg")

        # mv.exportToPNG(rf"{project_folder}\Layers\{dataset_name}.png", width=288, height=192, resolution = 96, color_mode="24-BIT_TRUE_COLOR", embed_color_profile=True)
        # mv.exportToJPEG(rf"{project_folder}\Layers\{dataset_name}.jpg", width=288, height=192, resolution = 96, jpeg_color_mode="24-BIT_TRUE_COLOR", embed_color_profile=True)
        # del mv

        # Export the resulting imported layout and changes to JPEG
        # print(f"Exporting '{current_layout.name}'")
        # current_map.exportToJPEG(rf"{project_folder}\Layouts\{current_layout.name}.jpg", page_width, page_height)
        # current_map.exportToPNG(rf"{project_folder}\Layouts\{current_layout.name}.png", page_width, page_height)

        # fc_md = md.Metadata(dataset)
        # fc_md.thumbnailUri = rf"{project_folder}\Layouts\{dataset_name}.png"
        # fc_md.thumbnailUri = rf"{project_folder}\Layouts\{dataset_name}.jpg"
        # fc_md.save()
        # del fc_md

        aprx.save()

        # #            from arcpy import metadata as md
        # #
        # #            fc_md = md.Metadata(dataset)
        # #            fc_md.thumbnailUri = rf"{project_folder}\Layers\{dataset_name}.png"
        # #            fc_md.save()
        # #            del fc_md
        # #            del md

        ##        aprx.save()
        ##
        ##        current_layout = [cl for cl in aprx.listLayouts() if cl.name == dataset_name][0]
        ##        print(f"Current Layout: {current_layout.name}")
        ##
        ##        current_layout.openView()
        ##
        ##        # Remove all map frames
        ##        for mf in current_layout.listElements("MapFrame_Element"): current_layout.deleteElement(mf); del mf
        ##
        ##        # print(f'Layout Name: {current_layout.name}')
        ##        # print(f'    Width x height: {current_layout.pageWidth} x {current_layout.pageHeight} units are {current_layout.pageUnits}')
        ##        # print(f'    MapFrame count: {str(len(current_layout.listElements("MapFrame_Element")))}')
        ##        # for mf in current_layout.listElements("MapFrame_Element"):
        ##        #     if len(current_layout.listElements("MapFrame_Element")) > 0:
        ##        #         print(f'        MapFrame name: {mf.name}')
        ##        # print(f'    Total element count: {str(len(current_layout.listElements()))} \n')
        ##
        ##
        ##        print(f"Create a new map frame using a point geometry")
        ##        #Create a new map frame using a point geometry
        ##        #mf1 = current_layout.createMapFrame(arcpy.Point(0.01,0.01), current_map, 'New MF - Point')
        ##        mf1 = current_layout.createMapFrame(arcpy.Point(0.0,0.0), current_map, 'New MF - Point')
        ##        #mf1.elementWidth = 10
        ##        #mf1.elementHeight = 7.5
        ##        #mf1.elementWidth  = page_width  - 0.01
        ##        #mf1.elementHeight = page_height - 0.01
        ##        mf1.elementWidth  = page_width
        ##        mf1.elementHeight = page_height

        ##        lyr = current_map.listLayers(f"{dataset_name}")[0]
        ##
        ##        #Zoom to ALL selected features and export to PDF
        ##        #arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION')
        ##        #mf1.zoomToAllLayers(True)
        ##        #arcpy.SelectLayerByAttribute_management(lyr, 'CLEAR_SELECTION')
        ##
        ##        #Set the map frame extent to the extent of a layer
        ##        #mf1.camera.setExtent(mf1.getLayerExtent(lyr, False, True))
        ##        #mf1.camera.scale = mf1.camera.scale * 1.1 #add a slight buffer
        ##
        ##        del lyr

        ##        print(f"Create a new bookmark set to the map frame's default extent")
        ##        #Create a new bookmark set to the map frame's default extent
        ##        bkmk = mf1.createBookmark('Default Extent', "The map's default extent")
        ##        bkmk.updateThumbnail()
        ##        del mf1
        ##        del bkmk

        # Create point text element using a system style item
        # txtStyleItem = aprx.listStyleItems('ArcGIS 2D', 'TEXT', 'Title (Serif)')[0]
        # ptTxt = aprx.createTextElement(current_layout, arcpy.Point(5.5, 4.25), 'POINT', f'{dataset_name}', 10, style_item=txtStyleItem)
        # del txtStyleItem

        # Change the anchor position and reposition the text to center
        # ptTxt.setAnchor('Center_Point')
        # ptTxt.elementPositionX = page_width / 2.0
        # ptTxt.elementPositionY = page_height - 0.25
        # del ptTxt

        # print(f"Using CIM to update border")
        # current_layout_cim = current_layout.getDefinition('V3')
        # for elm in current_layout_cim.elements:
        #     if type(elm).__name__ == 'CIMMapFrame':
        #         if elm.graphicFrame.borderSymbol.symbol.symbolLayers:
        #             sym = elm.graphicFrame.borderSymbol.symbol.symbolLayers[0]
        #             sym.width = 5
        #             sym.color.values = [255, 0, 0, 100]
        #         else:
        #             arcpy.AddWarning(elm.name + ' has NO symbol layers')
        # current_layout.setDefinition(current_layout_cim)
        # del current_layout_cim, elm, sym

        ##        ExportLayout = True
        ##        if ExportLayout:
        ##            #Export the resulting imported layout and changes to JPEG
        ##            print(f"Exporting '{current_layout.name}'")
        ##            current_layout.exportToJPEG(rf"{project_folder}\Layouts\{current_layout.name}.jpg")
        ##            current_layout.exportToPNG(rf"{project_folder}\Layouts\{current_layout.name}.png")
        ##        del ExportLayout

        ##        #Export the resulting imported layout and changes to JPEG
        ##        print(f"Exporting '{current_layout.name}'")
        ##        current_map.exportToJPEG(rf"{project_folder}\Layouts\{current_layout.name}.jpg", page_width, page_height)
        ##        current_map.exportToPNG(rf"{project_folder}\Layouts\{current_layout.name}.png", page_width, page_height)
        ##
        ##        fc_md = md.Metadata(dataset)
        ##        fc_md.thumbnailUri = rf"{project_folder}\Layouts\{current_layout.name}.png"
        ##        #fc_md.thumbnailUri = rf"{project_folder}\Layouts\{current_layout.name}.jpg"
        ##        fc_md.save()
        ##        del fc_md
        ##
        ##        aprx.save()

        # aprx.deleteItem(current_map)
        # aprx.deleteItem(current_layout)

        del current_map
        # , current_layout
        # del page_width, page_height
        del dataset_name, dataset

        aprx.save()

        print("\nCurrent Maps & Layouts")

        current_maps = aprx.listMaps()
        # current_layouts = aprx.listLayouts()

        if current_maps:
            print("\nCurrent Maps\n")
            for current_map in current_maps:
                print(f"\tProject Map: {current_map.name}")
                del current_map
        else:
            arcpy.AddWarning("No maps in Project")

        ##        if current_layouts:
        ##            print(f"\nCurrent Layouts\n")
        ##            for current_layout in current_layouts:
        ##                print(f"\tProject Layout: {current_layout.name}")
        ##                del current_layout
        ##        else:
        ##            arcpy.AddWarning("No layouts in Project")

        # del current_layouts
        del current_maps

        # Declared Variables set in function for aprx

        # Save aprx one more time and then delete
        aprx.save()
        del aprx

        # Declared Variables set in function
        del project_gdb, base_project_folder, metadata_folder, crfs_folder
        del project_folder, scratch_folder

        # Imports
        del dismap, parse_xml_file_format_and_save
        del md

        # Function Parameters
        del base_project_file, project

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
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    else:
        # Store all the local variables in a list,
        # using locals keyword.
        locals_stored = set(locals())

        if locals_stored:
            # Iterate over the list and print the local
            # variables.
            print(f"\nPrinting Local Variables in the '{inspect.stack()[0][3]}' function")
            for name in locals_stored:
                val = eval(name)
                print(f"\t{name} is {type(val)} and is equal to {val}")
        else:
            pass


def add_dataset_metadata(workspace="", wild_card="", feature_type="All"):
    try:
        from lxml import etree
        from  io import StringIO
        import json

        from arcpy import metadata as md

        import dismap_tools

        # Set basic arcpy.env variables
        arcpy.env.overwriteOutput          = True
        arcpy.env.parallelProcessingFactor = "100%"

        arcpy.env.workspace = workspace
        #print(workspace)

        project_folder = os.path.dirname(workspace)
        project_name   = os.path.basename(project_folder)

        datasets_dict = dismap_tools.dataset_title_dict(project_folder)

        for dataset in sorted(arcpy.ListDatasets(wild_card = wild_card, feature_type = feature_type)):
            print(f"Dataset: {dataset}")

            dataset_service = datasets_dict[dataset.replace("_CRF.crf", "")]["Dataset Service"]

            print(dataset_service)

            dataset_md = md.Metadata(dataset)
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()

            tree = etree.parse(StringIO(dataset_md.xml), parser=etree.XMLParser(encoding="UTF-8", remove_blank_text=True))
            root = tree.getroot()

            root.find(".//enttypl").attrib["Sync"] = "TRUE"

            # ### ->> Create Date and time Start
            # Set Create Date and time
            create_date = root.xpath("/metadata/Esri/CreaDate")

            if len(create_date) > 1:
                for i in range(1, len(create_date)):
                    create_date[i].getparent().remove(create_date[i])

            if len(create_date) == 1:
                # print(f"Create Date exists: {create_date[0].text}")
                create_date[0].text = dismap_tools.date_code(project_name)

            elif len(create_date) == 0:
                # print("Create Date does not exists")
                esri = root.xpath("/metadata/Esri")[0]
                _create_date = etree.SubElement(esri, "CreaDate")
                _create_date.text = dismap_tools.date_code(project_name)
                del esri, _create_date
            else:
                pass
            del create_date

            create_time = root.xpath("/metadata/Esri/CreaTime")

            if len(create_time) > 1:
                for i in range(1, len(create_time)):
                    create_time[i].getparent().remove(create_time[i])

            if len(create_time) == 1:
                #print(f"Create Time exists: {create_time[0].text}")
                create_time[0].text = "00000000"

            elif len(create_time) == 0:
                #print("Create Time does not exists")
                esri = root.xpath("/metadata/Esri")[0]
                _create_time = etree.SubElement(esri, "CreaTime")
                _create_time.text = "00000000"
                del esri, _create_time
            else:
                pass
            del create_time

            # ### ->> Create Date and time End

            # ### ->> linkage Start
            linkage = root.xpath("./distInfo/distTranOps/onLineSrc/linkage")

            for link in linkage:
                print(f"\tLink: {link.text}\n")
                del link

            del linkage

            # ### ->> linkage End

            # ### ->> itemName Start

            item_name = root.find("./Esri/DataProperties/itemProps/itemName").text

            print(f"\tItem Name: {item_name}")


            del item_name

            # ### ->> itemName End

            # ### ->> eainfo/detailed Start

            res_title = root.find("./dataIdInfo/idCitation/resTitle").text

            #root.find(".//enttypl").text = res_title if " Table " in res_title else res_title[:-9] + " Table " + version_code
            #root.find(".//enttypl").attrib["Sync"] = "FALSE"

            eainfo_detailed = root.find("./eainfo/detailed")
            eainfo_detailed.set("Sync", "FALSE")
            eainfo_detailed.set("Name", res_title[:-9] + " Table " + res_title[-8:])

            print(f"\teainfo_detailed: {eainfo_detailed.get('Name')}\n")
            #print(res_title)

            del eainfo_detailed
            del res_title

            # ### ->> eainfo/detailed End

            # Save back to dataset
            etree.indent(root, space="    ")
            dataset_md.xml = etree.tostring(
                tree,
                encoding="UTF-8",
                method="xml",
                xml_declaration=True,
                pretty_print=True,
            )
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()
            del dataset_md

            del tree, root
            del dataset


        # Declared variables
        del datasets_dict
        del project_folder, project_name
        # Imports
        del etree, StringIO, json, md, dismap_tools
        # Function parameter
        del workspace, wild_card, feature_type

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
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    else:
        # Store all the local variables in a list,
        # using locals keyword.
        locals_stored = set(locals())

        if locals_stored:
            # Iterate over the list and print the local
            # variables.
            #print(f"\nPrinting Local Variables in the '{inspect.stack()[0][3]}' function")
            for name in locals_stored:
                val = eval(name)
                print(f"\nLocal variable '{name}' is '{type(val)}' and is equal to '{val}'\n")
        else:
            pass


def script_tool(project_folder=""):
    """Script code goes below"""
    try:
        # Imports
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

        project_name = os.path.basename(project_folder)
        project_gdb  = os.path.join(project_folder, f"{project_name}.gdb")
        crf_folder   = os.path.join(project_folder, "CRFs")

        AddDatasetMetadata = True
        if AddDatasetMetadata:
            # CRF Folder
            add_dataset_metadata(workspace=crf_folder, wild_card="*", feature_type="Raster")
            # Mosaics in Project GDB
            #add_dataset_metadata(workspace=project_gdb, wild_card="*", feature_type="Mosaic")
        else:
            pass
        del AddDatasetMetadata

##        CreateMaps = False
##        if CreateMaps:
##            create_maps(base_project_file, project, dataset=rf"{project_gdb}\DisMAP_Regions")
##        del CreateMaps

        # Variable created in function
        del project_name, project_gdb, crf_folder
        # Imports
        # Function parameters
        del project_folder

        # Elapsed time
        end_time = time()
        hours, rem = divmod(end_time - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        arcpy.AddMessage(f"\n{'-' * 80}")
        arcpy.AddMessage(f"Python script: {os.path.basename(__file__)}")
        arcpy.AddMessage(f"Start Time: {strftime('%a %b %d %I:%M %p', localtime(start_time))}")
        arcpy.AddMessage(f"End Time: {strftime('%a %b %d %I:%M %p', localtime(end_time))}")
        arcpy.AddMessage(f"Elapsed Time   {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f} (H:M:S)")
        arcpy.AddMessage(f"{'-' * 80}")
        del hours, rem, minutes, seconds
        del end_time, start_time
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
        # Store all the local variables in a list,
        # using locals keyword.
        locals_stored = set(locals())

        if locals_stored:
            # Iterate over the list and print the local
            # variables.
            #print(f"\nPrinting Local Variables in the '{inspect.stack()[0][3]}' function")
            for name in locals_stored:
                val = eval(name)
                print(f"Local variable '{name}' is '{type(val)}' and is equal to '{val}'")
        else:
            pass

        # Store the global variables in a list using
        # globals keyword and subtract the previously
        # created list of built-in global variables from it.
        globals_stored = set(globals())-not_my_data

        if globals_stored:
            # Iterate over the list and print the local
            # variables.
            #print(f"\nPrinting Global Variables in the '{inspect.stack()[0][3]}' function")
            for name in globals_stored:
                # Excluding func and not_my_data as they are
                # also considered as a global variable
                #if name != "not_my_data" and name != "func":
                if name != "not_my_data" and name != "project_folder":
                    val = eval(name)
                    print(f"Global variable '{name}' is {type(val)} and is equal to '{val}'")

        else:
            pass

if __name__ == '__main__':
    try:
        # Create a list of all global variables using
        # globals( ) function, To store the built-in
        # global variables.
        not_my_data = set(globals())

        project_folder = arcpy.GetParameterAsText(0)
        if not project_folder:
            # project_name = "August-1-2025"
            # project_name = "February-1-2026"
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


# This is an autogenerated comment.
