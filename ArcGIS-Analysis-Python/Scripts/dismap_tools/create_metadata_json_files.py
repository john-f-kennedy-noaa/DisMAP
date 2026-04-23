"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""

import inspect
import os
import sys
import traceback

import arcpy


def script_tool(project_gdb=""):
    """Script code goes below"""
    try:
        from time import gmtime, localtime, strftime, time

        # Set a start time so that we can see how log things take
        start_time = time()
        arcpy.AddMessage(f"{'-' * 80}")
        arcpy.AddMessage(f"Python Script: {os.path.basename(__file__)}")
        arcpy.AddMessage(f"Location:       .. {'/'.join(__file__.split(os.sep)[-4:])}")
        arcpy.AddMessage(f"Python Version: {sys.version}")
        arcpy.AddMessage(f"Environment:    {os.path.basename(sys.exec_prefix)}")
        arcpy.AddMessage(
            f"Start Time:     {strftime('%a %b %d %I:%M %p', localtime(start_time))}"
        )
        arcpy.AddMessage(f"{'-' * 80}\n")

        arcpy.AddMessage("Creating JSON configuration files for metadata...")
        project_folder = os.path.dirname(project_gdb)
        out_data_path = os.path.join(project_folder, "CSV_Data")

        root_dict = {
            "Esri": 0,
            "dataIdInfo": 1,
            "dqInfo": 2,
            "distInfo": 3,
            "mdContact": 4,
            "mdLang": 5,
            "mdChar": 6,
            "mdDateSt": 7,
            "mdHrLv": 8,
            "mdHrLvName": 9,
            "mdFileID": 10,
            "mdParentID": 11,
            "mdMaint": 12,
            "refSysInfo": 13,
            "spatRepInfo": 14,
            "spdoinfo": 15,
            "spref": 16,
            "contInfo": 17,
            "dataSetFn": 18,
            "eainfo": 19,
            "Binary": 20,
        }

        import json

        json_path = os.path.join(out_data_path, "root_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(root_dict, json_file, indent=4)

        esri_dict = {
            "CreaDate": 0,
            "CreaTime": 1,
            "ArcGISFormat": 2,
            "ArcGISstyle": 3,
            "ArcGISProfile": 4,
            "SyncOnce": 5,
            "DataProperties": 6,
            "lineage": 0,
            "itemProps": 1,
            "itemName": 0,
            "imsContentType": 1,
            "nativeExtBox": 2,
            "westBL": 0,
            "eastBL": 1,
            "southBL": 2,
            "northBL": 3,
            "exTypeCode": 4,
            "itemLocation": 3,
            "linkage": 0,
            "protocol": 1, # noqa: E261
            "coordRef": 4,
            "type": 0,
            "geogcsn": 1,
            "csUnits": 2,
            "projcsn": 3,
            "peXml": 4,
            "SyncDate": 7,
            "SyncTime": 8,
            "ModDate": 9,
            "ModTime": 10,
            "scaleRange": 11,
            "minScale": 12,
            "maxScale": 13,
            "locales": 14,
        }

        json_path = os.path.join(out_data_path, "esri_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(esri_dict, json_file, indent=4)

        dataIdInfo_dict = {
            "dataIdInfo": 0,
            "envirDesc": 0,
            "dataLang": 1,
            "dataChar": 2,
            "idCitation": 3,
            "resTitle": 0,
            "resAltTitle": 1,
            "collTitle": 2, # noqa: E261
            "date": 3,
            "presForm": 4,
            "PresFormCd": 0,
            "fgdcGeoform": 1,
            "citRespParty": 5,
            "spatRpType": 4,
            "dataExt": 5,
            "exDesc": 0,
            "geoEle": 1,
            "GeoBndBox": 0, # noqa: E261
            "exTypeCode": 0,
            "westBL": 1,
            "eastBL": 2,
            "northBL": 3,
            "southBL": 4,
            "tempEle": 2,
            "TempExtent": 0,
            "exTemp": 0,
            "TM_Period": 0,
            "tmBegin": 0, # noqa: E261
            "tmEnd": 1,
            "TM_Instant": 1,
            "tmPosition": 0,
            "searchKeys": 1,
            "idPurp": 2,
            "idAbs": 3,
            "idCredit": 4,
            "idStatus": 5,
            "resConst": 6,
            "discKeys": 7, # noqa: E261
            "keyword": 0,
            "thesaName": 1,
            "resTitle": 0,
            "date": 1,
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citOnlineRes": 2, # noqa: E261
            "linkage": 0,
            "orFunct": 1,
            "OnFunctCd": 0,
            "thesaLang": 2,
            "languageCode": 0,
            "countryCode": 1,
            "themeKeys": 8,
            "keyword": 0,
            "thesaName": 1,
            "resTitle": 0,
            "date": 1, # noqa: E261
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citOnlineRes": 2,
            "linkage": 0,
            "orFunct": 1,
            "OnFunctCd": 0,
            "thesaLang": 2,
            "languageCode": 0,
            "countryCode": 1,
            "placeKeys": 9,
            "keyword": 0,
            "thesaName": 1,
            "resTitle": 0,
            "date": 1, # noqa: E261
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citOnlineRes": 2,
            "linkage": 0,
            "orFunct": 1,
            "OnFunctCd": 0,
            "thesaLang": 2,
            "languageCode": 0,
            "countryCode": 1,
            "tempKeys": 10,
            "keyword": 0,
            "thesaName": 1,
            "resTitle": 0,
            "date": 1, # noqa: E261
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citOnlineRes": 2,
            "linkage": 0,
            "orFunct": 1,
            "OnFunctCd": 0,
            "thesaLang": 2,
            "languageCode": 0,
            "countryCode": 1,
            "otherKeys": 11,
            "keyword": 0,
            "thesaName": 1,
            "resTitle": 0,
            "date": 1, # noqa: E261
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citOnlineRes": 2,
            "linkage": 0,
            "orFunct": 1,
            "OnFunctCd": 0,
            "thesaLang": 2,
            "languageCode": 0,
            "countryCode": 1,
            "idPoC": 11, # noqa: E261
            "resMaint": 12,
            "tpCat": 18,
        }

        json_path = os.path.join(out_data_path, "dataIdInfo_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(dataIdInfo_dict, json_file, indent=4)

        idCitation_dict = {
            "idCitation": 0,
            "resTitle": 0,
            "resAltTitle": 1,
            "collTitle": 2, # noqa: E261
            "presForm": 3,
            "PresFormCd": 0,
            "fgdcGeoform": 1,
            "date": 4,
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "citRespParty": 6,
        }

        json_path = os.path.join(out_data_path, "idCitation_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(idCitation_dict, json_file, indent=4)

        contact_element_order_dict = {
            "editorSource": 0,
            "editorDigest": 1,
            "rpIndName": 2,
            "rpOrgName": 3,
            "rpPosName": 4,
            "rpCntInfo": 5,
            "cntAddress": 0,
            "delPoint": 0, # noqa: E261
            "city": 1,
            "adminArea": 2,
            "postCode": 3,
            "eMailAdd": 4,
            "country": 5,
            "cntPhone": 1,
            "voiceNum": 0,
            "faxNum": 1,
            "cntHours": 2, # noqa: E261
            "cntOnlineRes": 3,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0,
            "editorSave": 6,
            "displayName": 7,
            "role": 8,
            "RoleCd": 0,
            "srcCitatn": 1,
            "resTitle": 0, # noqa: E261
            "resAltTitle": 1,
            "collTitle": 2,
            "date": 10,
            "createDate": 0,
            "pubDate": 1,
            "reviseDate": 2,
            "presForm": 3,
            "PresFormCd": 0,
            "fgdcGeoform": 1, # noqa: E261
            "citRespParty": 6,
            "citOnlineRes": 2,
        }

        json_path = os.path.join(out_data_path, "contact_element_order_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(contact_element_order_dict, json_file, indent=4)

        dqInfo_dict = {
            "dqScope": 0,
            "scpLvl": 0,
            "ScopeCd": 0,
            "scpLvlDesc": 1, # noqa: E261
            "datasetSet": 0,
            "report": 1,
            "measDesc": 0,
            "measResult": 1,
            "dataLineage": 3,
            "statement": 0,
            "dataSource": 1,
            "srcDesc": 0, # noqa: E261
            "srcCitatn": 1,
            "resTitle": 0,
            "resAltTitle": 1,
            "collTitle": 2,
            "citOnlineRes": 2,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0,
            "date": 3,
            "createDate": 0, # noqa: E261
            "pubDate": 1,
            "reviseDate": 2,
            "otherCitDet": 4,
            "presForm": 5,
            "PresFormCd": 0,
            "fgdcGeoform": 1,
            "citRespParty": 6,
            "editorSource": 0,
            "editorDigest": 1,
            "rpIndName": 2,
            "rpOrgName": 3,
            "rpPosName": 4,
            "rpCntInfo": 5,
            "cntAddress": 0,
            "delPoint": 0, # noqa: E261
            "city": 1,
            "adminArea": 2,
            "postCode": 3,
            "eMailAdd": 4,
            "country": 5,
            "cntPhone": 1,
            "voiceNum": 0,
            "faxNum": 1,
            "cntHours": 2, # noqa: E261
            "cntOnlineRes": 3,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0,
            "editorSave": 6,
            "displayName": 7,
            "role": 8,
            "RoleCd": 0,
            "srcMedName": 7,
            "MedNameCd": 0, # noqa: E261
            "prcStep": 3,
            "stepDesc": 0,
            "stepProc": 1,
            "editorSource": 0,
            "editorDigest": 1,
            "rpIndName": 2,
            "rpOrgName": 3,
            "rpPosName": 4,
            "rpCntInfo": 5,
            "cntAddress": 0,
            "delPoint": 0, # noqa: E261
            "city": 1,
            "adminArea": 2,
            "postCode": 3,
            "eMailAdd": 4,
            "country": 5,
            "cntPhone": 1,
            "voiceNum": 0,
            "faxNum": 1,
            "cntHours": 2, # noqa: E261
            "cntOnlineRes": 3,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0,
            "editorSave": 6,
            "displayName": 7,
            "role": 8, # noqa: E261
            "RoleCd": 0,
            "stepDateTm": 2,
            "cntOnlineRes": 3,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0,
        }

        json_path = os.path.join(out_data_path, "dqInfo_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(dqInfo_dict, json_file, indent=4)

        distInfo_dict = {
            "distInfo": 0,
            "distFormat": 0,
            "formatName": 0,
            "formatVer": 1, # noqa: E261
            "fileDecmTech": 2,
            "formatInfo": 3,
            "distributor": 1,
            "distorCont": 0,
            "editorSource": 0,
            "editorDigest": 1,
            "rpIndName": 2,
            "rpOrgName": 3,
            "rpPosName": 4,
            "rpCntInfo": 5,
            "cntAddress": 0,
            "delPoint": 0, # noqa: E261
            "city": 1,
            "adminArea": 2,
            "postCode": 3,
            "eMailAdd": 4,
            "country": 5,
            "cntPhone": 1,
            "voiceNum": 0,
            "faxNum": 1,
            "cntHours": 2, # noqa: E261
            "cntOnlineRes": 3,
            "linkage": 0,
            "orName": 1,
            "orDesc": 2,
            "orFunct": 3,
            "OnFunctCd": 0,
            "editorSave": 6,
            "displayName": 7,
            "role": 8,
            "RoleCd": 0, # noqa: E261
            "distTranOps": 2,
            "unitsODist": 0,
            "transSize": 1,
            "onLineSrc": 2,
            "linkage": 0,
            "protocol": 1,
            "orName": 2,
            "orDesc": 3,
            "orFunct": 4,
            "OnFunctCd": 0, # noqa: E261
        }

        json_path = os.path.join(out_data_path, "distInfo_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(distInfo_dict, json_file, indent=4)

        RoleCd_dict = {
            "001": "Resource Provider",
            "002": "Custodian",
            "003": "Owner",
            "004": "User",
            "005": "Distributor",
            "006": "Originator",
            "007": "Point of Contact",
            "008": "Principal Investigator",
            "009": "Processor",
            "010": "Publisher",
            "011": "Author",
            "012": "Collaborator",
            "013": "Editor",
            "014": "Mediator",
            "015": "Rights Holder",
        }

        json_path = os.path.join(out_data_path, "RoleCd_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(RoleCd_dict, json_file, indent=4)

        # role_dict = {"citRespParty"  : ,
        #             "idPoC"        : ,
        #             "distorCont"   : ,
        #             "mdContact"    : ,
        #             "stepProc"

        tpCat_dict = {
            "002": '<tpCat><TopicCatCd value="002"></TopicCatCd></tpCat>',
            "007": '<tpCat><TopicCatCd value="007"></TopicCatCd></tpCat>',
            "014": '<tpCat><TopicCatCd value="014"></TopicCatCd></tpCat>',
        }

        json_path = os.path.join(out_data_path, "tpCat_dict.json")
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(tpCat_dict, json_file, indent=4)

        # Define individual contacts for clarity and reuse
        tim_haverland = {
            "rpIndName": "Timothy J Haverland",
            "rpOrgName": "NMFS Office of Science and Technology",
            "rpPosName": "GIS App Developer",
            "cntInfo": {
                "delPoint": "1315 East West Highway", "city": "Silver Spring", "adminArea": "MD",
                "postCode": "20910-3282", "country": "US", "eMailAdd": "tim.haverland@noaa.gov",
                "voiceNum": "301-427-8137", "faxNum": "301-713-4137",
                "linkage": "https://www.fisheries.noaa.gov/about/office-science-and-technology"
            }
        }

        melissa_karp = {
            "rpIndName": "Melissa Ann Karp",
            "rpOrgName": "NMFS Office of Science and Technology",
            "rpPosName": "Fisheries Science Coordinator",
            "cntInfo": {
                "delPoint": "1315 East West Hwy", "city": "Silver Spring", "adminArea": "MD",
                "postCode": "20910-3282", "country": "US", "eMailAdd": "melissa.karp@noaa.gov",
                "voiceNum": "301-427-8202", "faxNum": "301-713-4137",
                "linkage": "https://www.fisheries.noaa.gov/about/office-science-and-technology"
            }
        }

        john_f_kennedy = {
            "rpIndName": "John F Kennedy",
            "rpOrgName": "NMFS Office of Science and Technology",
            "rpPosName": "GIS Specialist",
            "cntInfo": {
                "delPoint": "1315 East West Highway", "city": "Silver Spring", "adminArea": "MD",
                "postCode": "20910-3282", "country": "US", "eMailAdd": "john.f.kennedy@noaa.gov",
                "voiceNum": "301-427-8149", "faxNum": "301-713-4137",
                "linkage": "https://www.fisheries.noaa.gov/about/office-science-and-technology"
            }
        }

        nmfs_ost = {
            "rpIndName": "NMFS Office of Science and Technology",
            "rpOrgName": "NMFS Office of Science and Technology",
            "rpPosName": "GIS App Developer",
            "cntInfo": {
                "delPoint": "1315 East West Highway", "city": "Silver Spring", "adminArea": "MD",
                "postCode": "20910-3282", "country": "US", "eMailAdd": "tim.haverland@noaa.gov",
                "voiceNum": "301-427-8137", "faxNum": "301-713-4137",
                "linkage": "https://www.fisheries.noaa.gov/about/office-science-and-technology"
            }
        }

        # Assemble the contact dictionary using the defined contacts and their roles
        contact_dict = {
            "citRespParty": [{**tim_haverland, "role": "002"}],
            "idPoC": [{**melissa_karp, "role": "007"}],
            "distorCont": [{**nmfs_ost, "role": "005"}],
            "mdContact": [{**john_f_kennedy, "role": "011"}],
            "srcCitatn": [{**melissa_karp, "role": "008"}],
            "stepProc": [
                {**john_f_kennedy, "role": "009"},
                {**melissa_karp, "role": "009"}
            ]
        }

        json_path = os.path.join(out_data_path, "contact_dict.json")
        # arcpy.AddMessage(json_path)
        # Write to File
        with open(json_path, "w") as json_file:
            json.dump(contact_dict, json_file, indent=4)

        arcpy.AddMessage("Successfully created JSON configuration files.")

        # ###################### DisMAP ########################################

        # Declared Varaiables
        del project_folder, out_data_path
        # Imports
        # Function Parameters
        del json
        del project_gdb

        # Elapsed time
        end_time = time()
        elapse_time = end_time - start_time
        hours, rem = divmod(end_time - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        arcpy.AddMessage(f"\n{'-' * 80}")
        arcpy.AddMessage(f"Python script: {os.path.basename(__file__)}")
        arcpy.AddMessage(
            f"Start Time:    {strftime('%a %b %d %I:%M %p', localtime(start_time))}"
        )
        arcpy.AddMessage(
            f"End Time:      {strftime('%a %b %d %I:%M %p', localtime(end_time))}"
        )
        arcpy.AddMessage(
            f"Elapsed Time   {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f} (H:M:S)"
        )
        arcpy.AddMessage(f"{'-' * 80}")
        del hours, rem, minutes, seconds
        del elapse_time, end_time, start_time
        del gmtime, localtime, strftime, time

    except KeyboardInterrupt:
        sys.exit()
    except arcpy.ExecuteWarning:
        arcpy.AddWarning(
            f"Caught an arcpy.ExecuteWarning error in the '{inspect.stack()[0][3]}' function."
        )
        arcpy.AddWarning(arcpy.GetMessages(1))
    except arcpy.ExecuteError:
        arcpy.AddError(
            f"Caught an arcpy.ExecuteError error in the '{inspect.stack()[0][3]}' function."
        )
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
        sys.exit()
    except SystemExit as se:
        arcpy.AddError(
            f"Caught an SystemExit error: {se} in the '{inspect.stack()[0][3]}' function."
        )
        sys.exit()
    except Exception as e:
        arcpy.AddError(
            f"Caught an Exception error: {e} in the '{inspect.stack()[0][3]}' function."
        )
        traceback.print_exc()
        sys.exit()
    except:
        arcpy.AddError(
            f"Caught an except error in the '{inspect.stack()[0][3]}' function."
        )
        traceback.print_exc()
        sys.exit()
    else:
        # While in development, leave here. For test, move to finally
        rk = [key for key in locals().keys() if not key.startswith("__")]
        if rk:
            arcpy.AddMessage(
                f"WARNING!! Remaining Keys in the '{inspect.stack()[0][3]}' function at line number {inspect.stack()[0][2]}\n\t##--> '{', '.join(rk)}' <--##"
            )
            del rk
        return True
    finally:
        pass


if __name__ == "__main__":
    try:

        project_gdb = arcpy.GetParameterAsText(0)
        if not project_gdb:
            project_gdb = rf"{os.path.expanduser('~')}\Documents\ArcGIS\Projects\DisMAP\ArcGIS-Analysis-Python\August 1 2025\August 1 2025.gdb"
        else:
            pass

        script_tool(project_gdb=project_gdb)
        arcpy.SetParameterAsText(1, "Result")
        del project_gdb

    except SystemExit:
        pass
    except:
        arcpy.AddError(arcpy.GetMessages(2))
        traceback.print_exc()
    else:
        pass
    finally:
        sys.exit()
# This is an autogenerated comment.
