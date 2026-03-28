# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      john.f.kennedy
#
# Created:     05/03/2024
# Copyright:   (c) john.f.kennedy 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys # built-ins first
import traceback
import inspect

import arcpy # third-parties second

def worker(region_gdb=""):
    try:
        # Test if passed workspace exists, if not sys.exit()
        if not arcpy.Exists(rf"{region_gdb}"):
            sys.exit()(f"{os.path.basename(region_gdb)} is missing!!")

        # Imports
        from arcpy import metadata as md
        import dismap_tools

        # Set History and Metadata logs, set serverity and message level
        arcpy.SetLogHistory(True) # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(2) # 0—A tool will not throw an exception, even if the tool produces an error or warning.
                                  # 1—If a tool produces a warning or an error, it will throw an exception.
                                  # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(['NORMAL']) # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic workkpace variables
        table_name        = os.path.basename(region_gdb).replace(".gdb","")
        scratch_folder    = os.path.dirname(region_gdb)
        project_folder    = os.path.dirname(scratch_folder)
        csv_data_folder   = rf"{project_folder}\CSV_Data"
        scratch_workspace = rf"{scratch_folder}\{table_name}\scratch.gdb"

        arcpy.AddMessage(f"Table Name: {table_name}\nProject Folder: {os.path.basename(project_folder)}\nScratch Folder: {os.path.basename(scratch_folder)}\n")

        # Set basic workkpace variables
        arcpy.env.workspace                 = region_gdb
        arcpy.env.scratchWorkspace          = scratch_workspace
        arcpy.env.overwriteOutput           = True
        arcpy.env.parallelProcessingFactor  = "100%"
        arcpy.env.compression               = "LZ77"
        #arcpy.env.geographicTransformations = "WGS_1984_(ITRF08)_To_NAD_1983_2011"
        arcpy.env.pyramid                   = "PYRAMIDS -1 BILINEAR LZ77 NO_SKIP"
        arcpy.env.resamplingMethod          = "BILINEAR"
        arcpy.env.rasterStatistics          = "STATISTICS 1 1"
        #arcpy.env.XYResolution               = "0.1 Meters"
        #arcpy.env.XYResolution              = "0.01 Meters"
        #arcpy.env.cellAlignment = "ALIGN_WITH_PROCESSING_EXTENT" # Set the cell alignment environment using a keyword.

        # DatasetCode, CSVFile, TransformUnit, TableName, GeographicArea, CellSize,
        # PointFeatureType, FeatureClassName, Region, Season, DateCode, Status,
        # DistributionProjectCode, DistributionProjectName, SummaryProduct,
        # FilterRegion, FilterSubRegion, FeatureServiceName, FeatureServiceTitle,
        # MosaicName, MosaicTitle, ImageServiceName, ImageServiceTitle

        # Get values for table_name from Datasets table
        #fields = ["TableName", "GeographicArea", "DatasetCode", "CellSize", "MosaicName", "MosaicTitle"]
        #region_list = [row for row in arcpy.da.SearchCursor(rf"{region_gdb}\Datasets", fields, where_clause = f"TableName = '{table_name}'")][0]
        #del fields

        # Assigning variables from items in the chosen table list
        # ['AI_IDW', 'AI_IDW_Region', 'AI', 'Aleutian Islands', None, 'IDW']
        #table_name      = region_list[0]
        #geographic_area = region_list[1]
        #datasetcode     = region_list[2]
        #cell_size       = region_list[3]
        #mosaic_name     = region_list[4]
        #mosaic_title    = region_list[5]
        #del region_list

        # Start of business logic for the worker function
        arcpy.AddMessage(f"Processing: {table_name}")

        # Input
        region_fishnet            = rf"{region_gdb}\{table_name}_Fishnet"
        region_raster_mask        = rf"{region_gdb}\{table_name}_Raster_Mask"
        region_fishnet_bathymetry = rf"{region_gdb}\{table_name}_Fishnet_Bathymetry"
        # Output
        region_bathymetry         = rf"{region_gdb}\{table_name}_Bathymetry"

        # Get the reference system defined for the region in datasets
        # Set the output coordinate system to what is needed for the
        # DisMAP project
        region_prj = arcpy.Describe(region_raster_mask).spatialReference
        #arcpy.AddMessage(f"region_prj: {region_prj}")
        if region_prj.linearUnitName == "Kilometer":
            arcpy.env.cellSize = 1
            arcpy.env.XYResolution = 0.1
            arcpy.env.XYResolution  = 1.0
        elif region_prj.linearUnitName == "Meter":
            arcpy.env.cellSize = 1000
            arcpy.env.XYResolution = 0.0001
            arcpy.env.XYResolution  = 0.001

        # Process: Point to Raster Mask
        arcpy.env.outputCoordinateSystem = region_prj
        arcpy.env.cellSize   = int(arcpy.Describe(f"{region_raster_mask}/Band_1").meanCellWidth)
        arcpy.env.extent     = arcpy.Describe(region_raster_mask).extent
        arcpy.env.mask       = region_raster_mask
        arcpy.env.snapRaster = region_raster_mask

        del region_prj

        arcpy.AddMessage(f"\tCalculating Zonal Statistics using {os.path.basename(region_fishnet)} and {os.path.basename(region_fishnet_bathymetry)} to create {os.path.basename(region_bathymetry)}")
        # Execute ZonalStatistics
        #out_raster = arcpy.sa.ZonalStatistics(region_fishnet, "OID", region_fishnet_bathymetry, "MEDIAN", "NODATA")
        #out_raster = arcpy.sa.ZonalStatistics(region_fishnet, "OID", region_fishnet_bathymetry, "MEDIAN", "DATA")

        with arcpy.EnvManager(scratchWorkspace = arcpy.env.scratchWorkspace):
            #print(region_fishnet)
            #rint(region_fishnet_bathymetry)
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
                                circular_wrap_value           = 360
                            )

            arcpy.AddMessage("\tZonal Statistics: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            # Save the output
            out_raster.save(region_bathymetry)
            arcpy.AddMessage("\tSave: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            del out_raster

        dismap_tools.import_metadata(csv_data_folder, region_bathymetry)

        del region_bathymetry

        arcpy.management.Delete(rf"{region_gdb}\Datasets")
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
        arcpy.management.Delete(region_raster_mask)
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
        arcpy.management.Delete(region_fishnet)
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
        arcpy.management.Delete(region_fishnet_bathymetry)
        arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
        del region_raster_mask, region_fishnet, region_fishnet_bathymetry

        arcpy.management.Compact(region_gdb)

        # Declared Variables for this function only
        del scratch_folder, scratch_workspace
        del table_name, project_folder, csv_data_folder
        # Imports
        del md, dismap_tools
        # Function parameter
        del region_gdb

    except KeyboardInterrupt:
        sys.exit()
    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"Caught an arcpy.ExecuteWarning error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddWarning(arcpy.GetMessages(1))
        traceback.print_exc()
        sys.exit()
    except arcpy.ExecuteError:
        arcpy.AddError(f"Caught an arcpy.ExecuteError error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
        sys.exit()
    except SystemExit as se:
        arcpy.AddError(f"Caught an SystemExit error: {se} in the '{inspect.stack()[0][3]}' function.")
        sys.exit()
    except Exception as e:
        arcpy.AddError(f"Caught an Exception error: {e} in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    except:
        arcpy.AddError(f"Caught an except error in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith('__')]
        if rk: arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##"); del rk
        return True
    finally:
        pass

def preprocessing(project_gdb="", table_names="", clear_folder=True):
    try:
        import dismap_tools

        arcpy.SetLogHistory(True) # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(1) # 0—A tool will not throw an exception, even if the tool produces an error or warning.
                                  # 1—If a tool produces a warning or an error, it will throw an exception.
                                  # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(['NORMAL']) # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic arcpy.env variables
        arcpy.env.overwriteOutput          = True
        arcpy.env.parallelProcessingFactor = "100%"

        # Set varaibales
        project_folder    = os.path.dirname(project_gdb)
        scratch_folder    = rf"{project_folder}\Scratch"
        scratch_workspace = rf"{project_folder}\Scratch\scratch.gdb"
        csv_data_folder   = rf"{os.path.dirname(project_gdb)}\CSV_Data"
        project_bathymetry_gdb = rf"{project_folder}\Bathymetry\Bathymetry.gdb"

        # Clear Scratch Folder
        #ClearScratchFolder = True
        #if ClearScratchFolder:
        if clear_folder:
            dismap_tools.clear_folder(folder=rf"{os.path.dirname(project_gdb)}\Scratch")
        else:
            pass
        #del ClearScratchFolder
        del clear_folder

        arcpy.env.workspace        = project_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        del project_folder, scratch_workspace

        if not table_names:
            table_names = [row[0] for row in arcpy.da.SearchCursor(f"{project_gdb}\Datasets",
                                                                   "TableName",
                                                                   where_clause = "TableName LIKE '%_IDW'")]
        else:
            pass

        for table_name in table_names:
            arcpy.AddMessage(f"Pre-Processing: {table_name}")

            region_gdb = rf"{scratch_folder}\{table_name}.gdb"
            region_scratch_workspace = rf"{scratch_folder}\{table_name}\scratch.gdb"

            # Create Scratch Workspace for Region
            if not arcpy.Exists(region_scratch_workspace):
                os.makedirs(rf"{scratch_folder}\{table_name}")
                if not arcpy.Exists(region_scratch_workspace):
                    arcpy.AddMessage(f"Create File GDB: '{table_name}'")
                    arcpy.management.CreateFileGDB(rf"{scratch_folder}\{table_name}", f"scratch")
                    arcpy.AddMessage("\tCreate File GDB: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            del region_scratch_workspace
            # # # CreateFileGDB
            arcpy.AddMessage(f"Creating File GDB: '{table_name}'")
            arcpy.management.CreateFileGDB(rf"{scratch_folder}", f"{table_name}")
            arcpy.AddMessage("\tCreate File GDB: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            # # # CreateFileGDB

            # # # Datasets
            # Process: Make Table View (Make Table View) (management)
            datasets = rf'{project_gdb}\Datasets'
            arcpy.AddMessage(f"'{os.path.basename(datasets)}' has {arcpy.management.GetCount(datasets)[0]} records")
            arcpy.management.Copy(datasets, rf"{region_gdb}\Datasets")
            arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            del datasets
            # # # Datasets

            # # # Fishnet
            region_fishnet = rf"{project_gdb}\{table_name}_Fishnet"
            arcpy.AddMessage(f"The table '{table_name}_Fishnet' has {arcpy.management.GetCount(region_fishnet)[0]} records")
            arcpy.management.Copy(region_fishnet, rf"{region_gdb}\{table_name}_Fishnet")
            arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            del region_fishnet
            # # # Fishnet

            # # # Raster_Mask
            arcpy.AddMessage(f"Copy Raster Mask for '{table_name}'")
            arcpy.management.Copy(rf"{project_gdb}\{table_name}_Raster_Mask", rf"{region_gdb}\{table_name}_Raster_Mask")
            arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            # # # Raster_Mask

            # # # Bathymetry
            arcpy.AddMessage(f"Copy Bathymetry for '{table_name}'")
            arcpy.management.Copy(rf"{project_bathymetry_gdb}\{table_name}_Bathymetry", rf"{region_gdb}\{table_name}_Fishnet_Bathymetry")
            arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            # # # Bathymetry

            # Declared Variables
            del table_name

        # Declared Variables
        del scratch_folder, region_gdb
        del csv_data_folder, project_bathymetry_gdb
        # Imports
        del dismap_tools
        # Function Parameters
        del project_gdb, table_names

    except KeyboardInterrupt:
        sys.exit()
    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"Caught an arcpy.ExecuteWarning error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddWarning(arcpy.GetMessages(1))
        traceback.print_exc()
        sys.exit()
    except arcpy.ExecuteError:
        arcpy.AddError(f"Caught an arcpy.ExecuteError error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
        sys.exit()
    except SystemExit as se:
        arcpy.AddError(f"Caught an SystemExit error: {se} in the '{inspect.stack()[0][3]}' function.")
        sys.exit()
    except Exception as e:
        arcpy.AddError(f"Caught an Exception error: {e} in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    except:
        arcpy.AddError(f"Caught an except error in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith('__')]
        if rk: arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##"); del rk
        return True
    finally:
        pass

def script_tool(project_gdb=""):
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

        table_names = ["HI_IDW",]

        preprocessing(project_gdb=project_gdb, table_names=table_names, clear_folder=True)

        for table_name in table_names:
            region_gdb = rf"{os.path.dirname(project_gdb)}\Scratch\{table_name}.gdb"
            try:
                pass
                worker(region_gdb=region_gdb)
            except SystemExit:
                arcpy.AddError(arcpy.GetMessages(2))
                traceback.print_exc()
                sys.exit()
            del table_name, region_gdb
        del table_names

        # Declared Varaiables
        # Imports
        # Function Parameters
        del project_gdb

        # Elapsed time
        end_time = time()
        elapse_time =  end_time - start_time
        hours, rem = divmod(end_time-start_time, 3600)
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

    except KeyboardInterrupt:
        sys.exit()
    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"Caught an arcpy.ExecuteWarning error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddWarning(arcpy.GetMessages(1))
        traceback.print_exc()
        sys.exit()
    except arcpy.ExecuteError:
        arcpy.AddError(f"Caught an arcpy.ExecuteError error in the '{inspect.stack()[0][3]}' function.")
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
        sys.exit()
    except SystemExit as se:
        arcpy.AddError(f"Caught an SystemExit error: {se} in the '{inspect.stack()[0][3]}' function.")
        sys.exit()
    except Exception as e:
        arcpy.AddError(f"Caught an Exception error: {e} in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    except:
        arcpy.AddError(f"Caught an except error in the '{inspect.stack()[0][3]}' function.")
        traceback.print_exc()
        sys.exit()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith('__')]
        if rk: arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##"); del rk
        return True
    finally:
        pass

if __name__ == '__main__':
    try:
        project_gdb = arcpy.GetParameterAsText(0)
        if not project_gdb:
            project_gdb = rf"{os.path.expanduser('~')}\Documents\ArcGIS\Projects\DisMAP\ArcGIS-Analysis-Python\August 1 2025\August 1 2025.gdb"
        else:
            pass
        script_tool(project_gdb)
        arcpy.SetParameterAsText(1, "Result")
        del project_gdb
    except:
        traceback.print_exc()
    else:
        pass
    finally:
        pass