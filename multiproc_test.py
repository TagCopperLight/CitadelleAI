from time import sleep
import random
from tqdm import tqdm
from multiprocessing import Pool, current_process


def progresser(n: int):
    text = f'#{n}'
    sampling_counts = 10
    current = current_process()
    pos = current._identity[0]-1

    with tqdm(total=sampling_counts, desc=text, position=pos) as pbar:
        for _ in range(sampling_counts):
            sleep(random.uniform(0, 1))
            pbar.update(1)

if __name__ == '__main__':
    L = list(range(12)) # works until 23, breaks starting at 24
    with Pool(initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),)) as p: #type: ignore
        p.map(progresser, L)
        print('\n' * (len(L) + 1))
