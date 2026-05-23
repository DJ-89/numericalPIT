"""
Flask application for Richardson Extrapolation numerical method.
"""
from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__)

def parse_function(func_str, x_val):
    """
    Safely evaluate a mathematical function string using SymPy.
    This prevents Python code injection vulnerabilities.
    """
    x = sp.Symbol('x')
    try:
        # sympify safely evaluates math strings without executing arbitrary code
        expr = sp.sympify(func_str)
        
        # Substitute x with the provided value and evaluate to a float
        result = expr.subs(x, x_val).evalf()
        
        # Check for complex numbers (e.g., sqrt(-1))
        if not result.is_real:
            raise ValueError("Function resulted in a complex number at this point.")
            
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid mathematical function or evaluation error: {str(e)}")

def central_difference(f_expr, x_val, h):
    """Calculate central difference approximation"""
    return (parse_function(f_expr, x_val + h) - parse_function(f_expr, x_val - h)) / (2 * h)

def richardson_extrapolation(func_str, x_val, h0, n_levels=4):
    """
    Perform Richardson extrapolation using the safely parsed function.
    """
    D = []
    
    # First column: central difference approximations
    for i in range(n_levels):
        h = h0 / (2 ** i)
        d_val = central_difference(func_str, x_val, h)
        D.append([d_val])
    
    # Apply Richardson extrapolation formula
    for j in range(1, n_levels):
        for i in range(j, n_levels):
            factor = 4 ** j
            d_new = (factor * D[i][j-1] - D[i-1][j-1]) / (factor - 1)
            D[i].append(d_new)
    
    diagonal = [D[i][i] for i in range(len(D))]
    
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
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        func_str = data.get('function', 'x**2 * sin(x)')
        x_val = float(data.get('x', 1.0))
        h0 = float(data.get('h', 0.1))
        n_levels = int(data.get('levels', 4))
        
        if h0 <= 0:
            return jsonify({'error': 'Step size must be positive'}), 400
        if n_levels < 1 or n_levels > 10:
            return jsonify({'error': 'Number of levels must be between 1 and 10'}), 400
            
        # Test function parsing immediately before running the heavy loop
        parse_function(func_str, x_val)
        
        result = richardson_extrapolation(func_str, x_val, h0, n_levels)
        
        formatted_table = [[f"{val:.10f}" for val in row] for row in result['table']]
        formatted_diagonal = [f"{v:.10f}" for v in result['diagonal']]
        formatted_errors = [f"{v:.2e}" for v in result['errors']] if result['errors'] else []
        
        return jsonify({
            'success': True,
            'table': formatted_table,
            'diagonal': formatted_diagonal,
            'best_estimate': f"{result['best_estimate']:.10f}",
            'errors': formatted_errors,
            'x': x_val,
            'h0': h0,
            'function': func_str
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred. Please check your inputs.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)