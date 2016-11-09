#!/usr/bin/env python
import sys
import traceback
import os

import time
import subprocess
import ConfigParser
#print sys.path

import jshadobf
from jshadobf.common.convert import *
import compute_metrics

def print_metrics_in_line(list_dict):
    if len (list_dict) == 0 :
        return 
    keys = list(list_dict[0])

  
#  for k in 
  
    ks = list_dict[0].keys()
    ks.sort()
    print ("% 60s"+"% 10s"*(len(ks)-1)) % tuple(zip(*ks)[1])
    for l in list_dict:
        print ("% 60s"+"% 10s"*(len(ks)-1)) % tuple(map (lambda k:l[k]  ,ks))
#  for k in keys:
#    
#    print "% 10s"%k[1],":","% 20s"*len(list_dict) % tuple(map(lambda x: str(x[k]) , list_dict))

configfile="compare.conf"

if __name__=="__main__":
    import sys
    import optparse
  
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-C" :
            
            sys.argv[i]== "--config-file"
  
    optparser = optparse.OptionParser(usage="usage: %prog [options]",add_help_option=False)
#  optparser.disable_interspersed_args()

    optparser.add_option("-a" , "--all" ,dest="all",default=False, action='store_true',help="compute all the metrics")
    optparser.add_option("-1" , "--halstead" ,dest="halstead",default=False, action='store_true',help="compute the halstead metric")
    optparser.add_option("-2" , "--mccabe" ,dest="mccabe",default=False, action='store_true',help="compute the mccabe metric")
    optparser.add_option("-3" , "--harrison" ,dest="harrison",default=False, action='store_true',help="compute the harrison metric")
    optparser.add_option("-4" , "--oviedo" ,dest="oviedo",default=False, action='store_true',help="compute the oviedo metric")
    optparser.add_option("-5" , "--henry" ,dest="henry",default=False, action='store_true',help="compute the henry metric")
    optparser.add_option("-6" , "--munson" ,dest="munson",default=False, action='store_true',help="compute the munson metric")
    optparser.add_option("-f" , "--file" ,dest="file",default=[],action="append", help="file to compute the metrics on")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=0,action="count", help="verbose")
    optparser.add_option("-h" , "--help" ,dest="help",default=False,action="store_true", help="help")
#  optparser.add_option("-C" , "--config-file" ,dest="configfile",default="compare.conf", help="file containing the path for other obfuscator")

    c = ConfigParser.ConfigParser()
    c.read(configfile)
    obfs = c.sections()
    for obf in obfs :
        optparser.add_option( "--"+obf.replace("_","-") ,dest=obf,default=False,action='store_true', help="file containing the path for "+obf+" obfuscator")
  
  
    (option , arg ) = optparser.parse_args(sys.argv)
    if option.help :
        optparser.print_help()
        sys.exit(0)
  

#  optparser.add_option("-u" , "--uglifyjs-git" ,dest="uglifyjsgit",default=False,action="store_true", help="apply uglifyjs and the print the metrics (take the original file if exist otherwise the --file one)")
#  optparser.add_option("-g" , "--uglifyjs" ,dest="uglifyjs",default=False,action="store_true", help="apply uglifyjs and the print the metrics (take the original file if exist otherwise the --file one)")
#  optparser.add_option("-y" , "--yuicompressor" ,dest="yuicompressor",default=False,action="store_true", help="apply yuicompressor and the print the metrics (take the original file if exist otherwise the --file one)")
#  optparser.add_option("-c" , "--closure-compiler" ,dest="closure_compiler",default=False,action="store_true", help="apply closure-compiler and the print the metrics (take the original file if exist otherwise the --file one)")



    print option
    if option.file == []:
        optparser.print_help()
        sys.exit()
    if option.all :
        option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry = [True]*5

  
    values = compute_metrics.compute_metrics(option.file,option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry)
#  opt = [ "--unsafe", "--lift-vars" , "-mt"]
#
#  def genpos (l):
#    if len (l) == 1 :
#      return [l]
#    return [l[0:1]] + genpos(l[1:]) + map(lambda it: l[0:1]+it,genpos(l[1:]))
#  print option.__class__
#  print dir (option)

    for f in option.file:

        for obf in obfs :
            if getattr(option,obf):
  #
  #      try:
  #        ff=os.path.basename(f)
  #        n = compute_metrics.getnewfilename(prefix=ff+"-yui")
  #        ret = compute_metrics.execute_command("java -jar "+absp+"/../../yuicompressor/build/yuicompressor-2.4.8pre.jar -o " + n +" "  + f,verbose=option.verbose )
  #        yuifiles.append(n)
  #      except Exception:
  #        print "YUI compressor failed on "+f
                try:
                    ff=os.path.basename(f)
                    ff=ff[:ff.rfind(".")]
                    cmd = c.get(obf,"path")
                    options = c.get(obf,"option")
                    n = compute_metrics.getnewfilename(prefix=obf+"_"+ff+"_obf_")
                    options=options.replace("INFILE",f)
                    options=options.replace("OUTFILE",n)
                    print options
                    ret = compute_metrics.execute_command(cmd + " " + options  ,verbose=option.verbose)
                except Exception,e:
                    print e
                    print obf,"failed on",f
                try:
                    print "add value"
                    print n
                    values += compute_metrics.compute_metrics([n],option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry,option.verbose)
                except Exception,e:
                    print e
                    print obf,"failed on",f
  #
  #  for optionpos in [""]+ genpos(opt):
  #    if option.uglifyjsgit:
  #      uglyfiles = []
  #      for f in  option.file:
  #        try:
  #          ff=os.path.basename(f)
#          n = compute_metrics.getnewfilename(prefix=ff+"-ugit"+"".join(optionpos))
#          ret = compute_metrics.execute_command(absp+"/../../UglifyJS/bin/uglifyjs " + " ".join(optionpos)+  " -o " + n+ " " + f  ,verbose=option.verbose)
##          f = open(n,"w")
##          f.write(ret)
##          f.close()
#  
#
#          uglyfiles.append(n)
#        except Exception:
#          print "UgligyJS git version failed on "+f+", think of updating the git repository"
#  
#      values += compute_metrics.compute_metrics(uglyfiles,option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry)
#
#    if option.uglifyjs:
#      uglyfiles = []
#      for f in  option.file:
#  
#        try:
#          ff=os.path.basename(f)
#          n = compute_metrics.getnewfilename(prefix=ff+"-ug"+"".join(optionpos))
#          ret = compute_metrics.execute_command("uglifyjs " + " ".join(optionpos)+ " -o " + n + " " + f  ,verbose=option.verbose)
#          uglyfiles.append(n)
#        except Exception:
#          print "UgligyJS failed on "+f
#
#
#      values += compute_metrics.compute_metrics(uglyfiles,option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry)
#  if option.uglifyjs:
#    yuifiles = []
#
#    for f in  option.file:
#
#      try:
#        ff=os.path.basename(f)
#        n = compute_metrics.getnewfilename(prefix=ff+"-yui")
#        ret = compute_metrics.execute_command("java -jar "+absp+"/../../yuicompressor/build/yuicompressor-2.4.8pre.jar -o " + n +" "  + f,verbose=option.verbose )
#        yuifiles.append(n)
#      except Exception:
#        print "YUI compressor failed on "+f
#
#  
#    values += compute_metrics.compute_metrics(yuifiles,option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry)
#    
#  if option.closure_compiler:
#    yuifiles = []
#
#    for f in  option.file:
#
#      try:
#        ff=os.path.basename(f)
#        n = compute_metrics.getnewfilename(prefix=ff+"-yui")
#        ret = compute_metrics.execute_command("java -jar "+absp+"/../../yuicompressor/build/yuicompressor-2.4.8pre.jar -o " + n +" "  + f,verbose=option.verbose )
#        yuifiles.append(n)
#      except Exception:
#        print "YUI compressor failed on "+f

  
#    values += compute_metrics.compute_metrics(yuifiles,option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry)
    
  
    print_metrics_in_line(values)


