#import Crypto.Hash.SHA256
#import Crypto.Hash.MD5
import hashlib
import cPickle
import os, sys, optparse

'''
Copyright 2012 Jacob Porter
Please attribute me if you use this file.
'''

#Global variables that control parameters.
#Number of files to read before printing a "." and pickling
CNT = 1000
#Default number of bytes to read for hashing the file
BYTES_TO_READ = 100000
#String delimiter for file strings with same hash code
str_sep = '  !*!!*!  '
#Default pickle value.  False won't pickle the hash table
pickle_me = False
#Should we use the SHA256 hash function?
USE_SHA256 = True


def get_all_possible_dups(path, f_str):
    '''
    Starting from the path file, this function
    searches for all potential duplicate files.
    It uses a hash function to search for them.
    f_str is the path of the pickle file to write to.
    This is in case the process crashes, but it isn't used
    by the process.
    '''
    print "Searching for duplicate files under " + path
    total_files = 0
    # Count the number of files
    for root, dirs, files in os.walk(path):
        for name in files:
            total_files += 1
    # Print helpful messages
    print "Using the first " + str(BYTES_TO_READ) + \
    " bytes in each file to search for duplicate files in " + str(total_files) + " total files."
    if (pickle_me):
        print "Duplication hash will be periodically pickled at: " + f_str 
    else:
        print "Duplication hash will NOT be pickled."
    if (USE_SHA256):
        str_hash = "SHA256"
    else:
        str_hash = "MD5"
    print "Using the " + str_hash + " hash function."
    # Set up hash tables and counting variables
    hashes = {}
    dups = {}
    count = 0
    num_unread = 0
    # Search through all the files
    for root, dirs, files in os.walk(path):
        for name in files:
            item = os.path.join(root, name)
            # Update status and pickle hash table if necessary
            if (count == CNT):
                count = 0
                sys.stdout.write('.')
                if (pickle_me):
                    pickle_file(f_str, dups)
            count += 1
            # Try opening a file.  Skip if can't open
            try:
                f = open(item, 'rb')
                s = f.read(BYTES_TO_READ)
            except:
                num_unread += 1
                continue
            # Append the file size to avoid collisions
            s += str(os.path.getsize(item))
            # Get the hash code for the file
            if (USE_SHA256):
                #my_raw = Crypto.Hash.SHA256.new(s)
                my_raw = hashlib.sha256(s)
            else:
                #my_raw = Crypto.Hash.MD5.new(s)
                my_raw = hashlib.md5(s)
            myhash = my_raw.hexdigest()
            f.close()
            # Search for duplicates and store path if necessary
            if (hashes.has_key(myhash)):
                if (dups.has_key(myhash)):
                    dups[myhash] += str_sep + item
                else:
                    dups[myhash] = item + str_sep + hashes[myhash] 
            else:
                hashes[myhash] = item
    # Write final pickle and return duplicates hash
    if (pickle_me):
        pickle_file(f_str, dups)
    sys.stdout.write('\n')
    print "A total of " + str(total_files - num_unread) + \
    " files were able to be read.  There were " + str(num_unread) + " unread files."
    return dups

def pickle_file(mp, stuff):
    '''
    Pickle stuff into file mp
    '''
    f1 = open(mp , 'wb')
    cPickle.dump(stuff, f1, protocol=cPickle.HIGHEST_PROTOCOL)
    f1.close()

def examine_dups(d, path_to_dup_list):
    '''
    Search through the duplicate hash in d
    Write the paths to the potential duplicate files to
    path_to_dup_list
    '''
    print "Writing duplicate file list: " + path_to_dup_list
    head_str =  "Number of potential duplicates found: " + str(len(d))
    print head_str
    f = open(path_to_dup_list, 'wb')
    f.write(head_str + '\n\n')
    for lst in d.values():
        astr = lst.split(str_sep)
        for s in astr:
            f.write(s + '\n')
        f.write('\n')
    f.close()
    

def main():
    '''
    This kicks off the process and 
    parses the options from the arguments.
    '''
    global USE_SHA256, pickle_me, BYTES_TO_READ
    p = optparse.OptionParser()
    # Path of the super directory to search for duplicates
    p.add_option('--path', '-p', default ="/")
    # Will use sha256 if this is true
    p.add_option('--sha', '-s', action='store_true')
    # Will use md5 if this is true
    p.add_option('--md5', '-m', action='store_true')
    # Will pickle the output hash table if true
    p.add_option('--pickle', '-l', action='store_true')
    # The number of bytes to read for each file to hash
    p.add_option('--read', '-r', default = "100000")
    # The path to the pickle file
    p.add_option('--pickle_file', '-e', default="dups_pickle.dmp")
    # The path to the text file to write duplicate file paths
    p.add_option('--dup_file', '-d', default="dups.txt")
    options, arguments = p.parse_args()
    if options.md5:
        USE_SHA256 = False
    if options.sha:
        USE_SHA256 = True
    if options.pickle:
        pickle_me = True
    path = options.path
    BYTES_TO_READ = int(options.read)
    examine_dups(get_all_possible_dups(path, options.pickle_file), options.dup_file)
    print "Done!"
    
if __name__ == '__main__':
    main()