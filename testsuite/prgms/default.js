rhino = true

try{
		importPackage(java.io);
		importPackage(java.lang);
		function readfile(file)
		{
	  		var reader = new BufferedReader( new InputStreamReader( new FileInputStream(file) ) );
		
			v = ""
			while ((strval = reader.readLine()) != null) {
				v+=strval +"\n"
			}
	
			reader.close();
			print(v)
			return v
		}

		
		function writefile(file,data)
		{
			print(file)
			var out = new BufferedWriter(new FileWriter(file));
			out.write(data);
			out.close();
		}


		 var br = new java.io.BufferedReader(new java.io.InputStreamReader(java.lang.System["in"]) );
		function prompt(s)
		{
			print (s)
			return br.readLine();
		};
		function readstdin()
		{	
			var v = ""
			while ((strval = br.readLine()) != null) {
				v+=strval +"\n"
			}
			return v
		}
}
catch(err){
	rhino = false
}
spidermonkey = false
if ( ! rhino) 
{
	try {
		File;
		function readfile(file)
		{
			f = File(file)
			f.open("read","text")
			a =  f.readAll()
			v = a.join("\n")
			f.close()
			return v
		};
		function writefile(file,data)
		{
			f = File(file)
			f.open("write,create", "text");
			a =  f.write(data)
			f.close()
		}
		function readstdin()
		{
			var v = ""
			while ((strval = readline()) != null) {
				v+=strval +"\n"
			}
			return v

		}
		spidermonkey = true
	}
	catch(err2)
	{

	}

}
if (! rhino && ! spidermonkey )
{
	try
	{
		print = console.log 
		arguments = process.argv.slice(2)
		var fs = require('fs');
		function readfile(file)
		{
			return fs.readFileSync(file,"binary")
		}
		function writefile(file,data)
		{
		fs.writeFileSync(file,data );
		}
	
		function readstdin()
		{


//			var readline = require('readline');
//			var rl = readline.createInterface({
//			  input: process.stdin,
//			  output: process.stdout
//			});

//			while ((strval = readline()) != null) {
//				v+=strval +"\n"
//			}


			return fs.readFileSync('/dev/stdin').toString()

			var endstdin = false
			process.stdin.resume();
			process.stdin.setEncoding('utf8');
			var userEntry;
			process.stdin.on('end', function () {
			 endstdin = true
			});
			var data = ""
	
			process.stdin.on('data', function (chunk) {
				data += chunk
			  }
			);
			while(endstdin)	
			{}
			return  data
		}
	}
	catch(e)
	{
	}

}
