# Fusion-360-Report-Viewer #
### An AddIn to Automate Manufacturing Reports ###
\
This is a very early work in progress. Please feel free to reach out! I'm not a 
programmer by trade, and any input is greatly appreciated!

## Commands ##
* **Add Image:** Take a screenshot at the current view to associate with any 
  selected body.
* **Add Image Batch:** Produce a set of images associated with bodies under
  unique part id's
* **Edit Project Data:** Include custom variables in an associated JSON that 
* **Empty Temp Files:** Remove all temporary files used in report documents 
  (currently this is limited to images)
* **Input Project Data:** A utility for Edit Project Data which initializes the 
  associated JSON
* **Open Browser:** View a directory in your filesystem as a webpage in your 
  preferred internet browser
* **Open Home Folder:** A convenience to open the folder being hosted in your 
  browser
* **Open Log File:** A convenience to show the data exported from Fusion 360 
  into a subprocess
* **Process Add:** Add an attribute defined by custom report templates to 
  components - This attribute will be exported along with the component 
  definition
* **Process Remove:** Remove an attribute defined by a custom report template
* **Process Select:** Select all components with attributes defined by a 
  custom report template
* **Start Server:** Launch a TCP server to host your "Home Page" directory on a 
  localhost port (default is 8000) to view live updates to documents
* **Stop Server:** Stop the localhost server in case of a crash or to reduce 
  overhead

## Goals & Philosophy ##
* This AddIn intends to be easy to implement and free from additional package 
  installation.
* All code will be implemented using only the Python Standard Library and 
  various CLI tools which will come included as precompiled executables for the 
  x86_64-pc-windows-gnu environment.
* All data interchanged MUST be in a human-readable, plain text format. While 
  using JSON is not ideal, it meets these criteria while also being easy to 
  implement from the Python Standard Library.
* For this reason, the target of custom report building is raw HTML/CSS. These 
  documents are hosted in the browser so that they may be finalized by printing 
  to PDF.
* All utility binaries will be posted as a separate repository so that the 
  source code may be inspected.
* I intend to write all utility functions in Rust for stability, but all 
  arguments and expected outcomes from each utility will be documented so that 
  they can be replaced by any other compiled utility.
* Compiled utilities are not intended to interface with the Fusion 360 API 
  directly. This will be done with modularity and ease of use in mind. Each 
  one is intended to be "fire and forget" (i.e. to be launched in a separate 
  thread which will not return any information back into Fusion 360).
* The goal of utility binaries is for the burden of general file system 
  operations and interfacing with the browser to be taken away from Fusion 360. 
  Currently, the scope of utilities is limited to hosting local files and 
  editing HTML.
* Most Importantly: ANY operations which may incur a significant runtime 
  overhead in Fusion 360 should be focused on for optimization, able to be 
  deactivated with a single command, offloaded to a utility, or factored out 
  of the AddIn entirely.
* This aims to feel like a proper extension to your Fusion 360 workflow. 
  Adjustments to generated reports should happen and refresh in real time (per 
  every save or at the execution of a command). I want to avoid the necessity 
  to refresh the browser to view updated content. If you have the browser 
  open on another monitor, it should feel "connected" to Fusion 360. 
