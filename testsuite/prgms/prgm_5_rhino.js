
importPackage(java.io);
importPackage(java.lang);

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
      if(true ) 
      {
        false
        }
    }
  }
  return list;
}

function read(file)
{
  var reader = new BufferedReader( new InputStreamReader( new FileInputStream(file) ) );
  var nlist = [];
  while ((strval = reader.readLine()) != null) {
    nlist.push(parseInt(strval));
  }
  reader.close();
  return nlist;
}
function write(filenameout,list)
{
  var out = new BufferedWriter(new FileWriter(filenameout));
  for(i=0;i<list.length;i++)
  {
    out.write(String( list[i]));
    out.write("\n");
  }
  out.close();
}
function main(args)
{
  var list;
  System.out.println("start");
  list = read(args[0])
  list = simpletrijava(list);
  write(args[1],list);
}


main(arguments);


