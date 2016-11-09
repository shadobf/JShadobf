
try{
print = console.log 
arguments = process.argv.slice(2)
}
catch(err){
}





function f1 ( v1, v2, v3)
{


	v1 += v2 ;
	v3 += v1 ;
	return [v1,v2,v3]
}


function additem( l )
{

	l.push(10)
}

var ll, a1,a2,a3
a1 = 1 
a2 = 3 
a3 = 5


ll = f1( a1,a2,a3)

print (ll)  //		[ 4, 3, 9 ]
print (a1) // 		1
print (a2)	//		3
print (a3)	//		5
additem(ll)
print (ll)	//		[ 4, 3, 9, 10 ]



function clas()
{
	var t1;
	this.t1 = 1	
	t2 = 2
}

var c = new clas()
print (c.t1)	// 	1

print (c.t2)	//	undefined
print (c)		// 	{ t1: 1 }


clas.prototype.gett = function()
{
	return this.t1
}

print (c.gett())//	1


var a ;

if (true)
{
	a = 34;
	var a = 12;
}
print (a) //		12


function g()
{ 	
	a = 10;
	var a = 13;
	a = 14;
}
g()
print (a)	//		12



function h()
{ 	
	a = 10
	a = 14
}
h()
print (a)	//		14
function hh()
{ 	
	a = 20
	var a
}
hh()
print (a)	//		14



{
	var c = 0 
	c += 1 
	var u = [1,4,5]
	j = 100
	var j 
	j = 1000
	u.push (10)


	print  (u)
	print (c)
	print  (j)
}

print (u[0])



function addlist (i)
{
	i.push(10)
}
var cc = [1,2]

addlist(eval("cc"))
print (cc)
b1 = 12


//encountered region

function tl()
{
// F_before
	b1 = 10
	b2 = 3
// F_inside
	var b1
	b1 +=2
	b2 = 11
// F_after
	var b2
}
// v in F_vardec if "var v" in F
// v in F_vardec if "v=" in F and v not found upper 

//if "eval" => STOP

//v in F_vardec_before | v in encountered  & assigne  
// v=res[i]
//v in F_vardec_inside  & assigne 
// var=res[i]
//assign is v= v+= v-= 

//v ref in F_inside and not in F_vardec_inside
//v not a suffix
//
// f( v) 

function ttt(b1)
{
	var b1
	b1 +=2
	b2 = 11
	return [b1,b2]
}

function tll()
{
	b1 = 10
	b2 = 3
	var res = ttt(b1)
	var b1 = res[0]
	var b2 = res[1]
	var b2
}

tl()
print (b1)


var z = 100
function  printer_z()
{
	print (z)
}

printer_z()
function e()
{
	function  printer_z2()
	{
		print (z)
	}

	var z = 200;
	printer_z()
	printer_z2()
	z+=20
	print(z)
}
e()



var a = 30
{
	var a = 10 
{
	var a = 50 
	print (a)


}
	print (a)


}

	print (a)



cc = 1
var v = 0
function hf()
{

	if (true)	
	{

		var v
	}
	v = 10
	if (false)
	{
		var cc 
	}
	cc = 10
	print (v)
}
hf()
print(c)
print (v)












