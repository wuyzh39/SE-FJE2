import sys
import re
from abc import ABC, abstractmethod
import json

class Element(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

#具体的元素类，我将树形json的每个节点都当作一个元素
class TreeNode(Element):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_treeNode(self)

class TreeStyleIterator:
    def __init__(self,node_stack):
        self.elements=node_stack
        self.index=0

    def has_next(self):
        return self.index < len(self.elements)
    
    def next(self):
        if self.has_next():
            element = self.elements[self.index]
            self.index += 1
            return element


class Visitor(ABC):
    @abstractmethod
    def visit_treeNode(self, element):
        pass

class PrintVisitor(Visitor):
    def visit_treeNode(self, element):
        print(element.value)

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")

def convert_tree(data, level=0):
        if isinstance(data, dict):
            for key, value in data.items():
                # 检查是否是最后一个键
                last_key = key == list(data.keys())[-1]
                connector = "└─" if last_key else "├─"
                # print(f"{'│   ' * level}{connector} {key}")
                stack.append(TreeNode(f"{'│   ' * level}{connector} {key}"))
                convert_tree(value, level + 1)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                # 检查是否是列表中的最后一个元素
                last_item = i == len(data) - 1
                connector = "   " if last_item else "├──"
                # print(f"{'│   ' * level}{connector} {item}")
                stack.append(TreeNode(f"{'│   ' * level}{connector} {item}"))
                convert_tree(item, level + 1)

stack=[]

if __name__ == "__main__":
    file_path = input().rstrip()
    data = read_json_file(file_path)

    convert_tree(data)

    iterator = TreeStyleIterator(stack)

    visitor = PrintVisitor()
    while iterator.has_next():
        element = iterator.next()
        element.accept(visitor)


