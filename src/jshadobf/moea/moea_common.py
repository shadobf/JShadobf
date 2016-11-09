import tempfile
import os 
import cPickle

available_objectives = ["exectime","mu1","mu2","mu3","mu4","mu5","summu","mu1mu2","mu1mu2mu3","mu1mu2mu3mu4"]
timeout = 20*60

def getnewname_inc(directory,prefix="temp."):
    if not os.path.isdir(directory):
        os.makedirs (directory)
    l = os.listdir(directory)
    return directory + os.sep + prefix + "%03d"%len(l)

def getnewname(directory,prefix="temp."):
    if not os.path.isdir(directory):
        os.makedirs (directory)
    return tempfile.mktemp(suffix='', prefix=prefix, dir=directory)

def deepcopy(d):
    return cPickle.loads(cPickle.dumps(d, -1))
