print = console.log

var a = 10;

function f()
{
	a = a +1;
	print(a)
}


function f1()
{
	var a = 0;
	function f2()
	{
		f()
	}
	f()
	f2()
}
f()
f1()

each=3
print(each)
get=4
print(get)
set=5
print(set)

