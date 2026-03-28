# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        create_species_year_image_name_table_director
# Purpose:
#
# Author:      john.f.kennedy
#
# Created:     09/03/2024
# Copyright:   (c) john.f.kennedy 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys # built-ins first
import traceback
import inspect

import arcpy # third-parties second

def director(project_gdb="", Sequential=True, table_names=[]):
    try:
        # Imports
        import dismap_tools
        from create_mosaics_worker import preprocessing, worker

        # Test if passed workspace exists, if not sys.exit()
        if not arcpy.Exists(rf"{project_gdb}"):
            arcpy.AddError(f"{os.path.basename(project_gdb)} is missing!!")
            arcpy.AddError(arcpy.GetMessages(2))
            sys.exit()
        else:
            pass

        # Set History and Metadata logs, set serverity and message level
        arcpy.SetLogHistory(True) # Look in %AppData%\Roaming\Esri\ArcGISPro\ArcToolbox\History
        arcpy.SetLogMetadata(True)
        arcpy.SetSeverityLevel(2) # 0—A tool will not throw an exception, even if the tool produces an error or warning.
                                  # 1—If a tool produces a warning or an error, it will throw an exception.
                                  # 2—If a tool produces an error, it will throw an exception. This is the default.
        arcpy.SetMessageLevels(['NORMAL']) # NORMAL, COMMANDSYNTAX, DIAGNOSTICS, PROJECTIONTRANSFORMATION

        # Set basic arcpy.env values
        arcpy.env.overwriteOutput          = True
        arcpy.env.parallelProcessingFactor = "100%"
        arcpy.env.workspace                = project_gdb
        arcpy.env.scratchWorkspace         = rf"{os.path.dirname(project_gdb)}\Scratch\scratch.gdb"

        preprocessing(project_gdb=project_gdb, table_names=table_names, clear_folder=True)

        # Set basic workkpace variables
        scratch_folder  = rf"{os.path.dirname(project_gdb)}\Scratch"
        csv_data_folder = rf"{os.path.dirname(project_gdb)}\CSV_Data"

        # Sequential Processing
        if Sequential:
            arcpy.AddMessage(f"Sequential Processing")
            for i in range(0, len(table_names)):
                arcpy.AddMessage(f"Processing: {table_names[i]}")
                table_name = table_names[i]
                region_gdb = rf"{scratch_folder}\{table_name}.gdb"
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
            arcpy.AddMessage(f"Non-Sequential Processing")
            # Imports
            import multiprocessing
            from time import time, localtime, strftime, sleep, gmtime
            arcpy.AddMessage(f"Start multiprocessing using the ArcGIS Pro pythonw.exe.")
            #Set multiprocessing exe in case we're running as an embedded process, i.e ArcGIS
            #get_install_path() uses a registry query to figure out 64bit python exe if available
            multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))
            # Get CPU count and then take 2 away for other process
            _processes = multiprocessing.cpu_count() - 2
            _processes = _processes if len(table_names) >= _processes else len(table_names)
            arcpy.AddMessage(f"Creating the multiprocessing Pool with {_processes} processes")
            #Create a pool of workers, keep one cpu free for surfing the net.
            #Let each worker process only handle 1 task before being restarted (in case of nasty memory leaks)
            with multiprocessing.Pool(processes=_processes, maxtasksperchild=1) as pool:
                arcpy.AddMessage(f"\tPrepare arguments for processing")
                # Use apply_async so we can handle exceptions gracefully
                jobs={}
                for i in range(0, len(table_names)):
                    try:
                        arcpy.AddMessage(f"Processing: {table_names[i]}")
                        table_name = table_names[i]
                        region_gdb = rf"{scratch_folder}\{table_name}.gdb"
                        jobs[table_name] = pool.apply_async(worker, [region_gdb])
                        del table_name, region_gdb
                    except:
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
                    elapse_time =  end_time - start_time
                    arcpy.AddMessage(f"\nStart Time: {strftime('%a %b %d %I:%M %p', localtime(start_time))}")
                    arcpy.AddMessage(f"Have the workers finished?")
                    finish_time = strftime('%a %b %d %I:%M %p', localtime())
                    time_elapsed = u"Elapsed Time {0} (H:M:S)".format(strftime("%H:%M:%S", gmtime(elapse_time)))
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
                                except:
                                    pool.terminate()
                                    traceback.print_exc()
                                    sys.exit()
                            else:
                                pass
                            arcpy.AddMessage(f"Process {table_name}\n\tFinished on {result_completed[table_name]}")
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
                arcpy.AddMessage(f"Close the process pool")
                # close the process pool
                pool.close()
                # wait for all tasks to complete and processes to close
                arcpy.AddMessage(f"\tWait for all tasks to complete and processes to close")
                pool.join()
                # Just in case
                pool.terminate()
                del pool
                del jobs
            del _processes
            del time, multiprocessing, localtime, strftime, sleep, gmtime
            arcpy.AddMessage(f"Done with multiprocessing Pool\n")

        # Post-Processing
        arcpy.AddMessage("Post-Processing Begins")

        crf_folder = rf"{os.path.dirname(project_gdb)}\CRFs"

        datasets = list()
        walk = arcpy.da.Walk(scratch_folder, datatype=["RasterDataset", "MosaicDataset"])
        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                datasets.append(os.path.join(dirpath, filename))
                del filename
            del dirpath, dirnames, filenames
        del walk
        for dataset in datasets:
            datasets_short_path = f"{os.path.basename(os.path.dirname(os.path.dirname(dataset)))}\{os.path.basename(os.path.dirname(dataset))}\{os.path.basename(dataset)}"
            dataset_name = os.path.basename(dataset)
            dataset_type = arcpy.Describe(dataset).datatype
            region_gdb   = os.path.dirname(dataset)
            arcpy.AddMessage(f"\tDataset: '{dataset_name}'")
            arcpy.AddMessage(f"\t\tType:       '{dataset_type}'")
            arcpy.AddMessage(f"\t\tPath:       '{datasets_short_path}'")
            arcpy.AddMessage(f"\t\tRegion GDB: '{os.path.basename(region_gdb)}'")
            if dataset.endswith("Mosaic"):
                try:
                    if arcpy.Exists(rf"{project_gdb}\{dataset_name}"):
                        arcpy.management.Delete(rf"{project_gdb}\{dataset_name}")
                    else:
                        pass
                    arcpy.AddMessage(f"Copy '{dataset_name}'")
                    arcpy.management.Copy(in_data         = dataset,
                                          out_data        = rf"{project_gdb}\{dataset_name}",
                                          data_type       = "MosaicDataset",
                                          associated_data = "MosaicCatalogItemCategoryDomain 'CV domain' MosaicCatalogItemCategoryDomain DEFAULTS")
                    arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
                    #arcpy.AddMessage(f"\t\tAlter Fields for: '{dataset_name}'")
                    #dismap_tools.alter_fields(csv_data_folder, rf"{project_gdb}\{dataset_name}")
                    dismap_tools.import_metadata(csv_data_folder, rf"{project_gdb}\{dataset_name}")
                except arcpy.ExecuteWarning:
                    arcpy.AddWarning(arcpy.GetMessages(1))
                except arcpy.ExecuteError:
                    arcpy.AddError(arcpy.GetMessages(2))
                    traceback.print_exc()
                    sys.exit()

            elif dataset.endswith(".crf"):
                try:
                    if arcpy.Exists(rf"{crf_folder}\{dataset_name}"):
                        arcpy.management.Delete(rf"{crf_folder}\{dataset_name}")
                    else:
                        pass
                    arcpy.AddMessage(f"Copy '{dataset_name}'")
                    arcpy.management.Copy(in_data         = dataset,
                                          out_data        = rf"{crf_folder}\{dataset_name}",
                                          data_type       = "MosaicDataset",
                                          associated_data = "MosaicCatalogItemCategoryDomain 'CV domain' MosaicCatalogItemCategoryDomain DEFAULTS")
                    arcpy.AddMessage("\tCopy: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
                    dismap_tools.import_metadata(csv_data_folder, rf"{project_gdb}\{dataset_name}")
                except arcpy.ExecuteWarning:
                    arcpy.AddWarning(arcpy.GetMessages(1))
                except arcpy.ExecuteError:
                    arcpy.AddError(arcpy.GetMessages(2))
                    traceback.print_exc()
                    raise SystemExit
            else:
                pass
            arcpy.management.Delete(dataset)
            arcpy.AddMessage("\tDelete: {0}\n".format(arcpy.GetMessages().replace("\n", '\n\t')))
            del region_gdb, dataset_name, datasets_short_path, dataset_type
            del dataset
        del datasets

        arcpy.AddMessage(f"Compacting the {os.path.basename(project_gdb)} GDB")
        arcpy.management.Compact(project_gdb)
        arcpy.AddMessage("\t"+arcpy.GetMessages().replace("\n", "\n\t"))
        # Declared Variables assigned in function
        del scratch_folder, csv_data_folder, crf_folder
        # Imports
        del preprocessing, worker, dismap_tools
        # Function Parameters
        del project_gdb, Sequential, table_names

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

        # Clear Scratch Folder
        ClearScratchFolder = False
        if ClearScratchFolder:
            import dismap_tools
            dismap_tools.clear_folder(folder=scratch_folder)
            del dismap_tools
        else:
            pass
        del ClearScratchFolder

        try:
            # "AI_IDW", "EBS_IDW", "ENBS_IDW", "GMEX_IDW", "GOA_IDW", "HI_IDW", "NBS_IDW", "NEUS_FAL_IDW", "NEUS_SPR_IDW",
            # "SEUS_FAL_IDW", "SEUS_SPR_IDW", "SEUS_SUM_IDW", "WC_ANN_IDW", "WC_TRI_IDW",
            Test = True
            if Test:
                director(project_gdb=project_gdb, Sequential=True, table_names=["SEUS_FAL_IDW"])
            elif not Test:
                #director(project_gdb=project_gdb, Sequential=False, table_names=["NBS_IDW", "ENBS_IDW", "HI_IDW"])
                #director(project_gdb=project_gdb, Sequential=True, table_names=["SEUS_FAL_IDW", "SEUS_SPR_IDW", "SEUS_SUM_IDW",])
                #director(project_gdb=project_gdb, Sequential=False, table_names=["WC_TRI_IDW", "AI_IDW", "GMEX_IDW"])
                #director(project_gdb=project_gdb, Sequential=False, table_names=["GOA_IDW", "WC_ANN_IDW", "NEUS_FAL_IDW",])
                director(project_gdb=project_gdb, Sequential=True, table_names=["NEUS_FAL_IDW", "NEUS_SPR_IDW"])
            else:
                pass
            del Test

        except:
            arcpy.AddError(arcpy.GetMessages(2))
            traceback.print_exc()
            sys.exit()

        # Declared Variables

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
        arcpy.AddError(f"Caught an KeyboardInterrupt in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        sys.exit()
    except arcpy.ExecuteWarning:
        arcpy.AddWarning(f"Caught an arcpy.ExecuteWarning error in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        arcpy.AddWarning(arcpy.GetMessages(1))
        traceback.print_exc()
        sys.exit()
    except arcpy.ExecuteError:
        arcpy.AddError(f"Caught an arcpy.ExecuteError error in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
        sys.exit()
    except SystemExit as se:
        arcpy.AddError(f"Caught an SystemExit error: '{se}' in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        sys.exit()
    except Exception as e:
        arcpy.AddError(f"Caught an Exception error: '{e}' in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        traceback.print_exc()
        sys.exit()
    except:
        arcpy.AddError(f"Caught an except error in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}.")
        traceback.print_exc()
        sys.exit()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith('__')]
        if rk: arcpy.AddMessage(f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##"); del rk
        return True
    finally:
        if "Test" in locals().keys(): del Test

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