class Stack:

    # 初始化
    def __init__(self):
        self.__list = []

    # 入栈
    def push(self, item):
        self.__list.append(item)

    # 出栈
    def pop(self):
        if self.__list:
            return self.__list.pop()
        else:
            return None

    # 栈顶
    def peek(self):
        if self.__list:
            return self.__list[-1]
        else:
            return None

    # 判断空
    def is_empty(self):
        return self.__list == []

    # 获取大小
    def size(self):
        return len(self.__list)

    # 仅保留栈底第一个元素
    def reset(self):
        while not self.size() == 1:
            self.pop()

    # 展示栈
    def show(self):
        size = self.size()
        for i in range(size):
            print(self.__list[i])

    # 获取栈底
    def get_base(self):
        return self.__list[0]

    # 清空栈
    def empty(self):
        while not self.is_empty():
            self.pop()
