import itertools as it
import random

EQUALITY_PRECISION_SQ = 1e-10

# TODO: -------------, private args, logging
# progress:
#  [+] documentation
#  [ ] private args
#  [ ] logging



class Point:
    """class for vector operations etc."""

    def __init__(self, *args):
        # print('point init', args)
        super().__init__()
        if len(args) == 3:
            self.x, self.y, self.z = args
        elif len(args) == 1:
            self.x, self.y, self.z = args[0]
        else:
            raise ValueError('bad arguments count for point')

    def __add__(self, other):
        """self + other

        :param other: Point
        """
        if isinstance(other, Point):
            result = Point(self.x + other.x, self.y + other.y, self.z + other.z)
            return result
        else:
            raise ValueError("can't add {} to point".format(other.__class__.__name__))

    def __sub__(self, other):
        """self - other

        :param other: Point
        """
        if isinstance(other, Point):
            result = Point(self.x - other.x, self.y - other.y, self.z - other.z)
            return result
        else:
            raise ValueError("can't add {} to point".format(other.__class__.__name__))

    def __mul__(self, other):
        """self * other

        :param other: Point, number
        """
        if isinstance(other, Point):
            result = Point(self.x * other.x, self.y * other.y, self.z * other.z)
            return result
        elif isinstance(other, (int, float)):
            result = Point(self.x * other, self.y * other, self.z * other)
            return result
        else:
            raise ValueError("can't multiply {} with point".format(other.__class__.__name__))

    def __str__(self):
        """f'P({self.x}, {self.y})'"""
        return f'P({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        """f'P({self.x}, {self.y})'"""
        return f'P({self.x}, {self.y}, {self.z})'

    def __truediv__(self, other):
        """self / other

        :param other: Point, number
        """
        if isinstance(other, Point):
            result = Point(self.x / other.x, self.y / other.y, self.z / other.z)
            return result
        elif isinstance(other, (int, float)):
            result = Point(self.x / other, self.y / other, self.z / other)
            return result
        else:
            raise ValueError("can't div {} with point".format(other.__class__.__name__))

    def __rtruediv__(self, other):
        """other / self

        :param other: Point, number
        """
        if isinstance(other, Point):
            result = Point(other.x / self.x, other.y / self.y, other.z / self.z)
            return result
        elif isinstance(other, (int, float)):
            result = Point(other / self.x, other / self.y, other / self.z)
            return result
        else:
            raise ValueError("can't div {} with point".format(other.__class__.__name__))

    def __setattr__(self, key, value):
        """if key one of "x", "y", checks type of value"""
        if key == 'x':
            assert isinstance(value, (float, int)), 'bad x coord type, should be int or float'
        if key == 'y':
            assert isinstance(value, (float, int)), 'bad y coord type, shoulf be int of float'
        if key == 'z':
            assert isinstance(value, (float, int)), 'bad y coord type, shoulf be int of float'
        object.__setattr__(self, key, value)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def distance_sq(self, other):
        """distance^2 between self and other

        :param other: Point
        """
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2  + (self.z - other.z) ** 2

    def distance(self, other):
        """distance between self and other

        :param other: Point
        """

        return self.distance_sq(other) ** .5

    def abs(self):
        """absolute value of point"""
        return self.distance(Point(0,0,0))

    def vector_mul(self, other):
        """vector multiplication [self x other]

        :param other: Point
        """

        v1, v2 = self, other
        return Point(
            + v1.y*v2.z - v2.y*v1.z,
            - v1.x*v2.z + v2.x*v1.z,
            + v1.x*v2.y - v2.x*v1.y,
        )

    def scalar_mul(self, other):
        """scalar multiplication (self, other)

        :param other: Point
        """
        return self.x *other.x + self.y *other.y + self.z *other.z

    def set_inplace(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z
    
    @classmethod
    def checkis(cls, x):
        """assert isinstance(x, Point); deprecated method"""
        assert isinstance(x, cls), "This is not point!!! It's {}".format(x.__class__.__name__)

    if EQUALITY_PRECISION_SQ == 0:
        def __eq__(self, other):
            """self == other

            :param other: Point
            """
            if not isinstance(other, Point):
                return False
            return self.x == other.x and self.y == other.y and self.z == other.z 
    else:
        def __eq__(self, other):
            """self == other

            :param other: Point
            """
            if not isinstance(other, Point):
                return False
            return self.distance_sq(other) < EQUALITY_PRECISION_SQ

    def tolist(self):
        """list(self)"""
        return [self.x, self.y, self.z]

    def copy(self):

        return Point(self.x, self.y, self.z)
