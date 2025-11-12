# DisMAP ArcGIS Pro Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders
* Version Folders -- The version folders (i.e. April 1 2023) contain all the files, datasets, and databases for the listed version. Within each folder there is a README.md that lists the links to the datasets published to the NOAA Geoplatform and the Fisheries Portal
    + May 16 2022 -- 20220516 version (e.g. DisMAP_Regions_20220516)
    + April 1 2023 -- 20230401 version (e.g. DisMAP_Regions_20230401)
    + July 1 2024 -- 20240701 version (e.g. DisMAP_Regions_20240701)
    + December 1 2024 -- 20241201 version (e.g.HI_Sample_Locations_20241201)
    + August 1 2025 -- 20250801 version (e.g. DisMAP_Regions_20250801), Current Version

* Data Folders -- These folder contain input data needed for the DisMAP Python processing. Within each folder there is a README.md that lists datasources
    + Bathymetry -- This folder contains the sourece bathymetry data for all regions and the processed bathymetry contained in the Bathymetry.gdb 
    + Data -- This folder contains the CSV IDW data for each region, plus CSV support tables
    + Dataset Shapefiles -- This folder contains the shapefiles for each region

* src Folder -- This folder contains the current and past versions of Python scripts for generating the interpolated biomass and calculating the distribution indicators (latitude, depth, range limits, etc). Within each folder there is a README.md that lists the folder contents. The README.md file located in src/dismap_tools desacribes in general each Python script

#### Suggestions and Comments

If you see that the data, product, or metadata can be improved, you are invited to create a [pull request](https://github.com/nmfs-fish-tools/DisMAP/pulls) or [submit an issue to the code’s repository](https://github.com/nmfs-fish-tools/DisMAP/issues).

#### NOAA-NMFS GitHub Enterprise Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. 
The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

#### NOAA License

Software code created by U.S. Government employees is not subject to copyright in the United States (17 U.S.C. §105). The United States/Department of Commerce reserve all rights to seek and obtain copyright protection in countries other than the United States for Software authored in its entirety by the Department of Commerce. To this end, the Department of Commerce hereby grants to Recipient a royalty-free, nonexclusive license to use, copy, and create derivative works of the Software outside of the United States.

<img src="https://raw.githubusercontent.com/nmfs-general-modeling-tools/nmfspalette/main/man/figures/noaa-fisheries-rgb-2line-horizontal-small.png" alt="NOAA Fisheries" height="75"/>

[U.S. Department of Commerce](https://www.commerce.gov/) \| [National Oceanographic and Atmospheric Administration](https://www.noaa.gov) \| [NOAA Fisheries](https://www.fisheries.noaa.gov/)
