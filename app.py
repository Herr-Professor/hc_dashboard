from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import json
import os
from visualizations import create_summary_charts, create_custom_plot, create_search_result_plot
from data_processor import process_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('dashboard', filename=filename))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    filename = request.args.get('filename', 'sample_healthcare_data.csv')
    data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    processed_data = process_data(data)
    summary_charts = create_summary_charts(processed_data)
    columns = data.columns.tolist()
    
    return render_template('dashboard.html', 
                           summary_charts=summary_charts,
                           columns=columns,
                           filename=filename)

@app.route('/plot', methods=['POST'])
def plot():
    filename = request.json['filename']
    data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    x_axis = request.json['x_axis']
    y_axis = request.json['y_axis']
    
    plot_data = create_custom_plot(data, x_axis, y_axis)
    return jsonify(plot_data)

@app.route('/search', methods=['POST'])
def search():
    try:
        filename = request.json['filename']
        search_term = request.json['search_term']
        data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Perform search across all columns
        mask = data.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        search_results = data[mask]
        
        if len(search_results) > 0:
            plot_data = create_search_result_plot(search_results, search_term)
            return jsonify({'plot': plot_data, 'count': len(search_results)})
        else:
            return jsonify({'plot': None, 'count': 0})
    except Exception as e:
        app.logger.error(f"Error in search route: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)