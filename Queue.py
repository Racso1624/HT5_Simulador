class Queue:

    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola esta vacia")

    def size(self):
        return self.items.__sizeof__

    def isEmpty(self):
        return self.items == []

        