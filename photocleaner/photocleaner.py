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

def get_md5(filename):
    m = hashlib.md5()
    mfile = open(filename, "rb")
    m.update(mfile.read())
    mfile.close()
    md5_value = m.hexdigest()
    return md5_value

def get_urllist():
    #base = ("./")
    base = ("/Volumes/TOSHIBA/Photos")
    urlList=[]
    for dirpath,dirnames,filenames in os.walk(base):
        for filename in filenames:
            url = os.path.join(dirpath,filename)
            if os.path.isfile(url) == True and os.path.getsize(url) > 4096: 
                urlList.append(url)
    return  urlList

if __name__ == '__main__':
    log = logger()
    md5List =[]
    urlList =get_urllist()
    for a in urlList:
        md5 =get_md5(a)
        if (md5 in md5List):
            os.remove(a)
            print("repeat:%s" %a)
            log.info("repeat:%s" %a)
        else:
            md5List.append(md5)
            # print(md5List)
            # print("all %s photos"%len(md5List))
