
deduper.py
--------------------------------
deduper.py is a pytyhon utility that helps you find duplicate file contents in a directory and its subdirectories.  Use at your own risk.  There is no guarantee of good functioning.

Built using python 2.7.  Python must be installed for this file to be run.
Doesn't need any non-native modules to run.  Uses hashlib.

It will write a text file giving a list of files that are potentially duplicates of each other.  Some files marked as duplicates may not be duplicates because of hash collisions.
The process provides helpful run time messages to std.out.


EXAMPLE USAGE : 
$$>python deduper.py --path="C:/folder name/" --sha

Will use the SHA256 algorithm for finding duplicate files in C:/folder name/.  Will write a list of potential duplicate files to the C:/folder name/dups.txt by default, but this can be configured.
Can also use the MD5 hash by using --md5 instead of --sha for the runtime parameter.
SHA256 is the default when no parameter is specified.



OTHER USAGE:
In the command line after the file name, the following parameters can be specified.
 --path="pathname" to specify the super directory that you would like to search.  It automatically searches all subdirectories.  The default is the root directory.
 --sha to specify using the sha256 hash algorithm.  This is turned on by default
 --md5 to use the md5 hash function.
 --read="int_value"  The int_value is the number of bytes to read from each file to determine if the file is a duplicate.  
A larger value means a lower likelihood of hash collisions and thus fewer false duplicates, but it will take longer to run.  The default is 100,000 bytes = 100 kb.
 --pickle This paramter periodically (every 1000 files) writes the hash table for the files.  Useful if the system crashes, then you have some information,
but it does not affect the process.  The default is to turn this off.
 --pickle_file="pickle path and file name"  Sets the path and file name of the pickle file.  Defaults to "dups_pickle.dmp" and writes to --path
 --dup_file="dup path and file name"  Sets the location and file name of the duplicate file that is written at the end of the process
Defaults to "dups.txt" and writes the file to the path in --path


KNOWN PROBLEMS AND ISSUES:
Some files could be marked as duplicates when they are not.  This could be because some files will have many identical bytes at the top of the file but different bytes at the end.
Deduper.py uses the first bunch of bytes (as well as the file size) to hash the file and compares hashes from that to determine if the file is a duplicate.  
The process could look at more information to eliminate this problem.

This utility ignores the filename and hashes the first bunch of bytes of the file concatenated with the file size.  
This is okay since duplicate file contents might not have the same file name.

Always recurses down directories.  No way yet to control this yet.

Uses the kludgey string '  !*!!*!  ' to seperate file paths.  The problem is that a file could have this string in its name causing the process to break the path in the wrong part
when printing the duplication file at the end.  This won't affect finding potential duplicates though.
This was used since I couldn't figure out how to hash a list of strings.  For some reason it wouldn't work.

If the duplication hash grows to large for RAM, the process will crash without completing.  This could be fixed by writing to disc using the existing pickle mechanics.

If the number of files to search is to much to hold in an integer field, the process will crash.

If it can't read a file, it skips it.

No graphical interface.

Python must be installed on the system.  Non-executable file.


