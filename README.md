This command will import classes into code:

```python
from src.classes import *
```

Classes includes all essential objects to work with three dimensions. This would be: Matrix, Vector, Point, VectorSpace, CoordinateSystem.

# Matrix

Initialization example:

```python
m = Matrix([[1, 2], [3, 4]])
```

Initialization can be provided, using list[list[float]] and Vector. 

Example of usage:
```python
from src.classes import *

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[4, 5], [1, 2]])

m3 = (m1+m2).transpose()
m3_transposed = m3.transpose()
m3_determinant = m3.determinant()

m4 = ((m1 * m2)/m3)*2

elem = m4[0][0]

m1[0][0] = elem

print(m1.inverse())
```

Fields:
* `data` - return elements of given matrix in list[list[int, float]] type.
* `rows` - return number of rows of given matrix.
* `columns` - return number of columns of given matrix.

Methods of Matrix are inherited in Vector. 

All methods are called like that:
`<class_name>.<method_name>(<parameters>)`

Explanation for methods description:
`<method_name>(<parameter>: <input_type>) -> <output_type>`

Methods:
* `zero_matrix(rows: int, columns: int) -> Matrix` - create a matrix, filled with zeros and size, according to input parameters.
* `identity_matrix(size: int) -> Matrix` - create an identity matrix (it should be quadratic, so there is only one parameter of size).
* `matrix.copy() -> Matrix` - create a copy of matrix, given before '.'.
* `transpose() -> Matrix` - create a transposed version of given matrix.
* `determinant() -> float` - find a determinant of given matrix.
* `inverse() -> Matrix` - create an inverted of given matrix.
* `gram() -> Matrix` - create a gram matrix, bases in given matrix.
* `rotate(axes_indecies: list[int], angle: float) -> Matrix` - create a rotated matrix by two given axes and angle.

Also this class supports usual arithmetic operations, that are allowed with matrices. So are they:
* `matrix1 + matrix2 -> Matrix`
* `matrix1 - matrix2 -> Matrix`
* `matrix1 * matrix2 -> Matrix` (matrices should be of correct size, like: nxm * mxr, where n, m, r are of real type)
* `matrix1 == matrix2 -> Boolean`
* `matrix * {float, int} == {float, int} * matrix -> Matrix`
* `matrix1 / matrix2 -> Matrix` (returns multiply of matrix1 and inverted matrix2)
* `matrix / {int, float} -> Matrix`

There are several functions, providing more comfort while working with that code. For example:
* `matrix[i][j]` - return an element, placed on row i and column j.
* `matrix[i][j] = {float, int}` - place an int or float element in row i and column j.
* `matrix[i] = Vector` - return a vector, which is row i.

# Vector

Initialization example:

```python
v = Vector([1, 2, 3]) # horizontal vector
v = Vector([[1], [2], [3]]) # vertical vector
```

Initialization can be provided, using list[list[float]] and Matrix. 

Example of usage:
```python
from src.classes import *

v1 = Vector([1, 2, 3])
v2 = Matrix([1, 2, 4])

v3 = (v1+v2).transpose()
v3_transposed = v3.transpose()

scalar = (v1&v3)*2

elem = v4[0][0]

v1[0][0] = elem

print(v1**v2)
```

Fields:
* `values` - return elements of given vector in list[int, float] or list[list[int, float]] type (depends on horizontal or vertical the vector is).
* `size` - return a size of given vector.
* `is_transposed` - return a boolean value (if given vector is horizontal, the field would be False, if vertical - True).

Methods of Vector are inherited from Matrix. 

All methods are called like that:
`<class_name>.<method_name>(<parameters>)`

Explanation for methods description:
`<method_name>(<parameter>: <input_type>) -> <output_type>`

Methods:
* `as_matrix() -> Matrix` - return a matrix version of given vector.
* `transpose() -> Vector` - create a transposed version of given vector.
* `rotate(axes_indecies: list[int], angle: float) -> Vector` - create a rotated vector by two given axes and angle (n-dimensional rotation).
* `len() -> {int, float}` - return length of a vector.
* `norm()` - normalize vector.

Also this class supports usual arithmetic operations, that are allowed with matrices. So are they:
* `vector1 + vector2 -> Vector`
* `vector1 - vector2 -> Vector`
* `vector1 * vector2 -> Vector` (vector should be of correct size, like: 1xm * mx1, where m if of real type)
* `vector1 ** vector2 -> Vector` (vector product of given vectors in arbitrary VectorSpace)
* `vector1 & vector2 -> {int, float}` (scalar product of two given vectors in arbitrary VectorSpace)
* `vector1 == vector2 -> Boolean`
* `vector * {float, int} == {float, int} * vector -> Vector`
* `vector / {int, float} -> Vector`

There are several functions, providing more comfort while working with that code. For example:
* `vector[i]` - return an element, placed on position i.
* `vector[i] = {float, int}` - place an int or float element in position i.

# Point

Initialization example:

```python
p = Point([1, 2, 3])
```

Fields:
* `size` - return a size of given point.

There are only three operations allowed within this class, due to geometric logic.
* `point1 == point2 -> Boolean`
* `point + vector == vector + point -> Point`
* `point - vector -> Point`

# VectorSpace

Initialization example:

```python
vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
```

Initialization can be provided, using only list[Vector].

Fields:
* `basis` - return a Matrix of basis vectors.
* `size` - return a size of basis (number of vectors in basis).

Methods:
* `as_vector(point: Point) -> Vector` - return a radius-vector of a given point in arbitrary VectorSpace.

# CoordinateSystem

Fields:
* `initial_point` - return a point of Point type, that if fundamental in coordinate system.
* `vs` - return a VectorSpace type object.

Initialization example:

```python
p = Point([1, 2, 3])
vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
coordinate_system = CoordinateSystem(p, vs)
```
