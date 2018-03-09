import multiprocessing
import threading
from multiprocessing import Process
import math
import numpy as np

import matplotlib.pyplot as plt
import time


def prefix_sum(elements):
    res = [0] * (len(elements) + 1)
    for i in range(0, len(elements)):
        res[i+1] = res[i] + elements[i]

    return res


def _get_number_of_processes(arr_len, cores, step_size):
    max_processes = int(arr_len / step_size)
    return max_processes if max_processes <= cores else cores


def up_sum(arr, start_index, end_index, step_size, l):
    i = start_index
    while i < end_index:
        arr[i + step_size - 1] = arr[i + 2**l - 1] + arr[i + step_size - 1]
        i += step_size


def up_phase(arr, cores, with_threads_instead_of_processes):
    for l in range(0, int(math.log(len(arr), 2))):
        step_size = 2 ** (l + 1)
        number_of_processes = _get_number_of_processes(len(arr), cores, step_size)
        partition_size = int(len(arr) / number_of_processes)
        processes = []
        for i in range(0, number_of_processes):
            process = threading.Thread(target=up_sum, args=(arr, i * partition_size, (i+1) * partition_size - 1, step_size, l)) if with_threads_instead_of_processes \
                else Process(target=up_sum, args=(arr, i * partition_size, (i+1) * partition_size - 1, step_size, l))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


def down_swap(arr, start_index, end_index, step_size, l):
    i = start_index
    while i < end_index:
        buf = arr[i + step_size - 1]
        arr[i + step_size - 1] = arr[i + 2**l - 1] + arr[i + step_size - 1]
        arr[i + 2 ** l - 1] = buf
        i += step_size


def down_phase(arr, cores, with_threads_instead_of_processes):
    for l in reversed(range(0,int(math.log(len(arr), 2)))):
        step_size = 2 ** (l + 1)
        number_of_processes = _get_number_of_processes(len(arr), cores, step_size)
        partition_size = int(len(arr) / number_of_processes)
        processes = []
        for i in range(0, number_of_processes):
            process = threading.Thread(target=down_swap, args=(arr, i * partition_size, (i+1) * partition_size - 1, step_size, l)) if with_threads_instead_of_processes \
                else Process(target=down_swap, args=(arr, i * partition_size, (i+1) * partition_size - 1, step_size, l))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


def parallel_prefix_sum(elements, cores, with_threads_instead_of_processes):
    thread_safe_arr = multiprocessing.Array('i', elements)

    up_phase(thread_safe_arr, cores, with_threads_instead_of_processes)

    elements_sum = thread_safe_arr[-1]
    thread_safe_arr[-1] = 0

    down_phase(thread_safe_arr, cores, with_threads_instead_of_processes)

    res = list(thread_safe_arr)
    res.append(elements_sum)
    return res


def run_simulation(n_from, n_to, cores, with_threads_instead_of_processes = True):
    inputs = [list(np.random.randint(20, size=2**n)) for n in range(n_from, n_to)]
    elapsed_seq = []
    elapsed_par = []

    for input in inputs:
        t0_seq = time.time()
        p_seq = prefix_sum(input)
        elapsed_seq.append(time.time() - t0_seq)

        t0_par = time.time()
        p_par = parallel_prefix_sum(input, cores, with_threads_instead_of_processes)
        elapsed_par.append(time.time() - t0_par)

        if p_seq != p_par:
            print(p_seq)
            print(p_par)
            print()

    return elapsed_seq, elapsed_par


if __name__ == '__main__':
    lower = 15
    upper = 20
    s, p = run_simulation(lower, upper, 4)

    plt.plot(s, range(lower,upper), 'r', p,  range(lower,upper), 'b')
    plt.show()

    print(s)
    print(p)


