#!/usr/bin/env python3

class Buffer():
    def __init__(self, size):
        self._size = size
        self._buffer = [None] * size * 2
        self._start = 0
        self._count = 0

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._start + len(self._buffer)

    def __str__(self):
        return "{} - {}:{}:{}".format(self.start, len(self._buffer), self._buffer, self.end)

    def _send(self):
        data = self._buffer.pop(0)
        if (data is not None):
            print("emit data at index {}: {}".format(self.start, data))
            self._count -= 1
        self._start += 1

        self._buffer.append(None)

    def receive(self, index, data):
        if self._count == 0:
            if index < self._size:
                self._start = index
            else:
                self._start = index - self._size

        if index < self.start:
            print("index too low: {}".format(index))
            return

        if index > self.end:
            print("index too high: {}".format(index))
        else:
            if self._buffer[index - self.start] is not None:
                print("overwriting index {}".format(index))

            self._buffer[index - self.start] = data
            self._count += 1

        if index - self.start >= self._size:
            self._send()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Correct reordering of integers.')
    parser.add_argument('--size', default=10, type=int,
                    help='buffer size (default: 10)')
    parser.add_argument('filename',
                    help='input file with reordered integers')

    args = parser.parse_args()

    buffer = Buffer(args.size)

    with open(args.filename, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            if line != '':
                index = int(line)
                buffer.receive(index, "{}".format(index))

    print(buffer)

if __name__ == "__main__":
    exit(main())
