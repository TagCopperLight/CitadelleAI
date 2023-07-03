import subprocess
import threading
from typing import IO

class ReaderThread(threading.Thread):
    def __init__(self, stream: IO[bytes]):
        threading.Thread.__init__(self)
        self.stream = stream

    def run(self):
        while True:
            line = self.stream.readline()
            if len(line) == 0:
                break
            print(str(line, 'utf-8'))

process = subprocess.Popen(["./c_simulation/output/bin.out"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
if process.stdin is None or process.stdout is None:
    raise Exception("stdin is None")
process.stdin.write(b'3\n')
process.stdin.flush()

reader = ReaderThread(process.stdout)
reader.start()

process.wait()

reader.join()

print("Done!")