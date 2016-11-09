

  function Matrix (ary)   {
    (this.mtx = ary);
    (this.height = ary.length);
    (this.width = ary[0].length);
    }
    
  (Matrix.prototype.mult = function (other)   {
    if((this.width!=other.height))
      {
      }
      
    var result = [];
    for (var i = 0;(i<this.height);(i++))
      {
      (result[i] = []);
      for (var j = 0;(j<other.width);(j++))
        {
        var sum = 0;
        for (var k = 0;(k<this.width);(k++))
          {
          (sum += (this.mtx[i][k]*other.mtx[k][j]));
          }
          
        (result[i][j] = sum);
        }
        
      }
      
    return new Matrix (result);
    }
    
  );
  function read (file)   {
    var matrix = [];
    var file;
    var data = "";
    var data = readfile (file,"binary");
    var data;
    (list = data.split ("\n"));
    for ((i = 0);(i<list.length);(i++))
      {
      if((list[i]!=""))
        {
        var line = list[i].split (",");
        var tline = [];
        for (var j = 0;(j<line.length);(j++))
          {
          tline.push (parseInt (line[j]));
          }
          
        matrix.push (tline);
        }
        
      }
      
    return matrix;
    }
    
  function write (filenameout,list)   {
    var data = "";
    var i;
    for ((i = 0);(i<list.mtx.length);(i++))
      {
      for (var j = 0;(j<list.mtx[i].length);(j++))
        {
        if((j!=0))
          {
          (data += ",");
          }
          
        (data += (""+list.mtx[i][j]));
        }
        
      (data += "\n");
      }
      
    writefile (filenameout,data);
    }
    
  function main (args)   {
    var list;
    var a,b,c;
    print ("start");
    (a = new Matrix (read (args[0])));
    (b = new Matrix (read (args[1])));
    (c = a.mult (b));
    write (args[2],c);
    }
    
  var args = arguments;
  var argument = [args[0],args[1],args[2]];
  main (argument);
  
