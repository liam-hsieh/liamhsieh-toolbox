# toolbox.container

## toolbox.container.namedtuple_from_dict
*function*, Create and return a namedtuple instance with fields populated from a dictionary.
```nohighlight
This function dynamically creates a new namedtuple class with a given name and fields corresponding to the keys of the source dictionary. The values of the namedtuple are filled with the values from the source dictionary.

Args:
    source_dict (dict): The dictionary whose keys and values are to be used to create the namedtuple.
    name (str): The name of the new namedtuple class to be created.

Returns:
    namedtuple: An instance of the newly created namedtuple class, populated with data from the source_dict.
```

## toolbox.container.BoundFuncAsClsMethod
*class*, bound functions as methods of a class; non simple mode supports those methods to access properties from the class where we attach to 
```nohighlight

Args:
    mapper (dict): _description_
    class_to_attach_on (_type_, optional): _description_. Defaults to None.
    simple_mode (bool, optional): _description_. Defaults to True.
```

**Example:**
```python
def m1(self):
    return f"{self.user_name}'s method 1"

def m2(self):
    return self.msg

def m3(self,favorite):
    return f"{self.user_name} likes {favorite}"

method_mapper = {
    "method1":m1,
    "method2":m2,
    "method3":m3,
}

# simple mode
class Tester:
    def __init__(self,user_name):
        self.user_name=user_name
        self.methods = BoundFuncAsClsMethod(method_mapper)

tester=Tester("Liam")
tester.msg="original msg"

# method 1 can access tester.user_name
print(tester.methods.method1(tester))

# method2 can access tester.msg while instance of Tester has been passed to m2 as an arg during initilization
print(tester.methods.method2(tester))

# modify the content of msg
tester.msg="new one"

# the output also changes
print(tester.methods.method2(tester))

# testing how it handles additional argument 
print(tester.methods.method3(tester,"guava"))

# Non simple mode
class Tester:
    def __init__(self,user_name):
        self.user_name=user_name
        self.methods = BoundFuncAsClsMethod(method_mapper, self, simple_mode=False)

tester=Tester("Liam")
tester.msg="original msg"

# passing or not passing tester as arg for mehtod1 has the same result
print(tester.methods.method1())

# passing or not passing tester as arg for mehtod1 has the same result
print(tester.methods.method2())

# modify the content of msg
tester.msg="new one"

# the output also changes
print(tester.methods.method2())

# testing how it handles additional argument 
print(tester.methods.method3(tester,"guava"))
```

**Output**
In this example, both modes will have the same output as follows:
```nohighlight
Liam's method 1
original msg
new one
Liam likes guava
```        

