


function f1()
{

	function f2()
	{
		c += 10
		b += 10
	}
	var c = 1
	print (c)
	f2()
	print (c)
}
var c = 2
var b = 0


print (b,c)
f1()
print (b,c)

f3()
function f3()
{
	f2()
	function f2()
	{
		c += 100
		b += 100
	}
	var c = 1
	print (c)
	f2()
	print (c)
}

print (b,c)
f3()
print (b,c)

