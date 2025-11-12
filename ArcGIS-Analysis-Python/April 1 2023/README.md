# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"April 1 2023" Folder Summary:**

This is an **archived DisMAP project version** containing a complete snapshot of data processing from April 1, 2023. The folder serves as a historical build artifact and reference point for that production release.

**Key Components:**

| Component | Purpose |
|-----------|---------|
| **April 1 2023.aprx** | ArcGIS Pro project file (base project for this release version) |
| **April 1 2023.atbx** | ArcGIS Toolbox archive (geoprocessing tools/workflows snapshot) |
| **April 1 2023.gdb/** | Main project geodatabase containing processed spatial data |
| **DisMAP April 1 2023 Dev.gdb/** | Development geodatabase (intermediate/test data) |
| **DisMAP April 1 2023 Prod.gdb/** | Production geodatabase (final validated outputs) |
| **DisMAP April 1 2023 Prod.Overviews/** | Raster pyramid/overview files for optimized display |
| **Bathymetry.gdb/** | Bathymetry-specific geodatabase (depth raster data) |
| **CSV Data Folder/** | Input CSV files (survey data, species info, metadata) |
| **Dataset Shapefile Folder/** | Shapefiles for regions, boundaries, sample locations |
| **Metadata Export/** | Formatted XML metadata exports for all datasets |
| **ArcGIS Metadata/** | Metadata standard compliance documents |
| **Fisheries & NOAA Geoportal Metadata Export/** | Portal-specific metadata formats |
| **RasterFunctionTemplates/** | Function templates for raster processing workflows |
| **RasterFunctionsHistory/** | Archive of applied raster function chains |
| **GpMessages/, ImportLog/, Schema Folder/** | Processing logs, error messages, schema definitions |
| **README.md** | Project documentation with version history reference |

**Folder Status:**

- **Type**: Historical archive/snapshot (not active production)
- **Release Date**: April 1, 2023
- **Current Use**: Reference version; benchmarking against newer builds (August 1 2025, July 1 2024, December 1 2024)
- **Binary data**: Contains large GDBs (~500MB-1GB+ typical); treat as read-only artifacts
- **Not for editing**: Per copilot instructions, avoid modifying large binary geodatabases in version folders

This represents one of three versioned releases alongside **December 1 2024**, **July 1 2024**, and **August 1 2025** (current active), demonstrating the project's evolution over time with accumulated processing refinements.

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
