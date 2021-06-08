def fibonacci(n):
    seq = [0,1]
    if n < 0:
        return "Некорректный элемент последовательности"
    if n < 2:
        return seq[n]
    else:
        while len(seq) < n + 1:
            last_ind = len(seq) - 1
            seq.append(seq[last_ind] + seq[last_ind - 1])
        return seq[n]


print(fibonacci(0))
print(fibonacci(7))
print(fibonacci(-1))


# second solution
def fib(n):
    seq = [0, 1]
    if n < 0:
        return "Некорректный элемент последовательности"
    if n < 2:
        return seq[n]
    else:
        last_el, before_last_el = seq[1], seq[0]
        for iter in range(n - 1):
            last_el, before_last_el = last_el + before_last_el, last_el
        return last_el


print(fib(0))
print(fib(7))
print(fib(-1))