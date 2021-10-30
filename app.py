from flask import Flask, flash, render_template, redirect, request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    error = None
    if request.method == 'POST':
        if request.form['X_axis'] != '0' or \
                request.form['Y_axis'] != '0':
            error = 'Bike is relocated!!'
            flash('Bike is relocated!!')
        else:
            error = 'Bike is at rest.'
            flash('Bike is at rest.')
            return redirect(url_for('index'))
    return render_template('inputs.html', error=error)


if __name__ == '__main__':
    app.run()
