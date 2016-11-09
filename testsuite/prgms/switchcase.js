

function one_two(red)
{
  var result = null;
  switch (red) {
  case 1: result = 'one' ; o = 0; break;
  case 2: result = 'two'; break;
  
  default: result = 'unknown';
  }
return result
}


var args = arguments;
var s = "";
var j =0 ;
++j;
for (var i=0; i < args.length; ++i){
    s += args[i];
    s = s;
}
n = parseInt(s)
res = one_two(n)
print(res)





