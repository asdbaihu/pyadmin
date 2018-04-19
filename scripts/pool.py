from multiprocessing import Pool
import time

def take_nap(x):
    time.sleep(x)
    print(f"ahh...refreshing.It's {time.time()}!")

p = Pool(5)

p.map(take_nap,[1,2,3,4,5])

