print=console.log
object = { 
  a:7, 
  get b() { return this.a+1; }, 
  set c(x) { this.a = x/2 } 
};
print(object.a)
print(object.b)
object.c = 50
print(object.a)

