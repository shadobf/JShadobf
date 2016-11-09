
try{
print = console.log 
arguments = process.argv.slice(2)
}
catch(err){
}








function parameter_writer_list(p)
{
  p.push(3)
 
}


function parameter_writer_string(p)
{
  p = p + "toto"
 
}

p = "tata"
parameter_writer_string(p)
print( p)

p = [1,2,3]
parameter_writer_list(p)
print (p)


