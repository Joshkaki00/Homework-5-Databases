from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.errors import InvalidId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    # Retrieve all plants from the database
    plants_data = list(mongo.db.plants.find())

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # Gather data from form
        new_plant = {
            'name': request.form.get('name'),
            'variety': request.form.get('variety'),
            'photo_url': request.form.get('photo_url'),
            'date_planted': request.form.get('date_planted')
        }
        # Insert new plant into database
        result = mongo.db.plants.insert_one(new_plant)

        return redirect(url_for('detail', plant_id=str(result.inserted_id)))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""

    try:
        # Validate and convert plant_id to ObjectId
        plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})
    except (InvalidId, TypeError):
        return "Invalid plant ID", 400

    if not plant_to_show:
        return "Plant not found", 404

    # Find all harvests associated with this plant
    harvests = list(mongo.db.harvests.find({'plant_id': plant_id}))

    context = {
        'plant' : plant_to_show,
        'harvests': harvests
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """
    try:
        ObjectId(plant_id)
    except (InvalidId, TypeError):
        return "Invalid plant ID", 400

    # Create new harvest object
    new_harvest = {
        'quantity': request.form.get('quantity'), # e.g. '3 tomatoes'
        'date': request.form.get('date'),
        'plant_id': plant_id
    }
    if not new_harvest['quantity']:
        return "Quantity is required", 400

    # Insert new harvest into database
    mongo.db.harvests.insert_one(new_harvest)

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # Update plant with given plant_id
        updated_fields = {
            '$set' : {
                'name': request.form.get('name'),
                'variety': request.form.get('variety'),
                'photo_url': request.form.get('photo_url'),
                'date_planted': request.form.get('date_planted')
                }
        }
        mongo.db.plants.update_one({'_id': ObjectId(plant_id)}, updated_fields)

        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # Find the plant with given plant_id
        plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # Delete plant with given plant_id
    mongo.db.plants.delete_one({'_id': ObjectId(plant_id)})

    # Delete all harvests associated with this plant
    mongo.db.harvests.delete_many({'plant_id': plant_id})

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)

