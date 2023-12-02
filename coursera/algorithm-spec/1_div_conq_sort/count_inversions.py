def merge_sort(values):
    if len(values) == 1:
        return values, 0

    left = values[0:len(values)//2]
    right = values[len(values)//2:]
    left, c1 = merge_sort(left)
    right, c2 = merge_sort(right)
    sorted_values, c3 = count_split_inv(left, right)
    return sorted_values, c1 + c2 + c3

def count_split_inv(left, right):
    i = j = k = 0
    sorted_values = []
    inversions = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_values.append(left[i])
            i += 1
        else:
            sorted_values.append(right[j])
            j += 1
            inversions += 1
        k += 1

    while i < len(left):
        values[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        values[k] = right[j]
        j += 1
        k += 1
        inversions += 1

    return sorted_values, inversions


if __name__ == '__main__':
    with open('c:\\Users\\mtyuk\\Downloads\\merge_input.txt') as f:
        lines = f.read().splitlines()

    # values = [6, 5, 4, 3, 2, 1]
    values = []
    for line in lines:
        values.append(int(line))
    f.close()

    sorted_values, inversions = merge_sort(values)
    print(inversions)

