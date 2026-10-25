
from flask import Flask, render_template, request
from stack import Stack
from collections import deque
import math
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-for-your-own-project"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/works")
def works():
    return render_template("works.html")

@app.route("/works/uppercase", methods=["GET", "POST"])
def uppercase():
    result = None

    if request.method == "POST":
        text = request.form.get("inputString", "")
        result = text.upper()

    return render_template("touppercase.html", result=result)

@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result = None
    error = None

    if request.method == "POST":
        try:
            radius = float(request.form.get("radius", ""))

            if radius <= 0:
                error = "Please enter a positive radius."
            else:
                result = math.pi * radius ** 2

        except ValueError:
            error = "Please enter a valid number."

    return render_template(
        "circle.html", result=result, error=error
    )

@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result = None
    error = None

    if request.method == "POST":
        try:
            base = float(request.form.get("base", ""))
            height = float(request.form.get("height", ""))

            if base <= 0 or height <= 0:
                error = "Please enter positive measurements."
            else:
                result = 0.5 * base * height

        except ValueError:
            error = "Please enter valid numbers."

    return render_template(
        "triangle.html", result=result, error=error
    )

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_beginning(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def append(self, data):
        node = Node(data)

        if self.head is None:
            self.head = node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = node

    def insert_middle(self, data):
        if self.head is None:
            self.head = Node(data)
            return

        length = len(self.display())
        middle = length // 2
        node = Node(data)

        if middle == 0:
            node.next = self.head
            self.head = node
            return

        current = self.head
        for _ in range(middle - 1):
            current = current.next

        node.next = current.next
        current.next = node

    def insert_after(self, data, after_value):
        current = self.head

        while current:
            if current.data == after_value:
                node = Node(data)
                node.next = current.next
                current.next = node
                return True

            current = current.next

        return False

    def remove_beginning(self):
        if self.head is None:
            return None

        removed = self.head.data
        self.head = self.head.next
        return removed

    def remove_end(self):
        if self.head is None:
            return None

        if self.head.next is None:
            removed = self.head.data
            self.head = None
            return removed

        current = self.head
        while current.next.next:
            current = current.next

        removed = current.next.data
        current.next = None
        return removed

    def delete(self, data):
        current = self.head
        previous = None

        while current:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def search(self, data):
        current = self.head

        while current:
            if current.data == data:
                return True
            current = current.next

        return False

    def clear(self):
        self.head = None

    def display(self):
        values = []
        current = self.head

        while current:
            values.append(current.data)
            current = current.next

        return values


linked_list = LinkedList()
queue_items = deque()


@app.route("/works/linkedlist", methods=["GET", "POST"])
def linkedlist():
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()
        after = request.form.get("after", "").strip()

        if action == "insert_beginning":
            if value:
                linked_list.insert_beginning(value)
                message = f"Inserted {value} at the beginning."
            else:
                message = "Please enter a value."

        elif action == "insert_middle":
            if value:
                linked_list.insert_middle(value)
                message = f"Inserted {value} in the middle."
            else:
                message = "Please enter a value."

        elif action == "insert_end":
            if value:
                linked_list.append(value)
                message = f"Inserted {value} at the end."
            else:
                message = "Please enter a value."

        elif action == "insert_after":
            if not value or not after:
                message = "Enter both values for Insert After."
            elif linked_list.insert_after(value, after):
                message = f"Inserted {value} after {after}."
            else:
                message = f"Node {after} was not found."

        elif action == "remove_beginning":
            removed = linked_list.remove_beginning()
            message = (
                f"Removed {removed}."
                if removed is not None
                else "The list is empty."
            )

        elif action == "remove_end":
            removed = linked_list.remove_end()
            message = (
                f"Removed {removed}."
                if removed is not None
                else "The list is empty."
            )

        elif action == "remove_value":
            if value and linked_list.delete(value):
                message = f"Removed {value}."
            else:
                message = f"{value or 'That value'} was not found."

        elif action == "search":
            if value and linked_list.search(value):
                message = f"{value} was found."
            else:
                message = f"{value or 'That value'} was not found."

        elif action == "clear":
            linked_list.clear()
            message = "Linked list cleared."

    return render_template(
        "linkedlist.html",
        values=linked_list.display(),
        message=message
    )


@app.route("/works/queue", methods=["GET", "POST"])
def queue_demo():
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "enqueue":
            if value:
                queue_items.append(value)
                message = f"Enqueued {value}."
            else:
                message = "Please enter a value to enqueue."
        elif action == "dequeue":
            if queue_items:
                message = f"Dequeued {queue_items.popleft()}."
            else:
                message = "The queue is empty."
        elif action == "clear":
            queue_items.clear()
            message = "Queue cleared."

    return render_template(
        "queue.html",
        values=list(queue_items),
        message=message
    )

precedence = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3
}


def convert_infix_to_postfix(expression):
    if not expression or not expression.strip():
        raise ValueError("Please enter an expression.")

    text = "".join(expression.split())
    tokens = re.findall(r"[A-Za-z]+|\d+|[()+\-*/^]", text)

    if "".join(tokens) != text:
        raise ValueError("The expression contains invalid characters.")

    stack = Stack()
    output = []

    for token in tokens:
        if token.isalnum():
            output.append(token)

        elif token == "(":
            stack.push(token)

        elif token == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())

            if stack.is_empty():
                raise ValueError("Mismatched parentheses.")

            stack.pop()

        elif token in precedence:
            while (
                not stack.is_empty()
                and stack.peek() != "("
                and (
                    precedence[stack.peek()] > precedence[token]
                    or (
                        precedence[stack.peek()] == precedence[token]
                        and token != "^"
                    )
                )
            ):
                output.append(stack.pop())

            stack.push(token)

    while not stack.is_empty():
        item = stack.pop()

        if item == "(":
            raise ValueError("Mismatched parentheses.")

        output.append(item)

    return " ".join(output)


@app.route("/works/infix-postfix", methods=["GET", "POST"])
def infix_postfix():
    expression = ""
    result = None
    error = None

    if request.method == "POST":
        expression = request.form.get("expression", "")

        try:
            result = convert_infix_to_postfix(expression)
        except (ValueError, TypeError, IndexError) as exc:
            error = str(exc)

    return render_template(
        "infix_postfix.html",
        expression=expression,
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
