deduper.py is a pytyhon utility that helps you find duplicate files in a directory and its subdirectories.  Use at your own risk.  There is no guarantee of good functioning.

It will write a text file giving a list of files that are potentially duplicates of each other.  It provides helpful run time messages to std.out


EXAMPLE USAGE : python deduper.py --path="C:/folder name/" --sha

Will use the SHA256 algorithm for finding duplicate files in C:/folder.  Will write a list of potential duplicate files to the C:/folder name/dups.txt

Can also use the MD5 hash by using --md5 instead of --sha

SHA256 is the default