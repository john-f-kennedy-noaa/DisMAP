# [The Distribution Mapping and Analysis Portal (DisMAP)](https://github.com/nmfs-fish-tools/DisMAP) 
## ArcGIS Processing and Analysis using Python
> This code is always in development. Find the code used for various reports in the code [releases](https://github.com/nmfs-fish-tools/DisMAP/releases).

#### Explanation of Files and Folders

**"May 16 2022" Folder Summary:**

This is the **earliest archived project version** (May 16, 2022)—the original DisMAP processing baseline and foundational release. It represents the project's starting point with minimal infrastructure.

**Contents:**

| Component | Purpose |
|-----------|---------|
| **May 16 2022.aprx** | Initial ArcGIS Pro project file |
| **May 16 2022.gdb/** | Original project geodatabase (baseline outputs) |
| **GpMessages/** | Geoprocessing execution logs |
| **NOAA Geoportal Metadata Export/** | Portal metadata exports |
| **.backups/** | Version history backups |
| **README.md** | Documentation (minimal) |

**Version Evolution Timeline:**

```
May 16 2022 (v1.0 - Original)
    ↓
July 1 2024 (v2.0 - Major release, comprehensive)
    ↓
December 1 2024 (v2.5 - Checkpoint)
    ↓
August 1 2025 (v3.0 - Current production)
```

**Comparison to Later Versions:**

| Aspect | May 16 2022 | July 1 2024 | Aug 1 2025 |
|--------|-----------|-----------|-----------|
| **Minimal infrastructure** | ✓ Core only | ✗ Full | ✗ Full |
| **Regional data zipped** | ✗ | ✓ All 14 | ✗ Unzipped |
| **Metadata standards** | Basic | ✓ InPort, ArcGIS | ✓ Enhanced |
| **Layer files** | ✗ | ✓ Zipped | ✓ Structured |
| **Publishing infrastructure** | ✗ | ✓ | ✓ |
| **Python packaging** | ✗ | ✗ | ✓ |
| **Development tools** | ✗ | ✗ | ✓ Jupyter |

**Functional Role:**

- **Historical baseline**: Shows original project scope and structure
- **Processing reference**: Earliest implementation of the 10-director pipeline
- **Version control checkpoint**: Useful for tracking cumulative enhancements over ~3+ years
- **Archive only**: Not for active use or development

**Key Characteristics:**

- **Simplicity**: Bare minimum—only main GDB and project file
- **No bundling**: No regional zips, no separate metadata infrastructure
- **Minimal metadata**: Only basic NOAA Geoportal exports
- **Read-only**: Immutable historical snapshot (2022 production snapshot)

**Distinction from Other Versions:**

- **vs. April 1 2023**: April 1 2023 is more complete (metadata exports, structured folders); May 16 2022 is the predecessor
- **vs. July 1 2024**: July 1 2024 is the most feature-complete; May 16 2022 is the original minimal implementation
- **vs. August 1 2025**: August 1 2025 is actively developed; May 16 2022 is the historic baseline

**Data Status:**
- Read-only archived version
- Original release (over 3 years old as of November 2025)
- Represents foundational DisMAP pipeline implementation
- Binary GDB (treat as immutable)

This folder marks the **project's inception point**—the starting state before subsequent refinements, feature additions, and infrastructure enhancements that evolved through 2024-2025.

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
