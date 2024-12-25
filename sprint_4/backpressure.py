import queue
import threading
import time
import random

class Producer(threading.Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        while True:
            item = random.randint(1, 100)
            print(f"Producing {item}")
            #ждем буфер
            while self.buffer.full():
                print("Buffer full, waiting...")
                time.sleep(1)
            
            self.buffer.put(item)
            time.sleep(random.random())  # Спим случайное время

class Consumer(threading.Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        while True:
            # Ждём, если буфер пустой
            while self.buffer.empty():
                print("Buffer empty, waiting for items...")
                time.sleep(1)
            
            item = self.buffer.get()
            print(f"Consuming {item}")
            time.sleep(1 + random.random())  # спим для эмуляции backpressure

if __name__ == "__main__":
    buffer = queue.Queue(maxsize=5) 

    producer = Producer(buffer)
    consumer = Consumer(buffer)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()