# Release 2.0 / 12.11.25

*Items can be altered and searched*

+ [x] Adding and modifying items 
  + [x] an item can be modified (only by the user who created it)
  + [x] an item can be deleted (only by the user who created it)
  + [x] database can be searched (to all registered users)
- [x] items added to database are shown (when a user has logged inß)

Notes

+ currently, only line and player names are added to database even though it is possible to enter more information in the html page (add line)
  + accordingly, only those attributes can be edited
+ the search functionality only searches for keywords in line name


----

# Release 1.0 / 28.10.25

*Basic stuff works without displaying the items*

Features that work 

+ [x] User stuff
  + [x] user can create an account, log in and out 
  + [x] users are written to db (users)
+ [x] Adding and modifying items 
  + [x] an item (line) can be added
  + [x] gets written to db (items)
+ Other
  + [x] some custom prints for example after registering etc. 

Technical status

+ all is done with functions and/or html pages, no special modules other than db_module and config.py 
