from flask import Flask, render_template, jsonify
import collect_metrics
import database
import ml_model
import optimizer

app = Flask(__name__)

# Initialize DB on start
try:
    database.init_db()
except Exception as e:
    print(f"Warning during DB init: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/current')
def api_current():
    # Collect and store real metric
    data = collect_metrics.collect_and_store()
    return jsonify(data)

@app.route('/api/history')
def api_history():
    history = database.fetch_history(20)
    return jsonify(history)

@app.route('/api/processes')
def api_processes():
    return jsonify(collect_metrics.get_process_list())

@app.route('/api/retrain')
def api_retrain():
    # Force retrain of model
    ml_model.train_dummy_model()
    return jsonify({"status": "success", "message": "Model retrained successfully."})

@app.route('/api/recommend')
def api_recommend():
    data = collect_metrics.get_system_metrics()
    prediction = ml_model.predict_system_load(data['cpu'], data['ram'], data['disk'])
    recs = optimizer.get_recommendation(prediction, data['cpu'], data['ram'], data['disk'], data.get('top_process'))
    
    return jsonify({
        "load_status": prediction,
        "recommendations": recs,
        "top_process": data.get('top_process')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
