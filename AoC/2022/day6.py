def solution_day6():
    input_file = open('inputs/day6/input.txt', 'r')
    elfs = []

    lines = input_file.readlines()
    for line in lines:
        counter = 0
        buff = []
        for i in line:
            if len(buff) >= 14:
                if len(set(buff)) == 14:
                    print("Done! counter=%d" % counter)
                    break

                buff.pop(0)
                buff.append(i)
            else:
                buff.append(i)
            counter += 1

if __name__ == '__main__':
    solution_day6()