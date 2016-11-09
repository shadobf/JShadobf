
// Async task (same in all examples in this chapter)
function async(arg, callback) {
  print('do something with \''+arg+'\', return .001 sec later');
  setTimeout(function() { callback(arg * 2); }, 1);
}
// Final task (same in all the examples)
function final() { print('Done', results); }

// A simple async series:
var items = [ 1 ];
var results = [];
function series(item) {
  if(item) {
    async( item, function(result) {
      results.push(result);
      return series(items.shift());
    });
  } else {
    return final();
  }
}
series(items.shift());


print('process.env', process.env);
if(module === require.main) {
  print('This is the main module being run.');
}


var SimpleEE = function() {
  this.events = {};
};
SimpleEE.prototype.on = function(eventname, callback) {
  this.events[eventname] || (this.events[eventname] = []);
  this.events[eventname].push(callback);
};
SimpleEE.prototype.emit = function(eventname) {
  var args = Array.prototype.slice.call(arguments, 1);
  if (this.events[eventname]) {
    this.events[eventname].forEach(function(callback) {
      callback.apply(this, args);
    });
  }
};
// Example using the event emitter
var emitter = new SimpleEE();
emitter.on('greet', function(name) {
  print('Hello, ' + name + '!' );
});
emitter.on('greet', function(name) {
  print('World, ' + name + '!' );
});
['foo', 'bar', 'baz'].forEach(function(name) {
  emitter.emit('greet', name);
});










var Foo2 = function (name) { this.name2 = name; };

var Foo = function (name) { this.name = name; };
Foo.prototype.data = [1, 2, 3]; // setting a non-primitive property
Foo.prototype.var2 = Foo2(); // setting a non-primitive property
Foo.prototype.showData = function () { print(this.name, this.data); };
 
var foo1 = new Foo("foo1");
var foo2 = new Foo("foo2");
 
// both instances use the same default value of data
foo1.showData(); // "foo1", [1, 2, 3]
foo2.showData(); // "foo2", [1, 2, 3]
 
// however, if we change the data from one instance
foo1.data.push(4);
 
// it mirrors on the second instance
foo1.showData(); // "foo1", [1, 2, 3, 4]
foo2.showData(); // "foo2", [1, 2, 3, 4]




function Foo(name) {
  this.name = name;
  this.data = [1, 2, 3]; // setting a non-primitive property
};
Foo.prototype.showData = function () { print(this.name, this.data); };
var foo1 = new Foo("foo1");
var foo2 = new Foo("foo2");
foo1.data.push(4);
foo1.showData(); // "foo1", [1, 2, 3, 4]
foo2.showData(); // "foo2", [1, 2, 3]



function Animal(name) {
  this.name = name;
};
Animal.prototype.move = function(meters) {
  print(this.name+" moved "+meters+"m.");
};

function Snake() {
  Animal.apply(this, Array.prototype.slice.call(arguments));
};
Snake.prototype = new Animal();
Snake.prototype.move = function() {
  print("Slithering...");
  Animal.prototype.move.call(this, 5);
};

var sam = new Snake("Sammy the Python");
sam.move();
 
 var obj = { has_thing: true, id: 123 };
 if(obj.has_thing) {
 	print('true', obj.id);
 }





print(2 == "2"); // true
print(2 === "2"); // false
var arr = ["1", "2", "3"];
// Search the array of keys
print(arr.indexOf(2)); // returns -1
print(arr.indexOf("2")); // returns 1


var types = ['text/html', 'text/css', 'text/javascript'];
var string = 'text/javascript; encoding=utf-8';
if (types.some(function(value) {
    return string.indexOf(value) > -1;
  })) {
  print('The string contains one of the content types.');
}


var a = [ 'a', 'b', 'c' ];
var b = [ 1, 2, 3 ];
print( a.concat(['d', 'e', 'f'], b) );
print( a.join('! ') );
print( a.slice(1, 3) );
print( a.reverse() );
print( ' --- ');
var c = a.splice(0, 2);
print( a, c );
var d = b.splice(1, 1, 'foo', 'bar');
print( b, d );



function match(item, filter) {
  var keys = Object.keys(filter);
  // true if any true
  return keys.some(function (key) {
    return item[key] == filter[key];
  });
}
var objects = [ { a: 'a', b: 'b', c: 'c'},
  { b: '2', c: '1'},
  { d: '3', e: '4'},
  { e: 'f', c: 'c'} ];

objects.forEach(function(obj) {
  print('Result: ', match(obj, { c: 'c', d: '3'}));
});


var obj = {
  items: ["a", "b", "c"],
  process: function() {
    var self = this; // assign this to self
    this.items.forEach(function(item) {
      // here, use the original value of this!
      self.print(item);
    });
  },
  print: function(item) {
    print('*' + item + '*');
  }
};
obj.process();

if(true){
  function toto (n) {
	return n
  }
  function getarg (argum) {
	print("inside")
  }
  (n = toto(10));
  print(n)
}

