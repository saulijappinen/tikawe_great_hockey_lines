# Log of dev stuff



**17.11.25**

Edit, update, delete now forbidden for other users (previously could be done with changing url/website hidden field)


**12.11.25**

Release version 2.0 with meta docs updated. 

**11.11.25**

Final steps for realase 2.0, but still needs to be pushed. 


**4.11.25**

First steps to release 2.0 

* (video nmbr 4 stuff)
  * items_functions for getting items
  * item_page for every record (not very good yet but working)

* video 5 stuff
  * item_edit & update_item function working (main info)
    * FIXME: still not showing all the previous values in item_edit.html

**28.10.25**

Released version 1.0, see NEWS.md. 

Basically stuff related to materials in videos 1-3 and weeks 1-3. Every thing is done with functions in app.py other than db_module. 


At least the following bugs are present: 

- database gets locked (only can add 1 user per session)
- session does not end if you don't log out (maybe?) - so the user stays while the app closes
- you can insert a line without logging in etc. stuff


**27.10.25**

Starting upp the repo and main stuff from week 1 materials. App now working with landing page, form and result but nothing else.  