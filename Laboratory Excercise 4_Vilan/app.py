from flask import Flask, render_template, request
import math

app = Flask(__name__)


# =========================
# HOME
# =========================

@app.route('/')
def index():
    return render_template('index.html')


# =========================
# PROFILE
# =========================

@app.route('/profile')
def profile():
    return render_template('profile.html')


# =========================
# WORKS - UPPERCASE
# =========================

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None

    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()

    return render_template(
        'touppercase.html',
        result=result
    )


# =========================
# CIRCLE AREA
# =========================

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():

    result = None
    error = None

    if request.method == 'POST':

        try:
            radius = float(request.form.get('radius', ''))

            if radius <= 0:
                error = 'Please enter a positive radius.'
            else:
                result = math.pi * radius ** 2

        except ValueError:
            error = 'Please enter a valid number.'

    return render_template(
        'circle.html',
        result=result,
        error=error
    )


# =========================
# TRIANGLE AREA
# =========================

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():

    result = None
    error = None

    if request.method == 'POST':

        try:
            base = float(request.form.get('base', ''))
            height = float(request.form.get('height', ''))

            if base <= 0 or height <= 0:
                error = 'Please enter positive measurements.'
            else:
                result = 0.5 * base * height

        except ValueError:
            error = 'Please enter valid numbers.'

    return render_template(
        'triangle.html',
        result=result,
        error=error
    )


# =========================
# LINKED LIST
# =========================

class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def append(self, data):

        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

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

    def display(self):

        values = []

        current = self.head

        while current:

            values.append(current.data)

            current = current.next

        return values


linked_list = LinkedList()


@app.route('/works/linkedlist', methods=['GET', 'POST'])
def linkedlist():

    message = None

    if request.method == 'POST':

        action = request.form.get('action')
        value = request.form.get('value', '').strip()

        if action == 'add' and value:

            linked_list.append(value)

            message = f'Added: {value}'

        elif action == 'delete' and value:

            if linked_list.delete(value):

                message = f'Deleted: {value}'

            else:

                message = f'{value} was not found.'

        elif action == 'clear':

            linked_list.head = None

            message = 'Linked list cleared.'

    return render_template(
        'linkedlist.html',
        values=linked_list.display(),
        message=message
    )


# =========================
# CONTACT
# =========================

@app.route('/contact')
def contact():
    return render_template('contact.html')


# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':
    app.run(debug=True)