# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"Bathymetry" Folder Summary:**

This is a **shared bathymetry data repository** providing ocean depth reference datasets for the entire DisMAP project. It serves as the centralized source for depth rasters used during the `create_region_bathymetry` workflow step (director/worker pair #3).

**Contents:**

| Component | Source & Format |
|-----------|-----------------|
| **Alaska Bathymetry/** | Arc/INFO GRID format files provided by NOAA Alaska Region (regional depth coverage) |
| **GEBCO Bathymetry/** | ASCII GRID files downloaded from GEBCO website (General Bathymetric Chart of the Oceans—global coverage) |
| **Hawaii Bathymetry/** | BFISH_SU shapefile provided by NOAA Hawaii Science Center (regional depth data) |
| **Bathymetry.gdb/** | ArcGIS geodatabase (processed/integrated bathymetry rasters) |
| **README.md** | Documentation and processing reference |

**Processing Pipeline Integration:**

This folder feeds into the `create_region_bathymetry_director/worker` pair which:
1. Reads regional source bathymetry (Alaska GRID, GEBCO, or Hawaii shapefile)
2. Reprojects to match region-specific coordinate systems
3. Calculates zonal statistics (median depth per fishnet cell)
4. Outputs `{table_name}_Bathymetry` raster for each region (stored in main project GDB)

**Key Scripts Referenced:**
- `src/dismap_tools/create_base_bathymetry.py` — Base bathymetry preparation
- `create_region_bathymetry_director.py` — Orchestrates regional processing
- `create_region_bathymetry_worker.py` — Worker processes individual regions

**Multi-Source Strategy:**

- **Alaska**: Custom GRID format (ArcInfo native)
- **GEBCO**: Public global bathymetry dataset (ASCII raster)
- **Hawaii**: Custom shapefile (Science Center-specific)
- **Result**: Unified bathymetry coverage across all 15 IDW regions with consistent depth aggregation methodology

**Data Status:**
- Shared across all project versions (referenced by both April 1 2023 and August 1 2025)
- Read-only reference data (not modified during processing)
- Reusable for multiple survey regions and years

#### Suggestions and Comments

If you see that the data, product, or metadata can be improved, you are
invited to create a [pull request](https://github.com/nmfs-fish-tools/DisMAP/pulls)
or [submit an issue to the code’s repository](https://github.com/nmfs-fish-tools/DisMAP/issues).

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
