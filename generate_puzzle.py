import sys
import random


def create_puzzle(size):
    available_numbers = []
    for n in range(1, (size * size) + 1):
        available_numbers.append(n)

    lst = []
    for s in range(0, size):
        tmp_list = []

        # create row
        for s2 in range(0, size):
            if len(available_numbers) == 1:
                tmp_list.append(available_numbers.pop())
            else:
                tmp_list.append(available_numbers.pop(random.randrange(0, len(available_numbers))))

        # append row
        lst.append(tuple(tmp_list))
    return tuple(lst)


if __name__ == '__main__':
    print("Creating {} new puzzles of size {} at: {}".format(sys.argv[2], sys.argv[3], sys.argv[1]))

    f = open(sys.argv[1], "w")

    for i in range(0, int(sys.argv[2])):
        f.write("{}\n".format(create_puzzle(int(sys.argv[3]))).replace(",", ";"))

    f.close()
