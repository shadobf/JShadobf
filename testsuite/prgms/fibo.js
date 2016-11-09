


function fibo(n)
{
  if( n <= 1 )
  {
    return n;
  }
  var res = fibo(n-1) + fibo(n-2);
  return res;
}

console.log( fibo(10))

