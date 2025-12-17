from flask import Flask, jsonify, abort
import re

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name")
    
    if not name:
        return "Name is required", 400
    
    try:
        # Validate 'name' parameter to be a non-empty string without special characters (basic validation)
        pattern = re.compile(r"^[a-zA-Z\s]+$")
        if not name or not pattern.match(name):
            abort(400, description="Invalid input: 'name' must be a non-empty string with letters and spaces only.")
    except Exception as e:
        # Basic exception handling for unexpected errors during validation
        return str(e), 500
    
    response = jsonify({"message": f"Hello, {name}!"})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run()