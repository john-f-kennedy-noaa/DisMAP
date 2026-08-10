"""
Script documentation
- Tool parameters are accessed using arcpy.GetParameter() or
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import os
import traceback
import inspect

import arcpy

def script_tool(project_folder=""):
    """Script code goes below"""
    try:
        from lxml import etree
        from io import StringIO
        from zipfile import ZipFile
        import json
        import shutil

        from arcpy import metadata as md

        import dismap_tools

        arcpy.env.overwriteOutput = True

        # aprx = arcpy.mp.ArcGISProject("CURRENT")
        # aprx.save()
        # project_folder = aprx.homeFolder
        arcpy.AddMessage(project_folder)

        project_name    = os.path.basename(project_folder)
        project_gdb     = os.path.join(project_folder, f"{project_name}.gdb")  # noqa: F841
        home_folder     = os.path.dirname(project_folder)
        csv_data_folder = os.path.join(project_folder, "CSV_Data")  # noqa: F841
        dataset_shapefiles_folder = rf"{project_folder}\Dataset_Shapefiles"  # noqa: F841

        dataset_shapefiles = os.path.join(home_folder, f"Initial-Data\\Dataset-Shapefiles-{dismap_tools.date_code(project_name)}.zip")

## for i in range(0, len(alist)):
##...     print(alist[i].replace('Dataset-Shapefiles-20260601/', 'Dataset_Shapefiles/'))
##...

        arcpy.AddMessage(dataset_shapefiles)
        # Change Directory
        os.chdir(project_folder)
        arcpy.AddMessage(f"Un-Zipping files from {os.path.basename(dataset_shapefiles)}")
        #print(arcpy.Exists(dataset_shapefiles))
        with ZipFile(dataset_shapefiles, mode="r") as archive:
            for file in archive.namelist():
                archive.extract(file, ".")
                del file
        del archive
        arcpy.AddMessage(f"Done Un-Zipping files from {os.path.basename(dataset_shapefiles)}")

        # Change Directory
        #os.chdir(os.path.join(project_folder, os.path.basename(dataset_shapefiles))

        tmp_workspace = arcpy.env.workspace
        arcpy.env.workspace = os.path.join(project_folder, os.path.basename(dataset_shapefiles).replace(".zip", ""))

        #print(arcpy.env.workspace)

        folders = arcpy.ListWorkspaces(workspace_type="Folder")

        for folder in folders:
            print(folder)

            destination_folder = os.path.join(dataset_shapefiles_folder, os.path.basename(folder))

            # Safely merges contents into an existing folder
            shutil.copytree(folder, destination_folder, dirs_exist_ok=True)

            del destination_folder

        # Delete extract folder
        arcpy.management.Delete(os.path.join(project_folder, os.path.basename(dataset_shapefiles).replace(".zip", "")))

        arcpy.env.workspace = tmp_workspace
        del tmp_workspace

        csv_data_file = os.path.join(home_folder, f"Initial-Data\\CSV-Data-{dismap_tools.date_code(project_name)}.zip")
        contacts_file = os.path.join(home_folder, f"InitialData\\DisMAP-Contacts-{dismap_tools.date_code(project_name)}.xml")

        json_path = rf"{csv_data_folder}\root_dict.json"
        with open(json_path, "r", encoding='utf-8') as json_file:
            root_dict = json.load(json_file)  # noqa: F841
        del json_file
        del json_path

        arcpy.AddMessage(csv_data_folder)
        arcpy.AddMessage(csv_data_file)
        # Change Directory
        os.chdir(csv_data_folder)
        arcpy.AddMessage(f"Un-Zipping files from {os.path.basename(csv_data_file)}")
        print(arcpy.Exists(csv_data_file))
        with ZipFile(csv_data_file, mode="r") as archive:
            for file in archive.namelist():
                archive.extract(file, ".")
                del file
        del archive
        arcpy.AddMessage(f"Done Un-Zipping files from {os.path.basename(csv_data_file)}")

        tmp_workspace = arcpy.env.workspace
        arcpy.env.workspace = rf"{csv_data_folder}\python"

        csv_files = arcpy.ListFiles("*_survey.csv")

        arcpy.AddMessage("Copying CSV Files and renaming the file")
        for csv_file in csv_files:
            arcpy.management.Copy(rf"{csv_data_folder}\python\{csv_file}",
                                  rf"{csv_data_folder}\{csv_file.replace('_survey', '_IDW')}",
            )
            del csv_file
        del csv_files

        arcpy.env.workspace = tmp_workspace
        del tmp_workspace

        if arcpy.Exists(rf"{csv_data_folder}\python"):
            arcpy.AddMessage("Removing the extract folder")
            arcpy.management.Delete(rf"{csv_data_folder}\python")
        else:
            pass

        arcpy.AddMessage("Adding metadata to CSV file")
        tmp_workspace = arcpy.env.workspace
        arcpy.env.workspace = csv_data_folder

        csv_files = arcpy.ListFiles("*_IDW.csv")
        for csv_file in csv_files:
            arcpy.AddMessage(f"\t{csv_file}")
            dataset_md = md.Metadata(rf"{csv_data_folder}\{csv_file}")
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()
            dataset_md.importMetadata(contacts_file, "ARCGIS_METADATA")
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()
            target_tree = etree.parse(
                StringIO(dataset_md.xml),
                parser=etree.XMLParser(encoding="UTF-8", remove_blank_text=True),
            )
            target_root = target_tree.getroot()
            target_root[:] = sorted(target_root, key=lambda x: root_dict[x.tag])
            new_item_name = target_root.find(
                "Esri/DataProperties/itemProps/itemName"
            ).text
            arcpy.AddMessage(new_item_name)
              #^onLineSrcs = target_root.findall("distInfo/distTranOps/onLineSrc")
              #^#arcpy.AddMessage(onLineSrcs)
              #^for onLineSrc in onLineSrcs:
              #^    if onLineSrc.find('./protocol').text == "ESRI REST Service":
              #^        old_linkage_element = onLineSrc.find('./linkage')
              #^        old_linkage = old_linkage_element.text
              #^        #arcpy.AddMessage(old_linkage)
              #^        old_item_name = old_linkage[old_linkage.find("/services/")+len("/services/"):old_linkage.find("/FeatureServer")]
              #^        new_linkage = old_linkage.replace(old_item_name, new_item_name)
              #^        #arcpy.AddMessage(new_linkage)
              #^        old_linkage_element.text = new_linkage
              #^        #arcpy.AddMessage(old_linkage_element.text)
              #^        del old_linkage_element
              #^        del old_item_name, old_linkage, new_linkage
              #^        onLineSrc.find('./orName').text = f"{new_item_name} Feature Service"
              #^del onLineSrcs, new_item_name
            etree.indent(target_root, space="    ")
            dataset_md.xml = etree.tostring(
                target_tree,
                encoding="UTF-8",
                method="xml",
                xml_declaration=True,
                pretty_print=True,
            )
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()

            del dataset_md

            del csv_file
        del csv_files

        arcpy.env.workspace = tmp_workspace
        del tmp_workspace

    except arcpy.ExecuteWarning:
        arcpy.AddWarning(
            f"ArcPy Execute Warning in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(1)}"
        )
    except arcpy.ExecuteError:
        arcpy.AddError(
            f"ArcPy Execute Error in '{inspect.stack()[0][3]}':\n{arcpy.GetMessages(2)}"
        )
        arcpy.AddError("Traceback:\n")
        traceback.print_exc()
    except SystemExit:
        # This is not an error, so we allow the script to exit.
        pass
    except Exception as e:
        arcpy.AddError(
            f"An unexpected error occurred in '{inspect.stack()[0][3]}': {e}"
        )
        arcpy.AddError("Traceback:")
        traceback.print_exc()
    else:
        arcpy.AddMessage("\nScript finished successfully.\n")
    finally:
        arcpy.AddMessage(f"\n{'--End' * 10}--")

if __name__ == "__main__":
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

        arcpy.SetParameterAsText(1, True)

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
