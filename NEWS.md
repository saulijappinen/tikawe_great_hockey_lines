# Release v5.5 / 7.12.25

*Small improvements*

Notes

* key new features
  * length limits to text input (add / edit line)
  * search now works in all txt fields
  * not able to insert empty classes
  
* fixed bugs
  * delete item 

+ known bugs in current functionalities
  + class number check only checks amount of inputs, not that both league and nationality have been inserted


# Release v5 / 5.12.25

*Bugfixes, classes now working better, flash msgs for user stuff*

Notes

+ key new features
  + selected classes now showing more nicely on item page
  + flash msgs for user registering, login errors
  
* fixed bugs
  * chosen classes now showing in edit

+ known bugs in current functionalities
  + no requirement for selecting at least one class 
  

# Release v4.0 / 27.11.25

*Classes added (edit not yet working completely) and ratings possible*

Notes

+ key new features
  + classes (nationalities and league) now available for adding and editing
  + rating other users lines is possible

+ known bugs in current functionalities
  + in line edit, the predifined classes are not showing. however the edit itself works 


# Release v3.0 / 18.11.25

*Some under the hood updates and user page*

Under the hood

+ csrf 
+ url errors (html 403/404)
+ timestamps to user and items
+ bugfixes
  + update_items: correct function name

User pages

+ shows user name, added lines and creation date of the user account 

Notes

+ currently, only line and player names and modification time are added to database even though it is possible to enter more information in the html page (add line/edit line)
  + accordingly, only those attributes can be edited
+ the search functionality only searches for keywords in line name

# Release v2.0 / 12.11.25

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

# Release v1.0 / 28.10.25

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
