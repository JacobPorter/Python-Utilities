#import Crypto.Hash.SHA256
#import Crypto.Hash.MD5
import hashlib
import cPickle
import os, sys, optparse

'''
Copyright 2012 Jacob Porter
Please attribute me if you use this file.
'''

CNT = 1000
BYTES_TO_READ = 100000
str_sep = '  !*!!*!  '
pickle_me = False
USE_SHA256 = True


def get_all_possible_dups(path, f_str):
    print "Searching for duplicate files under " + path
    total_files = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            total_files += 1
    print "Using the first " + str(BYTES_TO_READ) + " bytes in each file to search for duplicate files in " + str(total_files) + " total files."
    if (pickle_me):
        print "Duplication hash will be periodically pickled at: " + f_str 
    else:
        print "Duplication hash will NOT be pickled."
    if (USE_SHA256):
        str_hash = "SHA256"
    else:
        str_hash = "MD5"
    print "Using the " + str_hash + " hash function."
    hashes = {}
    dups = {}
    count = 0
    num_unread = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            item = os.path.join(root, name)
            if (count == CNT):
                count = 0
                sys.stdout.write('.')
                if (pickle_me):
                    pickle_file(f_str, dups)
            count += 1
            try:
                f = open(item, 'rb')
                s = f.read(BYTES_TO_READ)
            except:
                num_unread += 1
                continue
            s += str(os.path.getsize(item))
            if (USE_SHA256):
                #my_raw = Crypto.Hash.SHA256.new(s)
                my_raw = hashlib.sha256(s)
            else:
                #my_raw = Crypto.Hash.MD5.new(s)
                my_raw = hashlib.md5(s)
            myhash = my_raw.hexdigest()
            f.close()
            if (hashes.has_key(myhash)):
                if (dups.has_key(myhash)):
                    dups[myhash] += str_sep + item
                else:
                    dups[myhash] = item + str_sep + hashes[myhash] 
            else:
                hashes[myhash] = item
    if (pickle_me):
        pickle_file(f_str, dups)
    sys.stdout.write('\n')
    print "A total of " + str(total_files - num_unread) + " files were able to be read.  There were " + str(num_unread) + " unread files."
    return dups

def pickle_file(mp, stuff):
    f1 = open(mp , 'wb')
    cPickle.dump(stuff, f1, protocol=cPickle.HIGHEST_PROTOCOL)
    f1.close()

def examine_dups(d, path_to_dup_list):
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
    global USE_SHA256, pickle_me, BYTES_TO_READ
    p = optparse.OptionParser()
    p.add_option('--path', '-p', default ="/")
    p.add_option('--sha', '-s', action='store_true')
    p.add_option('--md5', '-m', action='store_true')
    p.add_option('--pickle', '-l', action='store_true')
    p.add_option('--read', '-r', default = "100000")
    p.add_option('--pickle_file', '-e', default="dups_pickle.dmp")
    p.add_option('--dup_file', '-d', default="dups.txt")
    options, arguments = p.parse_args()
    if options.sha:
        USE_SHA256 = True
    if options.md5:
        USE_SHA256 = False
    if options.pickle:
        pickle_me = True
    path = options.path
    BYTES_TO_READ = int(options.read)
    examine_dups(get_all_possible_dups(path, options.pickle_file), options.dup_file)
    print "Done!"
    
if __name__ == '__main__':
    main()