# -*- encoding: utf-8 -*-

def list_ele(list1, op, scala1):
    list2 = {
        "+": lambda x, y: [e + y for e in x],
        "-": lambda x, y: [e - y for e in x],
        "*": lambda x, y: [e * y for e in x],
        "/": lambda x, y: [e / y for e in x],
    }[op](list1, scala1)

    return list2


def list_int_to_str(list1):
    return [str(e) for e in list1]


if __name__ == "__main__":
    l1 = [1, 2, 3, 4]
    l2 = list_ele(l1[:2], "*", 1*1./100)
    print(l2)

    l1 = ["a", "b", "c", "d"]
    l2 = list_ele(l1[:2], "+", "_heihei")
    print(l2)
