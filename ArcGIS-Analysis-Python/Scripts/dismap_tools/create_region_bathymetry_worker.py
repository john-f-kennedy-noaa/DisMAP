# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      john.f.kennedy
#
# Created:     05/03/2024
# Copyright:   (c) john.f.kennedy 2024
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os
import sys
import traceback
import inspect

import arcpy  # third-parties second

def worker(region_gdb=""):
    try:
        # Test if passed workspace exists, if not sys.exit()
        if not arcpy.Exists(rf"{region_gdb}"):
            sys.exit()(f"{os.path.basename(region_gdb)} is missing!!")

        # Imports
        from lxml import etree
        #from  io import StringIO
        from arcpy import metadata as md

        import dismap_tools

        # Set History and Metadata logs, set serverity and message level
        arcpy.SetLogHistory(True)  # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(2)  # 0—A tool will not throw an exception, even if the tool produces an error or warning.
        # 1—If a tool produces a warning or an error, it will throw an exception.
        # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(["NORMAL"])  # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic workkpace variables
        table_name = os.path.basename(region_gdb).replace(".gdb", "")
        scratch_folder = os.path.dirname(region_gdb)
        project_folder = os.path.dirname(scratch_folder)
        home_folder    = os.path.dirname(project_folder)
        project_name   = os.path.basename(project_folder)
        csv_data_folder = os.path.join(project_folder, "CSV_Data")
        scratch_workspace = rf"{scratch_folder}\{table_name}\scratch.gdb"

        arcpy.AddMessage(f"Table Name: {table_name}\nProject Folder: {os.path.basename(project_folder)}\nScratch Folder: {os.path.basename(scratch_folder)}\n")

        # Set basic workkpace variables
        arcpy.env.workspace = region_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"
        arcpy.env.compression = "LZ77"
        # arcpy.env.geographicTransformations = "WGS_1984_(ITRF08)_To_NAD_1983_2011"
        arcpy.env.pyramid = "PYRAMIDS -1 BILINEAR LZ77 NO_SKIP"
        arcpy.env.resamplingMethod = "BILINEAR"
        arcpy.env.rasterStatistics = "STATISTICS 1 1"
        # arcpy.env.XYResolution               = "0.1 Meters"
        # arcpy.env.XYResolution              = "0.01 Meters"
        # arcpy.env.cellAlignment = "ALIGN_WITH_PROCESSING_EXTENT" # Set the cell alignment environment using a keyword.

        # DatasetCode, CSVFile, TransformUnit, TableName, GeographicArea, CellSize,
        # PointFeatureType, FeatureClassName, Region, Season, DateCode, Status,
        # DistributionProjectCode, DistributionProjectName, SummaryProduct,
        # FilterRegion, FilterSubRegion, FeatureServiceName, FeatureServiceTitle,
        # MosaicName, MosaicTitle, ImageServiceName, ImageServiceTitle

        # Get values for table_name from Datasets table
        # fields = ["TableName", "GeographicArea", "DatasetCode", "CellSize", "MosaicName", "MosaicTitle"]
        # region_list = [row for row in arcpy.da.SearchCursor(rf"{region_gdb}\Datasets", fields, where_clause = f"TableName = '{table_name}'")][0]
        # del fields

        # Assigning variables from items in the chosen table list
        # ['AI_IDW', 'AI_IDW_Region', 'AI', 'Aleutian Islands', None, 'IDW']
        # table_name      = region_list[0]
        # geographic_area = region_list[1]
        # datasetcode     = region_list[2]
        # cell_size       = region_list[3]
        # mosaic_name     = region_list[4]
        # mosaic_title    = region_list[5]
        # del region_list

        # Start of business logic for the worker function
        arcpy.AddMessage(f"Processing: {table_name}")

        # Input
        region_fishnet     = os.path.join(region_gdb, f"{table_name}_Fishnet")
        region_raster_mask = os.path.join(region_gdb, f"{table_name}_Raster_Mask")
        region_fishnet_bathymetry = os.path.join(region_gdb, f"{table_name}_Fishnet_Bathymetry")
        # Output
        region_bathymetry = os.path.join(region_gdb, f"{table_name}_Bathymetry")

        # Get the reference system defined for the region in datasets
        # Set the output coordinate system to what is needed for the
        # DisMAP project
        region_prj = arcpy.Describe(region_raster_mask).spatialReference
        # arcpy.AddMessage(f"region_prj: {region_prj}")
        if region_prj.linearUnitName == "Kilometer":
            arcpy.env.cellSize = 1
            arcpy.env.XYResolution = 0.1
            arcpy.env.XYResolution = 1.0
        elif region_prj.linearUnitName == "Meter":
            arcpy.env.cellSize = 1000
            arcpy.env.XYResolution = 0.0001
            arcpy.env.XYResolution = 0.001

        # Process: Point to Raster Mask
        arcpy.env.outputCoordinateSystem = region_prj
        arcpy.env.cellSize = int(arcpy.Describe(os.path.join(region_raster_mask, "Band_1")).meanCellWidth)
        arcpy.env.extent = arcpy.Describe(region_raster_mask).extent
        arcpy.env.mask = region_raster_mask
        arcpy.env.snapRaster = region_raster_mask

        del region_prj

        arcpy.AddMessage(f"\tCalculating Zonal Statistics using {os.path.basename(region_fishnet)} and {os.path.basename(region_fishnet_bathymetry)} to create {os.path.basename(region_bathymetry)}")
        # Execute ZonalStatistics
        # out_raster = arcpy.sa.ZonalStatistics(region_fishnet, "OID", region_fishnet_bathymetry, "MEDIAN", "NODATA")
        # out_raster = arcpy.sa.ZonalStatistics(region_fishnet, "OID", region_fishnet_bathymetry, "MEDIAN", "DATA")

        with arcpy.EnvManager(scratchWorkspace=arcpy.env.scratchWorkspace):
            # print(region_fishnet)
            # rint(region_fishnet_bathymetry)
            out_raster = arcpy.sa.ZonalStatistics(
                in_zone_data                  = region_fishnet,
                zone_field                    = "OID",
                in_value_raster               = region_fishnet_bathymetry,
                statistics_type               = "MEDIAN",
                ignore_nodata                 = "DATA",
                process_as_multidimensional   = "CURRENT_SLICE",
                percentile_value              = 90,
                percentile_interpolation_type = "AUTO_DETECT",
                circular_calculation          = "ARITHMETIC",
                circular_wrap_value           = 360,
            )
            arcpy.AddMessage("\tZonal Statistics: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

            # Save the output
            out_raster.save(region_bathymetry)
            arcpy.AddMessage("\tSave: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))
            del out_raster

        print(arcpy.env.cellSize)
        print(region_raster_mask, arcpy.management.GetRasterProperties(in_raster=region_raster_mask, property_type="COLUMNCOUNT", band_index="Band_1").getOutput(0),
                  arcpy.management.GetRasterProperties(in_raster=region_raster_mask, property_type="ROWCOUNT", band_index="Band_1").getOutput(0),)
        print(region_bathymetry, arcpy.management.GetRasterProperties(in_raster=region_bathymetry, property_type="COLUMNCOUNT", band_index="Band_1").getOutput(0),
                  arcpy.management.GetRasterProperties(in_raster=region_bathymetry, property_type="ROWCOUNT", band_index="Band_1").getOutput(0),)

        # Add boilerplate metadata to dataset
        # Version Code
        version_code = dismap_tools.date_code(project_name)
        # Boilerplate
        contacts = rf"{home_folder}\Initial-Data\DisMAP-Contacts-{version_code}.xml"
        # Reads XML, pretty format, and write back the contacts XML
        etree.parse(contacts, parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)).write(contacts, pretty_print=True, xml_declaration=True, encoding="UTF-8") # pyright: ignore[reportAttributeAccessIssue]

        # Create Metadata object for new table
        dataset_md = md.Metadata(region_bathymetry)
        dataset_md.importMetadata(contacts, "ARCGIS_METADATA")
        dataset_md.save()
        dataset_md.synchronize("ALWAYS")
        dataset_md.save()
        del dataset_md

        dismap_tools.import_metadata(project_folder, region_bathymetry)

        #print(region_bathymetry, arcpy.management.GetRasterProperties(in_raster=region_bathymetry, property_type="COLUMNCOUNT", band_index="Band_1").getOutput(0),
        #          arcpy.management.GetRasterProperties(in_raster=region_bathymetry, property_type="ROWCOUNT", band_index="Band_1").getOutput(0),)

        del region_bathymetry

        arcpy.management.Delete(os.path.join(region_gdb, "Datasets"))
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

        arcpy.management.Delete(os.path.join(region_gdb, region_raster_mask))
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

        arcpy.management.Delete(os.path.join(region_gdb, region_fishnet))
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

        arcpy.management.Delete(os.path.join(region_gdb, region_fishnet_bathymetry))
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

        del region_raster_mask, region_fishnet, region_fishnet_bathymetry

        arcpy.management.Compact(region_gdb)

        # Reset environment settings to default settings.
        arcpy.ResetEnvironments()

        # Declared Variables for this function only
        del scratch_folder, scratch_workspace
        del table_name, project_folder, csv_data_folder
        # Imports
        del md, dismap_tools
        # Function parameter
        del region_gdb

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

        ##        # Set worker parameters
        ##        #table_name = "AI_IDW"
        ##        table_name = "HI_IDW"
        ##        #table_name = "NBS_IDW"
        ##        #table_name = "ENBS_IDW"

        project_name        = os.path.basename(project_folder)
        project_gdb         = os.path.join(project_folder, f"{project_name}.gdb")

        table_names = ["NBS_IDW",]

        from create_region_bathymetry_director import preprocessing

        preprocessing(project_gdb=project_gdb, table_names=table_names, clear_folder=True)

        del preprocessing

        for table_name in table_names:
            region_gdb = os.path.join(project_folder, f"Scratch\\{table_name}.gdb")
            worker(region_gdb=region_gdb)
            del table_name, region_gdb
        del table_names

        # Reset environment settings to default settings.
        arcpy.ResetEnvironments()

        # Declared Varaiables
        # Imports
        # Function Parameters
        del project_gdb

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
        arcpy.AddMessage("Script finished successfully.")
    finally:
        arcpy.AddMessage(f"{'--End' * 10}--")

if __name__ == '__main__':
    try:

        project_folder = arcpy.GetParameterAsText(0)
        if not project_folder:
            # project_name = "August-1-2025"
            # project_name = "February-1-2026"
            project_name = "June-1-2026"
            project_folder = os.path.join(os.path.expanduser('~'), f"Documents\\ArcGIS\\Projects\\DisMAP\\ArcGIS-Analysis-Python\\{project_name}")
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
