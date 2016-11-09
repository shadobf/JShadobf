
// Closure to make modules
var prop, obj;

(function(global) {
    global.MY_MODULE = global.MY_MODULE || {};

    // private API
    var hidden_variable = "I'm a hidden value.";

    function hidden_function() {
        print("You called a hidden function.</br>");
    }
    // public API
    global.MY_MODULE.publicFunction = function() {
        print("Public function calling a hidden one... </br>");
        hidden_function();
    };
    // a classical Constructor Function
    global.MY_MODULE.PublicObject = function() {
        this.public_variable = "I'm a public value";
        this.publicMethod = function() {
            print("<p>Public method of public object using</p> <ul><li>public variables like: \"" + this.public_variable + "\" </li><li>and hidden ones like: \"" + hidden_variable + "\"</li></ul>");
        };
    };

})(this);


print("MY_MODULE's visible properties: <ul>");
for (prop in this.MY_MODULE) {
    print("<li>" + prop + "</li>");
}
print("</ul>");

this.MY_MODULE.publicFunction();

obj = new this.MY_MODULE.PublicObject();
obj.publicMethod();
