### Project Summary
This project contains python scripts and python notebooks used to automate maintenance and QA/QC processes applied to the TNC Lands dataset.

### Project Description
The maintenance and sharing of the TNC Lands conservation lands dataset has evolved over time, becoming more standardized and automated, using the python scripting language.  Also, certain data transformations from the native TNC Lands schema into partner schemas were also created, but are not currently maintained.

This project contains the latest python scripts to automate the reconciliation of TNC Lands attribute data and LRM fee and conservation easement reports. This scripting is not complete, nor fully tested.

The code folder structure is as follows:
- tnclands
    - archive: archive copies of files when the base code is lacking code version control
    - docs: documentation for the project
    - notebooks: python notebook versions of the code
    - snippets: code fragments saved outside of the version control mechanism
    - source: the source code folder. At the time of this writing, only one python scriptfile exists:
        - tncLands_LRM_reconcile.py