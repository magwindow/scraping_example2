from multiprocessing import Process
import time

def print_time(thread_name, delay, iterations):
    start = int(time.time())
    for i in range(0, iterations):
        time.sleep(delay)
        seconds_elapsed = str(int(time.time()) - start)
        print(thread_name if thread_name else seconds_elapsed)

processes = [
    Process(target=print_time, args=('Counter', 1, 100)),
    Process(target=print_time, args=('Fizz', 3, 33)),
    Process(target=print_time, args=('Buzz', 5, 20)) 
]

if __name__ == '__main__':
    [p.start() for p in processes]
    [p.join() for p in processes]