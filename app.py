from flask import Flask, render_template, request
import re
app = Flask(__name__)

# Fungsi konversi input user ke format Python-valid
def convert_expression(expr):
    expr = expr.replace('^', '**')  # Ubah pangkat jadi **
    expr = re.sub(r'(\d)(x)', r'\1*\2', expr)  # 2x → 2*x
    expr = re.sub(r'(x)(\d)', r'\1*\2', expr)  # x2 → x*2 (jarang tapi jaga-jaga)
    expr = re.sub(r'([)\d])\(', r'\1*(', expr)  # 2(x+1) → 2*(x+1)
    return expr

# Fungsi Metode Simpson 1/3
def simpson13(f, a, b, n):
    if n % 2 == 1:
        n += 1  # n harus genap
    h = (b - a) / n
    x = [a + i*h for i in range(n+1)]
    y = [f(xi) for xi in x]
    
    result = y[0] + y[-1]
    for i in range(1, n):
        if i % 2 == 0:
            result += 2 * y[i]
        else:
            result += 4 * y[i]
    return (h / 3) * result

@app.route('/', methods=['GET', 'POST'])
def index():
    formatted_result = None
    a = b = n = fx_input = ''
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])
            fx_input = request.form['function']

            # Konversi input dari user
            fx = convert_expression(fx_input)

            # Evaluasi fungsi f(x)
            def f(x):
                return eval(fx, {"x": x, "__builtins__": {}})

            result = simpson13(f, a, b, n)
            formatted_result = f"Hasil Integral: {result:.3f}"
        except Exception as e:
            formatted_result = f"Terjadi kesalahan: {e}"

    return render_template('index.html', result=formatted_result, a=a, b=b, n=n, fx=fx_input)

if __name__ == '__main__':
    app.run(debug=True)
