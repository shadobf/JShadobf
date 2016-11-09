import sys

def print_level_order_and_id(tree, indent=0,printable=[]):
    if tree.__class__ in printable:
        print '{1}:{0}'.format('   '*indent,tree.getLine()), tree.text , "0x%x"%id(tree),str(tree)
    else:
        print '{1}:{0}'.format('   '*indent,tree.getLine()), tree.text , "0x%x"%id(tree)
    for child in tree.getChildren():
        print_level_order_and_id(child, indent+1)
    
def print_level_order(tree, indent=0,printable=["Ident","List","Number","Ltrue","Lfalse"]):
    classname = str(tree.__class__)
    if classname.find(".") != -1:
        classname = classname[classname.rfind(".")+1:]
    if classname in printable:
        print '{1}:{0}'.format('   '*indent,tree.getLine()), tree.text,str(tree)
    else:
        print '{1}:{0}'.format('   '*indent,tree.getLine()), tree.text
    for child in tree.getChildren():
        print_level_order(child, indent+1,printable)

def print_tree(tree):
    sys.stdout.write(str(tree.text)+"(")
    i = 0
    for child in tree.getChildren():
        if i != 0:
            sys.stdout.write(",")
        i = i + 1
        print_tree(child)
    sys.stdout.write(')')
