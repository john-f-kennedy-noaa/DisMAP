# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"July 1 2024" Folder Summary:**

This is a **comprehensive archived project version** (July 1, 2024) representing a fully-processed and documented production release. It contains the most complete distribution of working outputs and intermediate data of all versioned folders.

**Project Files:**

| Component | Purpose |
|-----------|---------|
| **July 1 2024.gdb/** | Main project geodatabase (processed outputs) |
| **July 1 2024.gdb.zip** | Compressed backup of main GDB |
| **July 1 2024 Metadata.aprx** | ArcGIS Pro project for metadata workflows |
| **July 1 2024 Metadata.gdb/** | Geodatabase for metadata management |
| **July 1 2024 Metadata.atbx** | ArcGIS Toolbox (geoprocessing workflows) |

**Processed Data & Outputs:**

| Category | Contents |
|----------|----------|
| **Regional outputs (zipped)** | AI_IDW.zip, EBS_IDW.zip, ENBS_IDW.zip, GMEX_IDW.zip, GOA_IDW.zip, HI_IDW.zip, NBS_IDW.zip, NEUS_FAL_IDW.zip, NEUS_SPR_IDW.zip, SEUS_FAL_IDW.zip, SEUS_SPR_IDW.zip, SEUS_SUM_IDW.zip, WC_ANN_IDW.zip, WC_TRI_IDW.zip |
| **Raster data** | CRFs.zip (Cloud Raster Formats for web services) |
| **Input data** | CSV Data/, CSV Data.zip, Bathymetry.zip, Dataset Shapefiles.zip |
| **Layer definitions** | Layers.zip (feature layer files) |
| **Publishing** | Publish.zip (service definitions) |

**Metadata Infrastructure:**

| Folder | Purpose |
|--------|---------|
| **Current Metadata/**, **Current Metadata.zip** | Active metadata (titles, descriptions, tags) |
| **Export Metadata/**, **Export Metadata.zip** | Formatted metadata exports |
| **ArcGIS Metadata/**, **ArcGIS Metadata.zip** | ArcGIS standard metadata compliance |
| **InPort Metadata/**, **InPort Metadata.zip** | NOAA InPort format metadata |
| **Fisheries Geoportal Metadata Export/** | Fisheries Portal metadata format |
| **NOAA Geoportal Metadata Export/** | NOAA Portal metadata format |
| **Project Metadata.zip** | Complete metadata archive |

**Logging & Documentation:**

| Item | Purpose |
|------|---------|
| **GpMessages/** | Geoprocessing tool execution logs |
| **Images.zip** | Map thumbnails and visualizations |
| **.backups/** | Version history backups |
| **README.md** | Documentation |

**Data Completeness:**

This version is the **most comprehensive archived release**:
- ✓ All 15 regional datasets (zipped individually)
- ✓ Complete metadata ecosystem (4 different standards)
- ✓ All input data (shapefiles, CSVs, bathymetry)
- ✓ Output deliverables (layers, publishing configs, CRFs)
- ✓ Both GDB formats (main + metadata GDB)
- ✓ Toolbox definitions

**Comparison to Other Versions:**

| Aspect | July 1 2024 | Aug 1 2025 | Dec 1 2024 | April 1 2023 |
|--------|-----------|-----------|-----------|------------|
| **Completeness** | Complete | Active | Minimal | Complete |
| **Regional zips** | ✓ All 14 | ✗ Unzipped | ✗ | ✗ |
| **Multiple metadata standards** | ✓ InPort, ArcGIS, NOAA | Partial | ✗ | ✓ |
| **Input data bundled** | ✓ Zipped | ✗ Separate | ✗ | ✗ |
| **Status** | Archived | Production | Checkpoint | Archived |

**Role in Development:**

- **Historical reference**: Most complete snapshot for comparing processing methodologies
- **Delivery package**: July 1 2024 was likely a major release milestone with full metadata preparation
- **Recovery point**: Full backup/restore capability if needed
- **Documentation archive**: Best example of complete end-to-end workflow outputs

**Key Distinction:**
July 1 2024 is the **most feature-complete archived version**—it includes all processing outputs individually zipped by region, comprehensive metadata exports for multiple portal standards (InPort, ArcGIS, NOAA, Fisheries), and complete input data bundling. It represents a production release with full quality assurance and documentation, unlike the simpler December 1 2024 checkpoint or the development-focused August 1 2025.

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
