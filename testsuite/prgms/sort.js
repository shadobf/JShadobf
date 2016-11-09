

function simpletrijava(list)
{
  var i,j;
  for(i = 0 ; i < list.length; i++)
  {
    for(j = i+1 ; j < list.length; j++)
    {
      var t;
      if(list[i]> list[j])
      {
        t=list[i];
        list[i] = list[j];
        list[j] = t;
      }
    }
  }
  return list;
}


var g;
function readeffr(err, file) { 
	 
                 if(err) {  
					g += file
  
                 }  
                 else{  
                } 
} 
function myread(file)
{
  //~ var reader = new BufferedReader( new InputStreamReader( new FileInputStream(file) ) );
  var nlist = [];
  var file;
  var data = "";
  //~ var buffer=new Buffer(100)
  //~ fd = fs.open(file, "r")
  var data = readfile(file);
  var data ;
  //~ fs.read(fd, buffer,0,100,0)
  //~ print (data)
  list = data.split("\n")
  for(i = 0 ; i < list.length; i++)
  {
	 if (list[i] != "")
	 {
		nlist.push(parseInt(list[i]));
	}
  }
  //~ print (nlist)
  //~ reader.close();
  return nlist;
}
function write(filenameout,list)
{
 var data = "";
 //~ print(list)
  for(i=0;i<list.length;i++) 
  {
	
    data +=""+list[i]+"\n"
  }	
  //~ print(data.length)
  writefile(filenameout,data)
  //~ print (filenameout)
  //~ fs.writeFileSync("./tmp/toto","jkjk" );
 
}
function main(args)
{
  var list;
  print("start");
  list = myread(args[0])
  list = simpletrijava(list);
  write(args[1],list);
}


var arguments_list  = arguments


main(arguments_list);


