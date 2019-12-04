from collections import Counter


def does_meet_password_criteria(num: str) -> bool:
    if len(num) != 6:
        return False
    for d1, d2 in zip(num[:], num[1:]):
        if d1 == d2:
            break
    else:
        return False
    for d1, d2 in zip(num[:], num[1:]):
        if d1 > d2:
            return False
    return True


def does_meet_password_criteria2(num: str) -> bool:
    if not does_meet_password_criteria(num):
        return False
    counter = Counter(num)
    val_len = set([val for val in counter.values() if val >= 2])
    return 2 in val_len


def sol1() -> int:
    min_num = 402328
    max_num = 864247
    counter = 0
    for num in range(min_num, max_num):
        if does_meet_password_criteria(str(num)):
            counter += 1
    return counter


def sol2() -> int:
    min_num = 402328
    max_num = 864247
    counter = 0
    for num in range(min_num, max_num):
        if does_meet_password_criteria2(str(num)):
            counter += 1
    return counter


def main() -> int:
    print(sol1())
    print(sol2())
    return 0


if __name__ == '__main__':
    exit(main())
