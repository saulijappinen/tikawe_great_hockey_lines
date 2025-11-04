# Log of dev stuff


**4.11.25**

First steps to release 2.0 (video nmbr 4 stuff)

* items_functions
* item_page for every record (not very good yet but working)

**28.10.25**

Released version 1.0, see NEWS.md. 

Basically stuff related to materials in videos 1-3 and weeks 1-3. Every thing is done with functions in app.py other than db_module. 


At least the following bugs are present: 

- database gets locked (only can add 1 user per session)
- session does not end if you don't log out (maybe?) - so the user stays while the app closes
- you can insert a line without logging in etc. stuff


**27.10.25**

Starting upp the repo and main stuff from week 1 materials. App now working with landing page, form and result but nothing else.  