# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"December 1 2024" Folder Summary:**

This is an **intermediate archived project version** (December 1, 2024)—a historical snapshot between July 1 2024 and the current August 1 2025 production version. It represents a development checkpoint with reduced content compared to fully-equipped versions.

**Contents:**

| Component | Purpose |
|-----------|---------|
| **December 1 2024.aprx** | ArcGIS Pro project file for this version |
| **December 1 2024.gdb/** | Project geodatabase (processed spatial datasets snapshot) |
| **GpMessages/** | Geoprocessing execution logs from processing runs |
| **NOAA Geoportal Metadata Export/** | Portal-formatted metadata exports |
| **.backups/** | Version history backups |
| **README.md** | Documentation (minimal content) |

**Comparison to Other Versions:**

| Aspect | Dec 1 2024 | Aug 1 2025 (Current) | April 1 2023 |
|--------|-----------|-------------------|-------------|
| **Status** | Development checkpoint | Active production | Archived snapshot |
| **Completeness** | Minimal (core GDB only) | Full (all infrastructure) | Full (historical) |
| **Python package** | Not included | ✓ __init__.py, credentials | ✗ |
| **Layer files** | ✗ | ✓ Layers/ folder | ✗ |
| **Publishing config** | ✗ | ✓ Publish/, Credentials | ✗ |
| **Metadata infrastructure** | Basic | Enhanced (XSL, XML) | Complete |
| **Development tools** | ✗ | ✓ Jupyter notebook | ✗ |

**Processing Timeline:**

```
April 1 2023 (v1.0)
    ↓
July 1 2024 (v2.0 intermediate)
    ↓
December 1 2024 (v2.5 checkpoint) ← Current folder
    ↓
August 1 2025 (v3.0 current production)
```

**Role in Development Workflow:**

- **Not for active use**: Represents intermediate state, potentially with incomplete/untested features
- **Reference point**: Shows evolution of project structure and features
- **Backup/recovery**: Available if August 1 2025 requires rollback to prior stable state
- **Historical comparison**: Useful for tracking processing methodology changes

**Data Status:**
- Read-only archived version
- GDB contains snapshot outputs from December 1, 2024 processing run
- No active development or updates
- Binary geodatabase (treat as immutable)

**Key Distinction:**
This version sits between April 1 2023 (fully documented historical) and August 1 2025 (fully operational current), representing an intermediate stage in the project's evolution without the complete infrastructure or documentation of the other two.

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
