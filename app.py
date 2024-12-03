from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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

    # Retrieve the plant with matching plant_id
    plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

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

    # Create new harvest object
    new_harvest = {
        'quantity': request.form.get('quantity'), # e.g. '3 tomatoes'
        'date': request.form.get('date'),
        'plant_id': plant_id
    }

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
        
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # TODO: Make a `find_one` database call to get the plant object with the
        # passed-in _id.
        plant_to_show = ''

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    # TODO: Make a `delete_one` database call to delete the plant with the given
    # id.

    # TODO: Also, make a `delete_many` database call to delete all harvests with
    # the given plant id.

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)

