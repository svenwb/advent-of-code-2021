

def read_algorithm(path):
    file = open(path, 'r')
    Lines = file.readlines()

    # read first 512 chars to parse the algorithm
    algorithm = []
    for line in Lines:
        if len(line) == 1:
            break

        for c in line:
            if c == '.':
                algorithm.append(0)
            elif c == '#':
                algorithm.append(1)
    
    assert len(algorithm) == 512

    return algorithm

def read_input(path, padding):
    file = open(path, 'r')
    Lines = file.readlines()

    # read input
    # skip algorithm
    is_algorithm_part = True
    input = []
    for line in Lines:
        if len(line) == 1:
            is_algorithm_part = False
            continue
        if is_algorithm_part:
            continue

        row = [0 for i in range(padding)]
        for c in line:
            if c == '.':
                row.append(0)
            elif c == '#':
                row.append(1)
        row = row + [0 for i in range(padding)]
        input.append(row)

    for i in range(padding):
        input.append([0 for i in range(len(input[0]))])
    for i in range(padding):
        input.insert(0, [0 for i in range(len(input[0]))])


    return input


def apply_algrithm(algorithm, input):
    output = []
    for i in range(len(input)-3):
        output_row = []
        for j in range(len(input[0])-3):
            pixel = input[i][j:j+3] + input[i+1][j:j+3] + input[i+2][j:j+3] 
            lookup = int("".join(str(x) for x in pixel), 2)
            output_row.append(algorithm[lookup])
        output.append(output_row)
    
    return output

def count_lit(image):
    result = 0;
    for row in image:
        result += sum(row)
    return result

def full_run(path, runs):
    algo = read_algorithm(path)
    input = read_input(path, runs * 5)
    output = input
    for i in range(runs):
        output = apply_algrithm(algo, output)
    count = count_lit(output)
    return count

print(full_run('input/day20_1.txt', 2))
print(full_run('input/day20_input.txt', 2))

print(full_run('input/day20_1.txt', 50))
print(full_run('input/day20_input.txt', 50))