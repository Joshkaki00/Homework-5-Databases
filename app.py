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
    # Retrieve all plants from the MongoDB `plants` collection.
    plants_data = mongo.db.plants.find()

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
        # Get the new plant's data from the form and insert into the database.
        new_plant = {
            'name': request.form['name'],
            'variety': request.form['variety'],
            'photo_url': request.form['photo_url'],
            'date_planted': request.form['date_planted']
        }
        result = mongo.db.plants.insert_one(new_plant)

        return redirect(url_for('detail', plant_id=str(result.inserted_id)))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""
    # Retrieve the plant with the given ID from the MongoDB `plants` collection.
    plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

    # Retrieve all harvests for the plant from the `harvests` collection.
    harvests = mongo.db.harvests.find({'plant_id': plant_id})

    context = {
        'plant': plant_to_show,
        'harvests': harvests
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """
    # Create a new harvest object from the form data.
    new_harvest = {
        'quantity': request.form['quantity'],
        'date': request.form['date'],
        'plant_id': plant_id
    }

    # Insert the harvest into the MongoDB `harvests` collection.
    mongo.db.harvests.insert_one(new_harvest)

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # Update the plant with the new data from the form.
        updated_plant = {
            '$set': {
                'name': request.form['name'],
                'variety': request.form['variety'],
                'photo_url': request.form['photo_url'],
                'date_planted': request.form['date_planted']
            }
        }
        mongo.db.plants.update_one({'_id': ObjectId(plant_id)}, updated_plant)

        return redirect(url_for('detail', plant_id=plant_id))
    else:
        # Retrieve the plant to display in the edit form.
        plant_to_show = mongo.db.plants.find_one({'_id': ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    """Deletes the plant and all its associated harvests."""
    # Delete the plant with the given ID from the MongoDB `plants` collection.
    mongo.db.plants.delete_one({'_id': ObjectId(plant_id)})

    # Delete all harvests associated with the plant ID from the `harvests` collection.
    mongo.db.harvests.delete_many({'plant_id': plant_id})

    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)
