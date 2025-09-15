## Set Interface (HashSet, TreeSet) - Study Notes

**1. Introduction**

The `Set` interface in Java, part of the Collections Framework, represents an unordered collection of unique elements.  Unlike `List`, which allows duplicate elements and maintains insertion order, a `Set` guarantees that each element is distinct.  This uniqueness constraint is the defining characteristic of a `Set`.  The primary implementations of the `Set` interface are `HashSet` and `TreeSet`, each offering different performance characteristics and functionalities based on their underlying data structures.  Understanding the nuances of these implementations is crucial for effective Java programming.

**2. Core Concepts**

* **Uniqueness:** The core principle of a `Set` is that it contains only one instance of each element.  Attempts to add duplicate elements are ignored.  The equality of elements is determined by the `equals()` method.  If two objects are considered equal by `equals()`, only one will be present in the Set.  It's crucial to override `equals()` and `hashCode()` consistently for custom classes used within `Set`s to ensure proper functionality.

* **Unordered (HashSet):**  `HashSet`s, backed by a hash table, do not maintain any specific order of elements.  Iteration order is not guaranteed and may vary between runs.  This allows for fast `add`, `remove`, and `contains` operations (average O(1) time complexity).

* **Ordered (TreeSet):** `TreeSet`s, backed by a red-black tree, maintain elements in a sorted order (natural ordering or based on a provided `Comparator`). This comes at the cost of slightly slower operations compared to `HashSet` (average O(log n) time complexity).  The sorted order allows for efficient retrieval of elements within a specific range.

* **Iteration:** Both `HashSet` and `TreeSet` implement the `Iterable` interface, allowing easy iteration over their elements using enhanced for loops or iterators.  The iteration order for `HashSet` is unpredictable, while for `TreeSet`, it's sorted according to the specified ordering.

* **Null Elements:** Both `HashSet` and `TreeSet` can hold at most one null element.


**3. Practical Examples**

**Example 1: HashSet**

```java
import java.util.HashSet;
import java.util.Set;

public class HashSetExample {
    public static void main(String[] args) {
        Set<String> mySet = new HashSet<>();
        mySet.add("apple");
        mySet.add("banana");
        mySet.add("apple"); // Duplicate - ignored
        mySet.add("orange");

        System.out.println(mySet); // Output: [banana, apple, orange] (order not guaranteed)
        System.out.println(mySet.contains("banana")); // Output: true
        System.out.println(mySet.size()); // Output: 3
    }
}
```

**Example 2: TreeSet**

```java
import java.util.TreeSet;
import java.util.Set;
import java.util.Comparator;

public class TreeSetExample {
    public static void main(String[] args) {
        // Natural ordering (based on String's compareTo method)
        Set<String> myTreeSet = new TreeSet<>();
        myTreeSet.add("apple");
        myTreeSet.add("banana");
        myTreeSet.add("orange");

        System.out.println(myTreeSet); // Output: [apple, banana, orange] (sorted)


        // Custom ordering using Comparator
        Comparator<String> reverseComparator = (s1, s2) -> s2.compareTo(s1);
        Set<String> myTreeSetReverse = new TreeSet<>(reverseComparator);
        myTreeSetReverse.add("apple");
        myTreeSetReverse.add("banana");
        myTreeSetReverse.add("orange");
        System.out.println(myTreeSetReverse); //Output: [orange, banana, apple] (reverse sorted)
    }
}
```

**Example 3:  Custom Class in a Set**

```java
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

class Person {
    String name;
    int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    @Override
    public String toString(){
        return name + " (" + age + ")";
    }
}

public class CustomClassInSet {
    public static void main(String[] args) {
        Set<Person> people = new HashSet<>();
        people.add(new Person("Alice", 30));
        people.add(new Person("Bob", 25));
        people.add(new Person("Alice", 30)); // Duplicate - ignored due to equals/hashCode

        System.out.println(people); // Output will show only unique Person objects.
    }
}
```

**4. Conclusion**

The choice between `HashSet` and `TreeSet` depends on the specific application requirements. If order doesn't matter and fast lookups are prioritized, `HashSet` is the better choice. If maintaining a sorted order is essential or range-based queries are frequent, `TreeSet` is preferred.  Remember that correctly implementing `equals()` and `hashCode()` is crucial when using custom classes with `Set` implementations to ensure uniqueness and proper functionality.  Understanding these fundamental concepts enables efficient and robust use of the `Set` interface in Java.