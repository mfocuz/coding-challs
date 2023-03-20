def solution_day4():
    input_file = open('inputs/day4/input.txt', 'r')

    lines = input_file.readlines()
    result = 0
    for line in lines:
        pairs = line.rstrip().split(',')
        p1 = pairs[0]
        p2 = pairs[1]

        if check_inside(p1, p2):
            result += 1

    print("Answer=%d" % result)




def check_inside(p1, p2):
    p1_l = int(p1.split('-')[0])
    p1_h = int(p1.split('-')[1])

    p2_l = int(p2.split('-')[0])
    p2_h = int(p2.split('-')[1])

    if (p1_l <= p2_l <= p1_h) or (p1_l <= p2_h <= p1_h)  or (p2_l <= p1_h <= p2_h) or (p2_l <= p1_h <= p2_h):
        return True
    else:
        return False




if __name__ == '__main__':
    solution_day4()