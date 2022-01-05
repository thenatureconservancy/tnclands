### Project Summary

This project contains python scripts and python notebooks used to automate maintenance and QA/QC processes applied to the TNC Lands dataset.

### Project Description

The maintenance and sharing of the TNC Lands conservation lands dataset has evolved over time, becoming more standardized and automated, using the python scripting language.  Also, certain data transformations from the native TNC Lands schema into partner schemas were also created, but are not currently maintained.

This project contains the latest python scripts to automate the reconciliation of TNC Lands attribute data and LRM fee and conservation easement reports. This scripting is not complete, nor fully tested.

The code folder structure is as follows:
- tnclands
    - archive: archive copies of files created when the project lacked code version control
    - docs: document files for the project
    - notebooks: python notebook versions of the code files
        - tncLands_LRM_reconcile.ipynb
    - snippets: code fragments saved outside of the version control mechanism
    - source: the source code folder. At the time of this writing, only one python scriptfile exists:
        - tncLands_LRM_reconcile.py

### Scripting Notes

This section describes the original use-case design when the python script was created.

- The python script is intended to be run from within an ArcGIS Pro 2 project.
- The script will be called from an ArcGIS tool, and the tool will reside in a ArcGIS toolbox.
- The inputs to the tool will be:
    - The TNC Lands Base feature class
    - An LRM fee and easement report
- The script will do the following:
    - Create a reconcilation report, showing the differences between the TNC Lands spatial data and the LRM report records
        - The script will report the LRM records that do not have a corresponding TNC Lands spatial record
        - The script will report the TNC Lands spatial records that do not have a corresponding LRM record
    - "Note that the LRM report only lists fee properties and conservation easements.  Other conservation protection mechanisms and historical information (transfers) or transactions that did not include a legal interest held by TNC (assists) are not included."
    - The script will update all of the LRM fields in the TNC Lands table schema, replacing the values in the fields with whatever is in the LRM report.
- General design considerations:
    - The script does not use classes, just functions
    - At the time of this writing, there is ***some*** error checking applied in the functions. The error checking should not be considered complete.
