# Richardson Extrapolation - Numerical Methods Project

## Project Overview

This Flask web application provides an interactive calculator and educational resource for **Richardson Extrapolation**, a powerful numerical method used to improve the accuracy of derivative approximations.

## Project Structure

```
/workspace/
├── app.py                  # Flask application with core algorithms
├── templates/
│   └── index.html          # Main HTML template with MathJax
├── static/
│   ├── css/
│   │   └── style.css       # Custom styling
│   └── js/
│       └── calculator.js   # Client-side JavaScript
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment configuration
└── README.md              # This file
```

## Features

### 1. Mathematical Discussion
- Comprehensive theoretical foundation of Richardson Extrapolation
- Derivation of the central difference formula
- Step-by-step explanation of the extrapolation process
- Error analysis and convergence properties

### 2. Worked Examples
Two complete, step-by-step solved examples:

**Example 1:** Derivative of \( f(x) = x^2 \sin(x) \) at \( x = 1.0 \)
- Initial step size: \( h_0 = 0.1 \)
- 4 levels of extrapolation
- Achieves accuracy improvement of ~5600×

**Example 2:** Derivative of \( f(x) = e^x \cos(x) \) at \( x = 0.5 \)
- Initial step size: \( h_0 = 0.2 \)
- 3 levels of extrapolation
- Achieves accuracy improvement of ~450×

### 3. Interactive Calculator
- User-defined function input with support for: sin, cos, tan, exp, log, sqrt, abs
- Configurable evaluation point (x)
- Adjustable initial step size (h₀)
- Selectable number of extrapolation levels (1-10)
- Real-time result display with full extrapolation table
- Convergence analysis with error estimates

## Installation

### Local Development

1. Install dependencies:
```bash
pip install flask
```

2. Run the application:
```bash
python app.py
```

3. Open browser to: http://127.0.0.1:5000

### Vercel Deployment

1. Create a Vercel account at https://vercel.com

2. Install Vercel CLI:
```bash
npm install -g vercel
```

3. Deploy:
```bash
vercel login
vercel --prod
```

## Technical Implementation

### Core Algorithm

The Richardson Extrapolation algorithm uses:

1. **Central Difference Formula** as the base approximation:
   \[
   D(h) = \frac{f(x+h) - f(x-h)}{2h}
   \]

2. **Recursive Extrapolation Formula**:
   \[
   D_j(h) = \frac{4^j D_{j-1}(h/2) - D_{j-1}(h)}{4^j - 1}
   \]

3. **Error Estimation**: The difference between successive diagonal elements provides an error estimate.

### Safe Function Parsing

User-provided functions are evaluated using a restricted namespace:
- Only safe mathematical functions are exposed
- No access to built-in Python functions
- Uses `eval()` with compiled expressions for security

### Technologies Used

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Math Rendering**: MathJax 3
- **Deployment**: Vercel

## API Endpoints

### GET /
Returns the main page with mathematical discussion, examples, and calculator interface.

### POST /calculate
Accepts JSON payload:
```json
{
    "function": "x**2 * sin(x)",
    "x": 1.0,
    "h": 0.1,
    "levels": 4
}
```

Returns JSON response:
```json
{
    "success": true,
    "table": [["2.2193305444"], ["2.2222661314", "2.2232446605"], ...],
    "diagonal": ["2.2193305444", "2.2232446605", ...],
    "best_estimate": "2.2232442755",
    "errors": ["3.91e-03", "6.97e-07", ...],
    "x": 1.0,
    "h0": 0.1,
    "function": "x**2 * sin(x)"
}
```

## Accuracy Verification

The implementation has been verified against analytical solutions:

| Example | Exact Value | Computed Value | Absolute Error |
|---------|-------------|----------------|----------------|
| \( x^2 \sin(x) \) at x=1.0 | 2.2232442755 | 2.2232442755 | 6.22×10⁻¹⁵ |
| \( e^x \cos(x) \) at x=0.5 | 0.6564499534 | 0.6564499569 | 3.55×10⁻⁹ |

## Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Safe evaluation of user functions | Restricted namespace with only math functions |
| Numerical precision issues | Using Python's float (double precision) |
| Division by very small numbers | Input validation for minimum step size |
| Responsive design | CSS flexbox and media queries |
| Math rendering in browser | MathJax 3 with async loading |

## Future Enhancements

- Plotting capabilities for function visualization
- Export results to CSV/PDF
- Additional numerical differentiation methods
- Support for complex-valued functions
- Automatic optimal step size selection

## License

This project is created for educational purposes as part of the PIT Project – Numerical Methods Online Calculator.

## Author

Created for the Numerical Methods course, 2026.
