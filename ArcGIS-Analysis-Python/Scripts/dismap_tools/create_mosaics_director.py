# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        create_species_year_image_name_table_director
# Purpose:
#
# Author:      john.f.kennedy
#
# Created:     09/03/2024
# Copyright:   (c) john.f.kennedy 2024
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os
import sys
import traceback
import inspect

import arcpy  # third-parties second

def preprocessing(project_gdb="", table_names="", clear_folder=True):
    try:
        import dismap_tools

        arcpy.SetLogHistory(
            True
        )  # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(
            1
        )  # 0—A tool will not throw an exception, even if the tool produces an error or warning.
        # 1—If a tool produces a warning or an error, it will throw an exception.
        # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(
            ["NORMAL"]
        )  # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic arcpy.env variables
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"

        # Set varaibales
        project_folder = os.path.dirname(project_gdb)
        scratch_folder = rf"{project_folder}\Scratch"
        scratch_workspace = os.path.join(project_folder, "Scratch\\scratch.gdb")

        # Clear Scratch Folder
        # ClearScratchFolder = True
        # if ClearScratchFolder:
        if clear_folder:
            dismap_tools.clear_folder(folder=rf"{os.path.dirname(project_gdb)}\Scratch")
        else:
            pass
        # del ClearScratchFolder
        del clear_folder

        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = scratch_workspace
        del project_folder, scratch_workspace

        if not table_names:
            table_names = [
                row[0]
                for row in arcpy.da.SearchCursor(
                    os.path.join(project_gdb, "Datasets"),
                    "TableName",
                    where_clause="TableName LIKE '%_IDW'",
                )
            ]
        else:
            pass

        for table_name in table_names:
            arcpy.AddMessage(f"Pre-Processing: {table_name}")

            region_gdb = os.path.join(scratch_folder, f"{table_name}.gdb")
            region_scratch_workspace = os.path.join(
                scratch_folder, f"{table_name}", "scratch.gdb"
            )

            # Create Scratch Workspace for Region
            if not arcpy.Exists(region_scratch_workspace):
                os.makedirs(os.path.join(scratch_folder, table_name))
                if not arcpy.Exists(region_scratch_workspace):
                    arcpy.AddMessage(f"Create File GDB: '{table_name}'")
                    arcpy.management.CreateFileGDB(
                        os.path.join(scratch_folder, f"{table_name}"), "scratch"
                    )
                    arcpy.AddMessage(
                        "\tCreate File GDB: {0}\n".format(
                            arcpy.GetMessages().replace("\n", "\n\t")
                        )
                    )
            del region_scratch_workspace
            # # # CreateFileGDB
            arcpy.AddMessage(f"Creating File GDB: '{table_name}'")
            arcpy.management.CreateFileGDB(rf"{scratch_folder}", f"{table_name}")
            arcpy.AddMessage(
                "\tCreate File GDB: {0}\n".format(
                    arcpy.GetMessages().replace("\n", "\n\t")
                )
            )
            # # # CreateFileGDB
            # # # Datasets
            # Process: Make Table View (Make Table View) (management)
            datasets = rf"{project_gdb}\Datasets"
            arcpy.AddMessage(
                f"'{os.path.basename(datasets)}' has {arcpy.management.GetCount(datasets)[0]} records"
            )
            arcpy.management.Copy(datasets, rf"{region_gdb}\Datasets")
            arcpy.AddMessage(
                "\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t"))
            )
            # # # Datasets

            # # # LayerSpeciesYearImageName
            LayerSpeciesYearImageName = (
                rf"{project_gdb}\{table_name}_LayerSpeciesYearImageName"
            )
            arcpy.AddMessage(
                f"The table '{table_name}_LayerSpeciesYearImageName' has {arcpy.management.GetCount(LayerSpeciesYearImageName)[0]} records"
            )
            arcpy.management.Copy(
                rf"{project_gdb}\{table_name}_LayerSpeciesYearImageName",
                rf"{region_gdb}\{table_name}_LayerSpeciesYearImageName",
            )
            arcpy.AddMessage(
                "\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t"))
            )
            del LayerSpeciesYearImageName
            # # # LayerSpeciesYearImageName

            # # # Raster_Mask
            arcpy.AddMessage(f"Copy Raster Mask for '{table_name}'")
            arcpy.management.Copy(
                rf"{project_gdb}\{table_name}_Raster_Mask",
                rf"{region_gdb}\{table_name}_Raster_Mask",
            )
            arcpy.AddMessage(
                "\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t"))
            )
            # # # Raster_Mask

            del datasets
            # Declared Variables
            del table_name

        # Declared Variables
        del scratch_folder, region_gdb
        # Imports
        del dismap_tools
        # Function Parameters
        del project_gdb, table_names

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

def director(project_gdb="", Sequential=True, table_names=[]):
    try:
        # Imports
        from lxml import etree
        from  io import StringIO
        from arcpy import metadata as md

        # Import the dismap module to access tools
        import dismap_tools
        from create_mosaics_worker import worker

        # Test if passed workspace exists, if not sys.exit()
        if not arcpy.Exists(rf"{project_gdb}"):
            arcpy.AddError(f"{os.path.basename(project_gdb)} is missing!!")
            arcpy.AddError(arcpy.GetMessages(2))
            sys.exit()
        else:
            pass

        # Set History and Metadata logs, set serverity and message level
        arcpy.SetLogHistory(True)  # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(2)  # 0—A tool will not throw an exception, even if the tool produces an error or warning.
        # 1—If a tool produces a warning or an error, it will throw an exception.
        # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(["NORMAL"])  # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic arcpy.env values
        arcpy.env.overwriteOutput = True
        arcpy.env.parallelProcessingFactor = "100%"
        arcpy.env.workspace = project_gdb
        arcpy.env.scratchWorkspace = (rf"{os.path.dirname(project_gdb)}\Scratch\scratch.gdb")

        preprocessing(project_gdb=project_gdb, table_names=table_names, clear_folder=True)

        # Set basic workkpace variables
        project_folder = os.path.dirname(project_gdb)
        project_name   = os.path.basename(project_folder)
        home_folder    = os.path.dirname(project_folder)
        scratch_folder = os.path.join(project_folder, "Scratch")
        csv_data_folder = os.path.join(project_folder, "CSV_Data")

        # Sequential Processing
        if Sequential:
            arcpy.AddMessage("Sequential Processing")
            for i in range(0, len(table_names)):
                arcpy.AddMessage(f"Processing: {table_names[i]}")
                table_name = table_names[i]
                region_gdb = os.path.join(scratch_folder, f"{table_name}.gdb")
                try:
                    worker(region_gdb=region_gdb)
                except SystemExit:
                    arcpy.AddError(arcpy.GetMessages(2))
                    traceback.print_exc()
                    sys.exit()
                del region_gdb, table_name
                del i
        else:
            pass

        # Non-Sequential Processing
        if not Sequential:
            arcpy.AddMessage("Non-Sequential Processing")
            # Imports
            import multiprocessing
            from time import gmtime, localtime, sleep, strftime, time

            arcpy.AddMessage("Start multiprocessing using the ArcGIS Pro pythonw.exe.")
            # Set multiprocessing exe in case we're running as an embedded process, i.e ArcGIS
            # get_install_path() uses a registry query to figure out 64bit python exe if available
            multiprocessing.set_executable(os.path.join(sys.exec_prefix, "pythonw.exe"))
            # Get CPU count and then take 2 away for other process
            _processes = multiprocessing.cpu_count() - 2
            _processes = (
                _processes if len(table_names) >= _processes else len(table_names)
            )
            arcpy.AddMessage(
                f"Creating the multiprocessing Pool with {_processes} processes"
            )
            # Create a pool of workers, keep one cpu free for surfing the net.
            # Let each worker process only handle 1 task before being restarted (in case of nasty memory leaks)
            with multiprocessing.Pool(processes=_processes, maxtasksperchild=1) as pool:
                arcpy.AddMessage("\tPrepare arguments for processing")
                # Use apply_async so we can handle exceptions gracefully
                jobs = {}
                for i in range(0, len(table_names)):
                    try:
                        arcpy.AddMessage(f"Processing: {table_names[i]}")
                        table_name = table_names[i]
                        region_gdb = os.path.join(scratch_folder, f"{table_name}.gdb")
                        jobs[table_name] = pool.apply_async(worker, [region_gdb])
                        del table_name, region_gdb
                    except:  # noqa: E722
                        pool.terminate()
                        traceback.print_exc()
                        sys.exit()
                    del i
                all_finished = False
                # Set a start time so that we can see how log things take
                start_time = time()
                result_completed = {}
                while True:
                    all_finished = True
                    # Elapsed time
                    end_time = time()
                    elapse_time = end_time - start_time
                    arcpy.AddMessage(
                        f"\nStart Time: {strftime('%a %b %d %I:%M %p', localtime(start_time))}"
                    )
                    arcpy.AddMessage("Have the workers finished?")
                    finish_time = strftime("%a %b %d %I:%M %p", localtime())
                    time_elapsed = "Elapsed Time {0} (H:M:S)".format(
                        strftime("%H:%M:%S", gmtime(elapse_time))
                    )
                    arcpy.AddMessage(f"It's {finish_time}\n{time_elapsed}")
                    finish_time = f"{finish_time}.\n\t{time_elapsed}"
                    del time_elapsed
                    for table_name, result in jobs.items():
                        if result.ready():
                            if table_name not in result_completed:
                                result_completed[table_name] = finish_time
                                try:
                                    # wait for and get the result from the task
                                    result.get()
                                except:  # noqa: E722
                                    pool.terminate()
                                    traceback.print_exc()
                                    sys.exit()
                            else:
                                pass
                            arcpy.AddMessage(
                                f"Process {table_name}\n\tFinished on {result_completed[table_name]}"
                            )
                        else:
                            all_finished = False
                            arcpy.AddMessage(f"Process {table_name} is running. . .")
                        del table_name, result
                    del elapse_time, end_time, finish_time
                    if all_finished:
                        break
                    sleep(_processes * 7.5)
                del result_completed
                del start_time
                del all_finished
                arcpy.AddMessage("Close the process pool")
                # close the process pool
                pool.close()
                # wait for all tasks to complete and processes to close
                arcpy.AddMessage(
                    "\tWait for all tasks to complete and processes to close"
                )
                pool.join()
                # Just in case
                pool.terminate()
                del pool
                del jobs
            del _processes
            del time, multiprocessing, localtime, strftime, sleep, gmtime
            arcpy.AddMessage("Done with multiprocessing Pool\n")

        # Post-Processing
        arcpy.AddMessage("Post-Processing Begins")

        crf_folder = os.path.join(project_folder, "CRFs")

        datasets = list()
        walk = arcpy.da.Walk(scratch_folder, datatype=["RasterDataset", "MosaicDataset"])

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                datasets.append(os.path.join(dirpath, filename))
                del filename
            del dirpath, dirnames, filenames
        del walk

        for dataset in datasets:
            datasets_short_path = f".. {'/'.join(dataset.split(os.sep)[-4:])}"
            dataset_name = os.path.basename(dataset)
            dataset_type = arcpy.Describe(dataset).datatype
            region_gdb = os.path.dirname(dataset)

            out_dataset_path = os.path.join(project_gdb, dataset_name)

            # Copy Raster to CRF
            #out_crf_path = os.path.join(project_folder, f"CRFs\\{dataset_name}")

            arcpy.AddMessage(f"\tDataset: '{dataset_name}'")
            arcpy.AddMessage(f"\t\tType:       '{dataset_type}'")
            arcpy.AddMessage(f"\t\tPath:       '{datasets_short_path}'")
            arcpy.AddMessage(f"\t\tRegion GDB: '{os.path.basename(region_gdb)}'")

            if dataset.endswith("Mosaic"):
                if arcpy.Exists(out_dataset_path):
                    arcpy.management.Delete(out_dataset_path)
                else:
                    pass
                arcpy.AddMessage(f"Copy '{dataset_name}'")
                arcpy.management.Copy(
                    in_data         = dataset,
                    out_data        = out_dataset_path,
                    data_type       = "MosaicDataset",
                    associated_data = "MosaicCatalogItemCategoryDomain 'CV domain' MosaicCatalogItemCategoryDomain DEFAULTS",
                )
                arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

                # Add boilerplate metadata to dataset
                # Version Code
                version_code = dismap_tools.date_code(project_name)
                # Boilerplate
                contacts = rf"{home_folder}\Initial-Data\DisMAP-Contacts-{version_code}.xml"
                # Reads XML, pretty format, and write back the contacts XML
                etree.parse(contacts, parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)).write(contacts, pretty_print=True, xml_declaration=True, encoding="UTF-8") # pyright: ignore[reportAttributeAccessIssue]

                # Create Metadata object for new table
                dataset_md = md.Metadata(out_dataset_path)
                dataset_md.importMetadata(contacts, "ARCGIS_METADATA")
                dataset_md.save()
                dataset_md.synchronize("ALWAYS")
                dataset_md.save()
                del dataset_md

                arcpy.AddMessage(f"\t\tAlter Fields for: '{os.path.basename(out_dataset_path)}'")
                dismap_tools.alter_fields(csv_data_folder, out_dataset_path)

                dataset_md = md.Metadata(out_dataset_path)
                dataset_md.synchronize("SELECTIVE")
                dataset_md.save()
                del dataset_md

                arcpy.AddMessage(f"\t\tImport Metadata for: '{os.path.basename(out_dataset_path)}'")
                dismap_tools.import_metadata(project_folder, out_dataset_path)

                dataset_md = md.Metadata(out_dataset_path)
                dataset_md.synchronize("ALWAYS")
                dataset_md.save()
                del dataset_md

                dataset_md  = md.Metadata(out_dataset_path)
                tree = etree.parse(StringIO(dataset_md.xml), parser=etree.XMLParser(encoding="UTF-8", remove_blank_text=True))
                root = tree.getroot()
                etree.indent(root, space="\t")
                dataset_md.xml = etree.tostring(tree, encoding="UTF-8", method="xml", xml_declaration=True, pretty_print=True,)
                dataset_md.save()
                del dataset_md
                del tree, root

            elif dataset.endswith(".crf"):
                out_crf_path = os.path.join(crf_folder, dataset_name)
                if arcpy.Exists(out_crf_path):
                    pass
                    # arcpy.management.Delete(out_crf_path)
                else:
                    pass
                arcpy.AddMessage(f"Copy '{dataset_name}'")
                arcpy.management.Copy(
                    in_data         = dataset,
                    out_data        = out_crf_path,
                    data_type       = "MosaicDataset",
                    associated_data = "MosaicCatalogItemCategoryDomain 'CV domain' MosaicCatalogItemCategoryDomain DEFAULTS",)
                arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

                # Add boilerplate metadata to dataset
                # Version Code
                version_code = dismap_tools.date_code(project_name)
                # Boilerplate
                contacts = rf"{home_folder}\Initial-Data\DisMAP-Contacts-{version_code}.xml"
                # Reads XML, pretty format, and write back the contacts XML
                etree.parse(contacts, parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)).write(contacts, pretty_print=True, xml_declaration=True, encoding="UTF-8") # pyright: ignore[reportAttributeAccessIssue]

                # Create Metadata object for new table
                dataset_md = md.Metadata(out_crf_path)
                dataset_md.importMetadata(contacts, "ARCGIS_METADATA")
                dataset_md.save()
                dataset_md.synchronize("ALWAYS")
                dataset_md.save()
                del dataset_md

                arcpy.AddMessage(f"\t\tImport Metadata for: '{os.path.basename(out_crf_path)}'")
                dismap_tools.import_metadata(project_folder, out_crf_path)

                dataset_md  = md.Metadata(out_crf_path)
                tree = etree.parse(StringIO(dataset_md.xml), parser=etree.XMLParser(encoding="UTF-8", remove_blank_text=True))
                root = tree.getroot()
                etree.indent(root, space="\t")
                dataset_md.xml = etree.tostring(tree, encoding="UTF-8", method="xml", xml_declaration=True, pretty_print=True,)
                dataset_md.save()
                del dataset_md
                del tree, root

            #arcpy.management.Delete(dataset)
            #arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", "\n\t")))

            del region_gdb, dataset_name, datasets_short_path, dataset_type
            del dataset
        del datasets

        arcpy.AddMessage(f"Compacting the {os.path.basename(project_gdb)} GDB")
        arcpy.management.Compact(project_gdb)
        arcpy.AddMessage("\t" + arcpy.GetMessages().replace("\n", "\n\t"))
        # Declared Variables assigned in function
        del scratch_folder, crf_folder # csv_data_folder
        # Imports
        del worker, dismap_tools
        # Function Parameters
        del project_gdb, Sequential, table_names

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

        # Set varaibales
        project_name   = os.path.basename(project_folder)
        project_gdb    = os.path.join(project_folder, f"{project_name}.gdb")
        #scratch_folder = rf"{project_folder}\Scratch"

        ##        # Clear Scratch Folder
        ##        ClearScratchFolder = False
        ##        if ClearScratchFolder:
        ##            import dismap_tools
        ##            dismap_tools.clear_folder(folder=scratch_folder)
        ##            del dismap_tools
        ##        else:
        ##            pass
        ##        del ClearScratchFolder

        try:
            # "AI_IDW", "EBS_IDW", "ENBS_IDW", "GMEX_IDW", "GOA_IDW", "HI_IDW", "NBS_IDW", "NEUS_FAL_IDW", "NEUS_SPR_IDW",
            # "SEUS_FAL_IDW", "SEUS_SPR_IDW", "SEUS_SUM_IDW", "WC_ANN_IDW", "WC_TRI_IDW",
            Test = False
            if Test:
                director(
                    project_gdb=project_gdb,
                    Sequential=True,
                    table_names=["HI_IDW",],
                    )
            elif not Test:
                director(
                    project_gdb=project_gdb,
                    Sequential=True,
                    table_names=[
                        "AI_IDW",
                        "EBS_IDW",
                        "ENBS_IDW",
                        "GMEX_IDW",
                        "GOA_IDW",
                        "HI_IDW",
                        "NBS_IDW",
                    ],
                )
                director(
                    project_gdb=project_gdb,
                    Sequential=True,
                    table_names=[
                        "NEUS_FAL_IDW",
                        "NEUS_SPR_IDW",
                        "SEUS_FAL_IDW",
                        "SEUS_SPR_IDW",
                        "SEUS_SUM_IDW",
                        "WC_ANN_IDW",
                        "WC_TRI_IDW",
                    ],
                )
            else:
                pass
            del Test

        except:  # noqa: E722
            arcpy.AddError(arcpy.GetMessages(2))
            traceback.print_exc()
            sys.exit()

        # Declared Variables

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
        arcpy.AddMessage(f"{'--The End' * 10}--")

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
