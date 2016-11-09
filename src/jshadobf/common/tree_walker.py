
def walker(program,function=lambda x,y : ([] ,y),postfunction=lambda x,y : ([] ,y),arg=None,walk_condition=lambda x,y: True):
    if program == None:
        return [], arg
    else:
        ret,arg= function(program,arg)
        if walk_condition(program,arg):
            for s in program.getChildren():
                r,arg = walker(s,function,postfunction,arg,walk_condition=walk_condition)
                ret = ret + r
        r,arg= postfunction(program,arg)
        ret = ret + r
    return ret ,arg

