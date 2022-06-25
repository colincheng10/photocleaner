import os
import hashlib
import logging
import sys

def logger():
    """ get logger"""
    logger = logging.getLogger()
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        file_handler = logging.FileHandler("test.log")
        file_handler.setFormatter(formatter) 
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter 
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    return logger

def get_md5(filename, size):
    m = hashlib.md5()
    mfile = open(filename, "rb")
    m.update(mfile.read(size))
    mfile.close()
    md5_value = m.hexdigest()
    return md5_value

def get_urllist(basedirs):
    jpgList = []
    movList = []
    for base in basedirs:
        #base = ("./")
        #base = ("/Volumes/TOSHIBA/Photos")
        #base = ("/Users/yin/Pictures/Unsort")
        for dirpath,dirnames,filenames in os.walk(base):
            for filename in filenames:
                url = os.path.join(dirpath,filename)
                if os.path.isfile(url) == True and os.path.getsize(url) > 4096: 
                    urlname = os.path.basename(url)
                    if urlname.endswith('.PNG') or urlname.endswith('.JPG') :
                        jpgList.append(url)
                    elif urlname.endswith('.MOV') or urlname.endswith('.mp4') or urlname.endswith('.MP4') :
                        movList.append(url)
                    else :
                        print("skip: %s", urlname)        

    return  jpgList, movList

# usage: python photocleaner/photocleaner.py /Users/yin/Pictures/Unsort /Users/yin/Pictures/xx/

if __name__ == '__main__':

    argv = sys.argv[1:]
    print('check dir: ', argv)

    log = logger()

    jpgList, movList =get_urllist(argv) 

    md5Set = set()
    md5Dict = dict()

    for a in movList:
        md5 = get_md5(a, 3*1024*1024)
        if (md5 in md5Set):
            print("repeat: ", a)
            print("origin: ", md5Dict[md5])
            #log.info("repeat: %s" %a)
            #os.remove(a)
        else:
            md5Set.add(md5)
            md5Dict[md5] = a
            #print("add: ", a)

    print("find mov:%d", len(md5Set))

    md5Set.clear()
    md5Dict.clear()

    for a in jpgList:
        md5 = get_md5(a, 512*1024)
        if (md5 in md5Set):
            print("repeat: ", a)
            print("origin: ", md5Dict[md5])
            #log.info("repeat: %s" %a)
            #os.remove(a)
        else:
            md5Set.add(md5)
            md5Dict[md5] = a
            #print("add:%s" %a)
            
    print("find pic: %d", len(md5Set))


