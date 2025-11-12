# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"Dataset Shapefiles" Folder Summary:**

This is a **regional shapefile repository** containing boundary and reference geometries for all 15 IDW survey regions in the DisMAP project. Each region is stored as a separate shapefile set with complete ArcGIS metadata.

**Regional Coverage (15 Regions):**

| Region | Geographic Area |
|--------|-----------------|
| **AI_IDW** | Aleutian Islands |
| **EBS_IDW** | Eastern Bering Sea |
| **ENBS_IDW** | Eastern/Northern Bering Sea |
| **GMEX_IDW** | Gulf of Mexico |
| **GOA_IDW** | Gulf of Alaska |
| **HI_IDW** | Hawaii |
| **NBS_IDW** | Northern Bering Sea |
| **NEUS_FAL_IDW** | Northeast US (Fall) |
| **NEUS_SPR_IDW** | Northeast US (Spring) |
| **SEUS_FAL_IDW** | Southeast US (Fall) |
| **SEUS_SPR_IDW** | Southeast US (Spring) |
| **SEUS_SUM_IDW** | Southeast US (Summer) |
| **WC_ANN_IDW** | West Coast (Annual) |
| **WC_TRI_IDW** | West Coast (Triennial) |

**Shapefile Structure (Per Region):**

Each region folder contains a standard shapefile dataset:
- `.shp` — Geometry (polygon boundaries)
- `.shx` — Shape index
- `.dbf` — Attribute database
- `.prj` — Projection definition
- `.sbn, .sbx` — Spatial indexes (query optimization)
- `.shp.xml` — ArcGIS metadata

**Pipeline Integration:**

These shapefiles serve as **input to Director #1** (`create_regions_from_shapefiles`):
1. Reads `{Region}_Region.shp` files
2. Imports polygon boundaries into master `DisMAP_Regions` feature class
3. Cascades metadata to all region-derived features (fishnets, bathymetry, sample locations, rasters, mosaics, indicators)

**Data Status:**
- Read-only reference geometries
- Stable across all processing runs (regional boundaries don't change)
- Shared across all project versions (April 1 2023 through August 1 2025)
- Coordinate system: Each region has `.prj` file specifying projection (typically regional UTM or custom projections)

**Versioning:**
- Archived version available: `Dataset Shapefiles 2025 08 01.zip` (in Data folder)
- Current working copy: This folder (active processing version)

**Functional Role:**
Starting point of the entire pipeline—geographic framework defining where all IDW interpolation, raster generation, and indicator calculations occur. No processing outputs without these regional boundaries. 

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
