# Pylint report

## General

All pylint reports last run on `2025-10-12 16.30`

General comments on errors, applies on all reports

`C0114: Missing module docstring (missing-module-docstring)`

Decided not to include docstring notation in the beginning of modules, in stead modules are briefly explained in readme.md

`C0116: Missing function or method docstring (missing-function-docstring)`

Decided not to include docstring notation on functions.

`C0301: Line too long (107/100) (line-too-long)`

Decided to leave these too long lines if only considers comments because it is clearer to read them on one line. Also a few long code lines where it is also clearer in my mind to read the whole code on one line.

## app.py



```
app.py:19:0: C0301: Line too long (107/100) (line-too-long)
app.py:27:0: C0301: Line too long (107/100) (line-too-long)
app.py:203:0: C0301: Line too long (118/100) (line-too-long)
app.py:215:0: C0301: Line too long (147/100) (line-too-long)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:109:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:109:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:136:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:150:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:159:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:208:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:268:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:286:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:296:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:315:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:315:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:342:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:349:0: C0116: Missing function or method docstring (missing-function-docstring)

Your code has been rated at 8.84/10 (previous run: 8.79/10, +0.05)
```

**Comments**

`R1710: Either all return statements in a function should return an expression, or none of them should.`

In both cases, the functions (delete_item() and login()) have post and get methods. In my understanding, this is a warning if the case would be that the method is neither of them but in reality this is not possible.

## users.py

```
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)

Your code has been rated at 8.00/10 (previous run: 7.60/10, +0.40)
```

## items.py

```
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:6:0: R0913: Too many arguments (6/5) (too-many-arguments)
items.py:6:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
items.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:75:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:75:0: R0913: Too many arguments (6/5) (too-many-arguments)
items.py:75:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
items.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:134:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:140:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:161:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:173:0: C0116: Missing function or method docstring (missing-function-docstring)

Your code has been rated at 7.37/10 (previous run: 7.19/10, +0.18)
```

**Comments**

pylint triggers add_item() and update_item() which write to db in two parts. However all 6 arguments in the function are needed for the two db writes in total.

## config.py

```
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)

Your code has been rated at 5.00/10 (previous run: 0.00/10, +5.00)
```