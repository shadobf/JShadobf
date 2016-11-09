for each (var i in [1,2,3,4])
{
	print (i)
}


function map(i,f) {
	for(let x in i ) {
	yield f(x);
	}
};
let vv = 1;

let ff = map([1,2,3,4],function (x){return x*x;});


//ff.foreach(function(i)
//{
//	print (i)
//}
//);


for ( i in ff)
{
print (i);
}

var xx ;
let (x = 1) xx = x;
try
{
print (x)
}
catch(e)
{
print(e)
}
print (xx)


let (v = "v" ) {print (v)};


print ( [ i=x for each (x in [1,2,3,4])])

