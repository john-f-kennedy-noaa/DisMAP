"""
Script documentation
- Tool parameters are accessed using arcpy.GetParameter() or
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy
import traceback, os, sys
def script_tool(home_folder, source_zip_file):
    """Script code goes below"""
    try:
        import copy
        from zipfile import ZipFile
        from arcpy import metadata as md
        from lxml import etree
        from io import StringIO, BytesIO

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        #aprx.save()
        home_folder = aprx.homeFolder
        arcpy.AddMessage(home_folder)
        out_data_path = rf"{home_folder}\CSV_Data"
        import json
        json_path = rf"{out_data_path}\root_dict.json"
        with open(json_path, "r") as json_file:
            root_dict = json.load(json_file)
        del json_file
        del json_path
        del json
        arcpy.AddMessage(out_data_path)
        # Change Directory
        os.chdir(out_data_path)
        arcpy.AddMessage(f"Un-Zipping files from {os.path.basename(source_zip_file)}")
        with ZipFile(source_zip_file, mode="r") as archive:
            for file in archive.namelist():
                archive.extract(file, ".")
                del file
        del archive
        arcpy.AddMessage(f"Done Un-Zipping files from {os.path.basename(source_zip_file)}")
        tmp_workspace = arcpy.env.workspace
        arcpy.env.workspace = rf"{out_data_path}\python"
        csv_files = arcpy.ListFiles("*_survey.csv")
        arcpy.AddMessage("Copying CSV Files and renameing the file")
        for csv_file in csv_files:
            arcpy.management.Copy(rf"{out_data_path}\python\{csv_file}", rf"{out_data_path}\{csv_file.replace('_survey', '_IDW')}")
            del csv_file
        del csv_files
        arcpy.env.workspace = tmp_workspace
        del tmp_workspace
        if arcpy.Exists(rf"{out_data_path}\python"):
            arcpy.AddMessage("Removing the extract folder")
            arcpy.management.Delete(rf"{out_data_path}\python")
        else:
            pass
        arcpy.AddMessage(f"Adding metadata to CSV file")
        tmp_workspace = arcpy.env.workspace
        arcpy.env.workspace = out_data_path
        contacts = rf"{os.path.dirname(home_folder)}\Datasets\DisMAP Contacts 2025 08 01.xml"
        csv_files = arcpy.ListFiles("*_IDW.csv")
        for csv_file in csv_files:
            arcpy.AddMessage(f"\t{csv_file}")
            dataset_md = md.Metadata(rf"{out_data_path}\{csv_file}")
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()
            dataset_md.importMetadata(contacts, "ARCGIS_METADATA")
            dataset_md.save()
            dataset_md.synchronize("OVERWRITE")
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()
            target_tree = etree.parse(StringIO(dataset_md.xml), parser=etree.XMLParser(encoding='UTF-8', remove_blank_text=True)) # type: ignore
            target_root = target_tree.getroot()
            target_root[:] = sorted(target_root, key=lambda x: root_dict[x.tag])
            new_item_name = target_root.find("Esri/DataProperties/itemProps/itemName").text
            arcpy.AddMessage(new_item_name)
##            onLineSrcs = target_root.findall("distInfo/distTranOps/onLineSrc")
##            #arcpy.AddMessage(onLineSrcs)
##            for onLineSrc in onLineSrcs:
##                if onLineSrc.find('./protocol').text == "ESRI REST Service":
##                    old_linkage_element = onLineSrc.find('./linkage')
##                    old_linkage = old_linkage_element.text
##                    #arcpy.AddMessage(old_linkage)
##                    old_item_name = old_linkage[old_linkage.find("/services/")+len("/services/"):old_linkage.find("/FeatureServer")]
##                    new_linkage = old_linkage.replace(old_item_name, new_item_name)
##                    #arcpy.AddMessage(new_linkage)
##                    old_linkage_element.text = new_linkage
##                    #arcpy.AddMessage(old_linkage_element.text)
##                    del old_linkage_element
##                    del old_item_name, old_linkage, new_linkage
##                    onLineSrc.find('./orName').text = f"{new_item_name} Feature Service"
##            del onLineSrcs, new_item_name
            etree.indent(target_root, space='    ') # pyright: ignore[reportAttributeAccessIssue]
            dataset_md.xml = etree.tostring(target_tree, encoding='UTF-8', method='xml', xml_declaration=True, pretty_print=True) # pyright: ignore[reportAttributeAccessIssue]
            dataset_md.save()
            dataset_md.synchronize("ALWAYS")
            dataset_md.save()

            del dataset_md

            del csv_file
        del csv_files
        arcpy.env.workspace = tmp_workspace
        del tmp_workspace
        del home_folder
        del source_zip_file
        del md
        return out_data_path
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
    except:
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
    else:
        pass
    finally:
        pass
        del out_data_path
if __name__ == "__main__":
    try:
        home_folder = arcpy.GetParameterAsText(0)
        if not home_folder:
           home_folder = rf"{os.path.expanduser('~')}\Documents\ArcGIS\Projects\DisMAP\ArcGIS-Analysis-Python\August 1 2025"
        else:
           pass
           
        source_zip_file = arcpy.GetParameterAsText(1)            
        if not source_zip_file:
            source_zip_file = rf"{os.path.expanduser('~')}\Documents\ArcGIS\Projects\DisMAP\ArcGIS-Analysis-Python\Datasets\CSV Data 2025 08 01.zip"
        else:
           pass
           
        script_tool(home_folder, source_zip_file)
        arcpy.SetParameterAsText(2, "Result")
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
    except:
        import traceback
        traceback.print_exc()
        arcpy.AddError(arcpy.GetMessages(2))
