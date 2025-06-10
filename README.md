# Windows-Printer-Add-Tool

Adding printers from a network print server can be tedious through the Windows GUI. It requires several clicks, confirmations, and manually connecting to the print server. Additionally, you must restart the process for each new printer you want to install. I built a tool to quickly add multiple printers from a defined print server.

## Features
- Built in print server access: PowerShell command (running thru subprocess) connects and gets the list of printers.
- Multiple printer selection: App works through printers in order, installing them one-by-one automatically.

## Version History
6-10-25: Initial version
Future versions: add option to use default print server or to select or add one (for an org with multiple print servers). Add scroll bar in interface. 

