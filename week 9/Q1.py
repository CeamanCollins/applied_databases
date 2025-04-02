import numpy

def double(n):
    return n * 2

def main():
    array_1 = []
    array_2 =[]

    for i in range(10):
        array_1.append(numpy.random.randint(1, 100))

    for i in array_1:
        array_2.append(double(i))

    print(array_2)

if __name__ == "__main__":
    main()