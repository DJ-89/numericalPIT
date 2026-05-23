"""
Flask application for Richardson Extrapolation numerical method.
This module provides a web interface with mathematical discussion,
worked examples, and an interactive calculator.
"""

from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


def f(x):
    """
    Default function for demonstration: f(x) = x^2 * sin(x)
    Can be modified or extended to support user-defined functions.
    """
    return x**2 * math.sin(x)


def parse_function(func_str, x_val):
    """
    Safely evaluate a mathematical function string at a given x value.
    Uses a restricted namespace to prevent code injection.
    
    Args:
        func_str: String representation of the function (e.g., "x**2 * sin(x)")
        x_val: The x value at which to evaluate
        
    Returns:
        The evaluated function value
    """
    # Restricted namespace with only safe math functions
    safe_dict = {
        'x': x_val,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'abs': abs,
        'pi': math.pi,
        'e': math.e,
    }
    
    try:
        # Evaluate the expression directly
        result = eval(compile(func_str, '<string>', 'eval'), {"__builtins__": {}}, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Error evaluating function '{func_str}' at x={x_val}: {str(e)}")


def forward_difference(f, x, h):
    """Calculate forward difference approximation: (f(x+h) - f(x)) / h"""
    return (f(x + h) - f(x)) / h


def central_difference(f, x, h):
    """Calculate central difference approximation: (f(x+h) - f(x-h)) / (2h)"""
    return (f(x + h) - f(x - h)) / (2 * h)


def richardson_extrapolation(f, x, h0, n_levels=4):
    """
    Perform Richardson extrapolation to improve derivative approximation.
    
    Uses central difference as the base method and applies Richardson
    extrapolation recursively to eliminate error terms.
    
    Args:
        f: Function to differentiate
        x: Point at which to calculate derivative
        h0: Initial step size
        n_levels: Number of extrapolation levels
        
    Returns:
        Dictionary containing the extrapolation table and results
    """
    # Initialize the extrapolation table
    # D[i][j] where i is the level of refinement, j is the extrapolation order
    D = []
    
    # First column: central difference approximations with decreasing h
    for i in range(n_levels):
        h = h0 / (2 ** i)
        d_val = central_difference(f, x, h)
        D.append([d_val])
    
    # Apply Richardson extrapolation formula
    # D[i][j] = (4^j * D[i][j-1] - D[i-1][j-1]) / (4^j - 1)
    for j in range(1, n_levels):
        for i in range(j, n_levels):
            factor = 4 ** j
            d_new = (factor * D[i][j-1] - D[i-1][j-1]) / (factor - 1)
            D[i].append(d_new)
    
    # Extract diagonal elements (best estimates at each level)
    diagonal = [D[i][i] for i in range(len(D))]
    
    # Calculate errors if we have enough levels
    errors = []
    if len(diagonal) > 1:
        for i in range(1, len(diagonal)):
            errors.append(abs(diagonal[i] - diagonal[i-1]))
    
    return {
        'table': D,
        'diagonal': diagonal,
        'best_estimate': diagonal[-1] if diagonal else None,
        'errors': errors
    }


@app.route('/')
def index():
    """Render the main page with all content."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculator requests."""
    try:
        data = request.get_json()
        
        # Parse inputs
        func_str = data.get('function', 'x**2 * sin(x)')
        x = float(data.get('x', 1.0))
        h0 = float(data.get('h', 0.1))
        n_levels = int(data.get('levels', 4))
        
        # Validate inputs
        if h0 <= 0:
            return jsonify({'error': 'Step size must be positive'}), 400
        if n_levels < 1 or n_levels > 10:
            return jsonify({'error': 'Number of levels must be between 1 and 10'}), 400
        
        # Create function wrapper
        def user_func(val):
            return parse_function(func_str, val)
        
        # Perform Richardson extrapolation
        result = richardson_extrapolation(user_func, x, h0, n_levels)
        
        # Format the table for display
        formatted_table = []
        for i, row in enumerate(result['table']):
            formatted_row = []
            for j, val in enumerate(row):
                formatted_row.append(f"{val:.10f}")
            formatted_table.append(formatted_row)
        
        # Format diagonal and errors
        formatted_diagonal = [f"{v:.10f}" for v in result['diagonal']]
        formatted_errors = [f"{v:.2e}" for v in result['errors']] if result['errors'] else []
        
        return jsonify({
            'success': True,
            'table': formatted_table,
            'diagonal': formatted_diagonal,
            'best_estimate': f"{result['best_estimate']:.10f}",
            'errors': formatted_errors,
            'x': x,
            'h0': h0,
            'function': func_str
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
