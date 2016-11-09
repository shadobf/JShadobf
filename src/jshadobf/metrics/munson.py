from jshadobf.common.tree_walker import walker

#NOT IMPLEMENTED

def munson(program_tree):
    l,a = walker(program_tree,munson_func,munson_post_func,arg=[])
    s = 0
    return s
  
def munson_func(program,arg=[]):
    return [],arg
  
def munson_post_func(program,arg=[0]):
    return [],arg





























