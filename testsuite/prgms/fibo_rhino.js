  
importPackage(java.io);
importPackage(java.lang);
 
function fibo(n)
{
  if( n <= 1 )
  {
    return n;
  }
  var res = fibo(n-1) + fibo(n-2);
  return res;
}

function ()
{
var number1 = 3, number2 = 2, result;
result = number1 * number2;
}

var args = arguments;
var s = "";
var j =0 ;
++j;
for (var i=0; i < args.length; ++i){
    s += args[i];
    s = s;
}
n = parseFloat(s)
System.out.println(fibo(n))


a = b = 3
