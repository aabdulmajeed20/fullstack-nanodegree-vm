from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

engine = create_engine("sqlite:///restaurantmenu.db", connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    # restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = item.serialize)    

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if(request.method == 'POST'):
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Item Created!")
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenu.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if(request.method == 'POST'):
        if(request.form['name']):
            item.name = request.form['name']
        session.add(item)
        session.commit()
        flash("Item edited successfully!")
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = item)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if(request.method == 'POST'):
        session.delete(item)
        session.commit()
        flash("Item deleted successfully!")
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = item)

if(__name__ == "__main__"):
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)