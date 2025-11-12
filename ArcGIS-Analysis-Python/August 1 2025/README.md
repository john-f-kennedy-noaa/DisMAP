# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"August 1 2025" Folder Summary:**

This is the **current active DisMAP project version** (as of August 1, 2025)—the primary development and production environment for processing, analysis, and Portal publishing workflows.

**Core Project Files:**

| Component | Purpose |
|-----------|---------|
| **August 1 2025.aprx** | Active ArcGIS Pro project (base for all spatial workflows) |
| **August 1 2025.gdb/** | **Main project geodatabase** (all processed spatial datasets) |
| **user_credentials.py** | Portal authentication credentials (for publishing workflows) |
| **__init__.py, __pycache__/** | Python package structure for this project version |
| **ArcGIS2InPort.xsl** | XSLT stylesheet for metadata transformation to InPort format |
| **New Notebook.ipynb** | Jupyter notebook (analysis/development workspace) |

**Data & Processing Folders:**

| Folder | Contents |
|--------|----------|
| **CSV_Data/** | Input CSV files (survey observations, species metadata, filter tables) |
| **Dataset_Shapefiles/** | Regional shapefiles (15 IDW regions: AI_IDW, EBS_IDW, etc.) |
| **Bathymetry/** | Bathymetry source data (GEBCO, Alaska, Hawaii rasters) |
| **CRFs/** | Cloud Raster Format exports (web-ready mosaic rasters) |
| **Layers/** | `.lyrx` layer files (published feature class definitions) |
| **Publish/** | Service definition drafts (`.sddraft`, `.sd` files for Portal upload) |

**Metadata & Documentation:**

| Folder | Purpose |
|--------|---------|
| **Metadata_Export/** | XML metadata exports for all datasets (formatted for Portal/InPort) |
| **RasterFunctionTemplates/** | Raster function definitions (processing templates) |
| **Images/** | Map thumbnails, visualization exports |
| **Index/** | Spatial indices for fast GDB queries |

**Processing & Logging:**

| Folder | Purpose |
|--------|---------|
| **GpMessages/** | Geoprocessing tool execution logs/warnings |
| **ImportLog/** | Data import operation logs |
| **Scratch/** | Temporary workspace (working GDB, intermediate outputs) |
| **.backups/, .pyHistory** | Version history backups and Python command history |
| **.ipynb_checkpoints/** | Jupyter notebook version snapshots |

**Development Indicators:**

- **Python package structure**: Presence of __init__.py and `user_credentials.py` indicates this version is actively maintained as a development workspace
- **Jupyter support**: `New Notebook.ipynb` suggests ongoing exploratory analysis/testing
- **Portal-ready**: Pre-configured credentials and publishing infrastructure (Layers, Publish folders) show this is the active deployment target
- **XSLT metadata transformation**: `ArcGIS2InPort.xsl` indicates integration with NOAA's InPort metadata repository system

**Workflow Status:**

This folder represents the **complete pipeline terminus**—output from all 10 processing directors flows here:
1. ✓ Regions created → stored in GDB
2. ✓ Fishnets/bathymetry/sample locations → stored in GDB
3. ✓ IDW rasters, richness rasters → stored in GDB
4. ✓ Mosaic datasets created → stored in GDB + CRFs exported
5. ✓ Indicators calculated → stored in GDB
6. ✓ Layer files, publishing metadata prepared → in Layers, Publish, Metadata_Export
7. ⏳ Portal publishing (via `publish_to_portal_director`) → ready to upload services

**Compared to April 1 2023:**
- Active vs. archived (April 1 2023 is read-only historical snapshot)
- Enhanced metadata infrastructure (XSL transform, user credentials)
- Development tools included (Jupyter notebook, Python history tracking)
- Portal-integrated (Publish folder, CRF exports for web services)

#### Suggestions and Comments

If you see that the data, product, or metadata can be improved, you are
invited to create a [pull
request](https://github.com/nmfs-fish-tools/DisMAP/pulls)
or [submit an issue to the code’s
repository](https://github.com/nmfs-fish-tools/DisMAP/issues).

#### NOAA-NMFS GitHub Enterprise Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic 
and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project 
code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims 
against the Department of Commerce or Department of Commerce bureaus stemming from the use of this 
GitHub project will be governed by all applicable Federal law. Any reference to specific commercial 
products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not 
constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. 
The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used 
in any manner to imply endorsement of any commercial product or activity by DOC or the United States
Government.

#### NOAA License

Software code created by U.S. Government employees is not subject to
copyright in the United States (17 U.S.C. §105). The United
States/Department of Commerce reserve all rights to seek and obtain
copyright protection in countries other than the United States for
Software authored in its entirety by the Department of Commerce. To this
end, the Department of Commerce hereby grants to Recipient a
royalty-free, nonexclusive license to use, copy, and create derivative
works of the Software outside of the United States.

<img src="https://raw.githubusercontent.com/nmfs-general-modeling-tools/nmfspalette/main/man/figures/noaa-fisheries-rgb-2line-horizontal-small.png" alt="NOAA Fisheries" height="75"/>

[U.S. Department of Commerce](https://www.commerce.gov/) \| [National
Oceanographic and Atmospheric Administration](https://www.noaa.gov) \|
[NOAA Fisheries](https://www.fisheries.noaa.gov/)
