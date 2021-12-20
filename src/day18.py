import math

class Pair(object):
    left_pair = None
    left_value = None
    right_pair = None
    right_value = None
    parent = None

    def __init__(self, left_pair = None, left_value = None, right_pair = None, right_value = None):
        # Right side: either link to pair or value
        assert right_value is None or right_pair is None
        self.right_pair = right_pair
        self.right_value = right_value

        # Left side: either link to p
        assert left_value is None or left_pair is None
        self.left_pair = left_pair
        self.left_value = left_value

        if self.left_pair:
            self.left_pair.parent = self 

        if self.right_pair:
            self.right_pair.parent = self

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Pair):
            return self.left_pair == other.left_pair and self.left_value == other.left_value and self.right_pair == other.right_pair and self.right_value == other.right_value
        return False

    def magnitude(self):
        left = self.left_value if self.left_value is not None else self.left_pair.magnitude()
        right = self.right_value if self.right_value is not None else self.right_pair.magnitude()
        return 3*left + 2*right
    
    def add_right(self, value):
        if self.right_pair is None:
            self.right_value += value
        elif self.left_pair is None:
            self.left_value += value
        else:
            self.right_pair.add_right(value)
    
    def add_left(self, value):
        if self.left_pair is None:
            self.left_value += value
        elif self.right_pair is None:
            self.right_value += value
        else:
            self.left_pair.add_left(value)

    def to_list(self):
        left = self.left_value if self.left_value is not None else self.left_pair.to_list()
        right = self.right_value if self.right_value is not None else self.right_pair.to_list()
        return [left,  right]



def parse_number(input):
    import json
    number_array = json.loads(input)
    return pair_from_array(number_array)

def pair_from_array(array): 
    assert len(array) == 2
    left = array[0]
    right = array[1]
    left_value = left if type(left) == int else None
    left_pair = pair_from_array(left) if isinstance(left, list) else None
    right_value = right if type(right) == int else None
    right_pair = pair_from_array(right) if isinstance(right, list) else None
    return Pair(left_pair, left_value, right_pair, right_value)

def add(p1, p2):
    assert isinstance(p1, Pair) and isinstance(p2, Pair)
    return Pair(left_pair=p1, right_pair=p2)

def reduce(num):
    while explode(num, 0) or split(num):
        # print(num.to_list())
        continue
 
    return num

def split(num):
    if num is None:
        return
    if num.left_value is not None and num.left_value > 9:
        num.left_pair = Pair(left_value=math.floor(num.left_value / 2.0), right_value=math.ceil(num.left_value / 2.0))
        num.left_pair.parent = num
        num.left_value = None
        return num
    
    if num.right_value is not None and num.right_value > 9:
        num.right_pair = Pair(left_value=math.floor(num.right_value / 2.0), right_value=math.ceil(num.right_value / 2.0))
        num.right_pair.parent = num
        num.right_value = None
        return num
    
    return split(num.right_pair) or split(num.left_pair)

def explode(num, level=0):
    # find leftmost with depth == 4
    assert level <= 4
    if level == 4:
        assert num.left_pair is None and num.right_pair is None
        return num
    
    if num.left_pair is not None:
        exploding_pair = explode(num.left_pair, level+1)
        if exploding_pair and exploding_pair.parent:
            add_to_left(exploding_pair.left_value, exploding_pair)
            add_to_right(exploding_pair.right_value, exploding_pair)
            exploding_pair.parent = None
            num.left_pair = None
            num.left_value = 0
        if exploding_pair:
            return exploding_pair

    if num.right_pair is not None:
        exploding_pair = explode(num.right_pair, level+1)
        if exploding_pair and exploding_pair.parent:
            add_to_left(exploding_pair.left_value, exploding_pair)
            add_to_right(exploding_pair.right_value, exploding_pair)
            exploding_pair.parent = None
            num.right_pair = None
            num.right_value = 0
        if exploding_pair:
            return exploding_pair
    
    return None

def add_to_left(value, current_pair): 
    while True:
        if current_pair.parent is None:
            return
        elif current_pair.parent.left_pair == current_pair:
            current_pair = current_pair.parent
        else:
            break
    # move one more up
    current_pair = current_pair.parent
    if current_pair.left_pair is None:
        current_pair.left_value += value
    else:
        current_pair.left_pair.add_left(value)

def add_to_right(value, current_pair): 
    while True:
        if current_pair.parent is None:
            return
        elif current_pair.parent.right_pair == current_pair:
            current_pair = current_pair.parent
        else:
            break
    # move one more up
    current_pair = current_pair.parent
    if current_pair.right_pair is None:
        current_pair.right_value += value
    else:
        current_pair.right_pair.add_left(value)

def sum_from_file_input(path): 
    file = open(path, 'r')
    Lines = file.readlines()
 
    sum = None
    for line in Lines:
        num = parse_number(line)
        if sum is not None:
            sum = add(sum, num)
            sum = reduce(sum)
        else:
            sum = num
    
    return sum


# Tests 

def test_magnitude_examples(): 
    number = parse_number("[[1,2],[[3,4],5]]")
    magnitude = number.magnitude()
    assert magnitude == 143

    number = parse_number("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    magnitude = number.magnitude()
    assert magnitude == 1384

    number = parse_number("[[[[1,1],[2,2]],[3,3]],[4,4]]")
    magnitude = number.magnitude()
    assert magnitude == 445

    number = parse_number("[[[[3,0],[5,3]],[4,4]],[5,5]]")
    magnitude = number.magnitude()
    assert magnitude == 791

    number = parse_number("[[[[5,0],[7,4]],[5,5]],[6,6]]")
    magnitude = number.magnitude()
    assert magnitude == 1137

    number = parse_number("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
    magnitude = number.magnitude()
    assert magnitude == 3488

def test_parse_input():
    # [[1,2],[[3,4],5]]
    number = parse_number("[[1,2],[[3,4],5]]")
    assert number.right_pair.left_pair.right_value == 4

def test_add():
    p1 = parse_number("[1,2]")
    p2 = parse_number("[[3,4],5]")
    sum = add(p1, p2)
    assert sum == parse_number("[[1,2],[[3,4],5]]")

def test_explode():
    num = parse_number("[[[[[9,8],1],2],3],4]")
    num = reduce(num)
    assert num == parse_number("[[[[0,9],2],3],4]")

    num = parse_number("[7,[6,[5,[4,[3,2]]]]]")
    num = reduce(num)
    assert num == parse_number("[7,[6,[5,[7,0]]]]")
    
    num = parse_number("[[6,[5,[4,[3,2]]]],1]")
    num = reduce(num)
    assert num == parse_number("[[6,[5,[7,0]]],3]")

    num = parse_number("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    num = reduce(num)
    assert num == parse_number("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

def test_split():
    num = parse_number("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    num = reduce(num)
    # print(num.to_list())
    assert num == parse_number("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

def test_example():
    num1 = parse_number("[[[[4,3],4],4],[7,[[8,4],9]]]")
    num2 = parse_number("[1,1]")
    sum = add(num1, num2)
    sum = reduce(sum)
    assert sum == parse_number("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


def test_example_sum1():
    sum = sum_from_file_input("src/day18_example1.txt")  
    print(sum.to_list())
    assert sum == parse_number("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")
    
def test_example_sum():
    sum = sum_from_file_input("src/day18_example.txt")  
    print(sum.to_list())
    assert sum == parse_number("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")

def test_simple_1():
    sum = sum_from_file_input("src/day18_simple_1.txt")  
    print(sum.to_list())
    assert sum == parse_number("[[[[5,0],[7,4]],[5,5]],[6,6]]")


# Run tests
# test_parse_input()
# test_magnitude_examples()
# test_add()
# test_explode()
# test_split()
# test_example()
test_example_sum1()
# test_example_sum()
test_simple_1()


