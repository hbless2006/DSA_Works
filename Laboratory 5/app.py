
from flask import Flask, request, render_template_string
from stack import Stack
import re

app = Flask(__name__)

order_of_precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}


def split_into_tokens(expression):
    if expression is None or not expression.strip():
        raise ValueError("Please enter an infix expression.")

    text = ''.join(expression.split())
    tokens = re.findall(r'[A-Za-z]+|\d+|[()+\-*/^]', text)

    if ''.join(tokens) != text:
        raise ValueError("Invalid character in expression.")

    return tokens


def is_valid_operand(token):
    return token.isalnum()


def convert_infix_to_postfix(expression):
    tokens = split_into_tokens(expression)

    ops = Stack()
    output = []

    for token in tokens:
        if is_valid_operand(token):
            output.append(token)

        elif token == '(':
            ops.push(token)

        elif token == ')':
            while not ops.is_empty() and ops.peek() != '(':
                output.append(ops.pop())

            if ops.is_empty():
                raise ValueError("Mismatched parentheses.")

            ops.pop()

        elif token in order_of_precedence:
            while (
                not ops.is_empty()
                and ops.peek() != '('
                and (
                    order_of_precedence[ops.peek()]
                    > order_of_precedence[token]
                    or (
                        order_of_precedence[ops.peek()]
                        == order_of_precedence[token]
                        and token != '^'
                    )
                )
            ):
                output.append(ops.pop())

            ops.push(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    while not ops.is_empty():
        leftover = ops.pop()

        if leftover == '(':
            raise ValueError("Mismatched parentheses.")

        output.append(leftover)

    return ' '.join(output)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infix to Postfix Converter</title>
    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">

        <header class="header">
            <p class="small-title">PYTHON STACK PROJECT</p>
            <h1>Infix to Postfix</h1>
            <p>Transform expressions using the Stack data structure.</p>
        </header>

        <form method="POST">
            <label for="expression">Enter Infix Expression</label>

            <input
                type="text"
                id="expression"
                name="expression"
                placeholder="Example: A*(B+C)/D"
                value="{{ expression }}"
                required
            >

            <button type="submit">Convert Expression</button>
        </form>

        {% if result %}
        <div class="result">
            <h3>Conversion Successful!</h3>
            <p>Infix: {{ expression }}</p>
            <p>Postfix: {{ result }}</p>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">
            <strong>Error:</strong> {{ error }}
        </div>
        {% endif %}

        <section class="examples">
            <h3>Try These Examples</h3>
            <p><code>(A+B+C)*D</code></p>
            <p><code>A*(B+C)/D</code></p>
            <p><code>A*(B+C^D)</code></p>
        </section>

        <footer>
            Infix to Postfix Converter | Stack Data Structure
        </footer>

    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    expression = ''
    result = ''
    error = ''

    if request.method == 'POST':
        expression = request.form.get('expression', '')

        try:
            result = convert_infix_to_postfix(expression)
        except ValueError as e:
            error = str(e)

    return render_template_string(
        HTML,
        expression=expression,
        result=result,
        error=error
    )


if __name__ == '__main__':
    app.run(debug=True)