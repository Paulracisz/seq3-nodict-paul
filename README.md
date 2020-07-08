<img height="120" src="img/200-no-dictionaries-pls.png" />

# NoDict - A dictionary without a dictionary
For this assignment, you will be using Python classes to create a new object that behaves like a dictionary in Python, but you are not allowed to use a built-in dictionary in your implementation. The purpose is to gain a better understanding of how dictionaries function under the hood by creating your own.

This assignment focuses on creating a data structure that can be used in other programs rather than building a concrete, real-world application. Customized data structures go together with Python naturally since Python is an object-oriented language.

Be sure to review this entire README before you get started. There are a lot of guidelines and hints to help you if you get stuck. Please resist the urge to 'skim'.

You will create a single class named `NoDict` that performs the primary functions of a dictionary:
- Association of key/value pairs
- Ability to insert a new key/value entry or update an existing entry
- Ensure that all keys are unique (and handle duplicates)
- Look up a value when given a key
- Delete a key/value entry

# Objectives
- Understand how dictionaries work under the hood
- Learn what `hashing` is and how to apply it
- Understand what a `hash map` is
- Apply principles of [object composition](https://realpython.com/inheritance-composition-python/) to a solution

# Instructions
We will use the principle of _object composition_ to create the `NoDict` class. This means that the primary `NoDict` class will be composed of a collection of smaller class objects called `Nodes`. Each Node object represents a single key/value pair. The keys and values of a dictionary should be kept together, otherwise the benefit of _associative mapping_ that dictionaries provide becomes lost. The job of the `NoDict` class is to manage the `Nodes` and provide interface methods that can be easily used by a programmer. The `Node` class itself is not meant to be used directly by a programmer, but it is a private working component of the `NoDict` class.

## Part A - Node class

- Define a class named `Node` that can be initialized with a key (mandatory) and a value (optional). Example:
   ```python
   n1 = Node("Kevin")  # Create a Node with a key, but no value
   n2 = Node("George", 21)  # Create Node with key and value
   ```
- The key and the value should be stored as instance variables within `Node`.
- Within the Node class, define and implement python "dunder" methods for `__init__`,  `__repr__`, and `__eq__`
- The Node class should print a human-readable representation of its key/value contents when asked. The `__repr__` method can do this. For example, this is not very readable
   ```python
   >>> print(Node("Kevin", 21))
   <__main__.Node object at 0x7f4b24f33580>
   ```
   The following, however, is more readable and shows the contents of the Node. It also adheres to the rules about what to return from a `__repr__` method vs. a `__str__` method. The `__repr__` method should return a string representation of a Python object that may be evaluated by the Python interpreter to [instantiate another instance](https://stackoverflow.com/questions/37779105/writing-a-repr-method) of the object.
   ```python
   >>> print(Node("Kevin", 21))
   Node("Kevin", 21)
   ```
   Implement the `__repr__` method like this:
   ```python
   return f'{self.__class__.__name__}({self.key}, {self.value})'
   ```
- The Node class should hash its own key, and keep that hash value as an instance attribute, `self.hash`. This hash value will be used by the NoDict class. Use the built-in Python `hash()` function for this.
- The Node class object should be able to compare itself to other Node objects using the Python built-in `==` operator.  For example
   ```python
   n1 = Node('Mike', 21)
   n2 = Node('Mike', 34)
   n3 = Node('Nick', 56)
   print(f'n1 == n2 ? {n1 == n2}')
   print(f'n2 == n3 ? {n2 == n3}')
   ```
   This should output
   ```console
   n1 == n2 ? True
   n2 == n3 ? False
   ```
   To do make this possible, implement the `__eq__` method within the Node class.
- Each method defined in the Node class should have a docstring.

# Part B - NoDict class
Create a class named `NoDict` which implements the key features of a dictionary.  Do not use the `dict` keyword, `{}` syntax, or other Python dictionary derivatives such as `OrderedDict` or `defaultdict` in your implementation.

Your `NoDict` class should initialize with an arbitrary default size of 10 internal 'buckets', but can be overridden for more or fewer buckets. The buckets should be implemented as a list of lists. Each bucket will contain 0 or more Node objects. Please review how to initialize a list containing `n` empty lists.

```python
[
   [], [], [], [] ... []  # n empty lists, contained in a list
]
```
The buckets are the important part of the `NoDict` class &mdash; they are where all the key/value Nodes will be stored. The `NoDict` class should implement the following class methods:

- `__init__` - class initializer to create the buckets according to a size parameter. Save the size parameter as an instance variable in the class. Create another instance variable to hold the bucket list. Your instance variable should be named `self.buckets`.

- `__repr__` - string representation of the contents of the buckets. The `__repr__` dunder method will be called any time you print the dictionary. It will give a detailed view of everything, to help you in debugging. You may notice that this `__repr__` method does not strictly adhere to the same rule that we used for the Node object, which is okay for this example problem because we want to see all the buckets.  Use the following code snippet for this method:
```python
      def __repr__(self):
         """Return a string representing the NoDict contents."""
         # We want to show all the buckets vertically
         return '\n'.join([f'{self.__class__.__name__}.{i}:{bucket}' for i, bucket in enumerate(self.buckets)])
```

- `add` - This class method should accept a new key and value, and store it into the `NoDict` instance. However, this method should not allow duplicate keys.  First, make a `Node` class using the key and value, e.g. `new_node = Node(key, value)`.

   To add the Node into a bucket, you must first determine which bucket to use. Get the previously hashed value of the Node from its `.hash` attribute which you computed, and modulo-divide (`%`)that large integer down to an index that can be used to reference any one of the buckets. That means you will modulo-divide the Node's hash value by the number of buckets in `NoDict`.

   Once you have a bucket index, you can reference the bucket itself (recall that each bucket is a list). Now that you have the bucket selected, you must iterate through its contents (which are all `Node` instances). As you examine each `Node` instance in the bucket, you should test for equality with the `Node` instance that you are trying to insert. If that `Node` does not match any existing `Node` in the bucket, append it to the bucket. If a match is found (the `Node` already exists in the bucket), then remove the previous matching `Node` before appending the new one. This way you have solved the 'No duplicates' requirement.

- `get` - This class method should perform a key-lookup in the `NoDict` class. It should accept just one parameter: The key to look up. If the key is found in the `NoDict` class, return its associated value. If the key is not found, raise a `KeyError` exception.

   This method will look similar to `add`. First, create a `Node` instance from the key, e.g., `node_to_find = Node(key)`. Then compute the bucket index the same way you did for the `add` function. Once you have the bucket, iterate through the bucket and look for a `Node` that matches `node_to_find`. If you find it, return that `Node`'s value.  If the iteration completes without finding a matching `Node`, raise a `KeyError` exception like this:
   ```python
   raise KeyError(f'{key} not found')
   ```

- `__setitem__` - Implement this magic "dunder" method within the `NoDict` class to enable square-bracket _assignment_ behavior. Think of it like a setter method.  After enabling this behavior, you will be able to do this:
   ```python
      my_dict = NoDict()
      my_dict['Kevin'] = 21
   ```

- `__getitem__` - Implement this magic "dunder" method within the `NoDict` class to enable square-bracket _reading_ behavior. This will make the class behave more like a regular dictionary. Without enabling this behavior, you could not write an expression like this:
   ```python
   kevin_age = my_dict['Kevin']
   ```
At this point, you have defined a very basic `NoDict` data structure that functions as an associative dictionary that can store and retrieve key/value pairs. You have used object composition by declaring a `Node` class to represent a hashed associative binding, and then used those `Node`s within the `NoDict` class. You have have also uncovered the secret of why dictionaries perform at close to ideal **O(1)** (constant time) lookup speed: Instead of iterating over a giant list of nodes, you are using the **hash** function to directly compute the bucket index of where to find a node.

## Part C - Testing
By now you should be familiar with how to run the tests that come with assignments.  Here are a couple of options for testing:
- Use the built-in VSCode "Test Tube" extension by searching the command pallette for `Python: Configure Tests`. Choose "unittest" as your framework, and "tests" as the folder containing the tests, and `test*.py` as the file pattern.  The test tube should appear in your Navigator bar.
- Use the command line : `python -m unittest tests/test_nodict.py`

Make sure all of the provided tests are passing before submitting your pull request.

# References
- [The Mighty Dictionary](https://www.youtube.com/watch?v=rWdF7oW6z18) - Brandon Craig Rhodes
- [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781449361747/ch04.html) -  Micha Gorelick, Ian Ozsvald

## PR (Pull Request) Workflow for this assignment
2. *Clone* your own repo to your local development machine.
3. Create a separate branch named `dev` and checkout the branch.
5. Commit your changes, then `git push` the branch back to your own GitHub account.
5. From your own GitHub repo, create a pull request (PR) *from your `dev` branch back to your master branch*.
6. Copy/Paste the URL **link to your PR** as your assignment submission.
7. Your grader will post code review comments inline within your pull request in your GitHub account. Be sure to respond to any comments and make requested changes. **RESUBMIT** a new link to your PR after making changes. This is the code review iteration cycle.
