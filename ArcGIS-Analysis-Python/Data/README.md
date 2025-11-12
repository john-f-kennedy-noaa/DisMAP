# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"Data" Folder Summary:**

This is the **centralized metadata and configuration repository** providing reference data, lookup tables, and survey information for the entire DisMAP processing pipeline. It contains static reference files updated as of August 1, 2025 (version date in filenames).

**Core Configuration Files:**

| File | Purpose | Format |
|------|---------|--------|
| **Datasets_20250801.csv** | Master dataset registry (survey names, regions, seasons, codes) | CSV |
| **DisMAP_Survey_Info_20250801.csv** | Survey metadata (names, descriptions, methodologies, contacts) | CSV |
| **Species_Filter_20250801.csv** | Species filtering criteria (core vs. non-core designation, persistence thresholds) | CSV |
| **DisMAP_Regions_20220516.xml** | Regional boundary definitions (15 IDW regions, geographic extents) | XML |
| **DisMAP Contacts 2025 08 01.xml** | Principal investigators and contacts for each survey | XML |

**Data Lookup Tables:**

| File | Purpose |
|------|---------|
| **RoleCd.txt** | Role code reference (PI, co-investigator, analyst, etc.) |
| **SpeciesPersistenceIndicatorPercentileBin_20250801.csv** | Species persistence percentile thresholds (binning criteria) |
| **SpeciesPersistenceIndicatorTrend_20250801.csv** | Species trend indicators (declining/stable/increasing designations) |

**Archived Data Archives:**

| File | Contents |
|------|----------|
| **CSV Data 2025 08 01.zip** | Raw survey observations (point-level catch/biomass data by species/year/location) |
| **Dataset Shapefiles 2025 08 01.zip** | Regional shapefiles (polygon boundaries for 15 IDW regions) |

**Pipeline Integration:**

These files feed into multiple processing stages:

1. **create_region_sample_locations** (Director #4)
   - Reads raw CSV survey data
   - Applies Species_Filter for core species identification
   - Uses DisMAP_Survey_Info for metadata enrichment

2. **create_rasters** (Director #5)
   - References Datasets_20250801.csv for IDW region mapping
   - Applies species persistence thresholds from SpeciesPersistenceIndicator* files

3. **create_indicators_table** (Director #9)
   - Uses Species_Filter to aggregate core vs. total species richness

4. **Metadata publishing** (publish_to_portal_director)
   - Embeds DisMAP Contacts XML for author attribution
   - References DisMAP_Regions_20220516.xml for geographic descriptions

**Data Status:**
- Read-only reference (updated only when survey data refreshed)
- Version-dated naming convention (20250801 suffix indicates August 1, 2025 release)
- Shared across all project versions and processing runs
- Critical dependencies: Cannot be omitted or corrupted without halting pipeline

**Versioning Pattern:**
- Files consistently dated: 2025-08-01 (current)
- Historical versions available in archived project folders (e.g., April 1 2023, July 1 2024)
- R data processing generates these CSVs from raw survey databases (via `data_processing_rcode/create_data_for_map_generation.R`)

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
