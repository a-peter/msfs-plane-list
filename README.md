This is a very basic version of a tool that tries to detect
the data folders of a Microsoft Flight Simulator 2020 version.

When found, it reads all aircrafts that are present inside
these folders. It will export a list of aircrafts along with
some data on these aircrafts to an excel file and to a 
csv file.

The execution will be logged into the file aircrafts.log.

No license, just take the code and use it as you like.

# Instructions

Just run the .exe file or (if you have installed Python)
the `msfs_plane_list.py`.

The program tries to find the configuration files for 
the MS Store and the Steam variant.

After execution you'll have an Excel file and a CSV file
containing a list of airplanes.

# Blacklist

If you find something inside the list wich is *no* aircraft,
you can create a file `blacklist.txt` containing the folder
name to be ignored.

# Issues 

If you have any issues, just create an issue at
[here](https://github.com/a-peter/msfs-plane-list/issues).
I maybe ask for more details on your issue.