from flask import Flask, request, jsonify
from flask_cors import CORS
from models import get_db

app = Flask(__name__)
CORS(app)

@app.route("/matches",methods=["GET"])
def get_matches():
	db = get_db()
	cursor = db.cursor(dictionary=True)

	try:
		cursor.execute("SELECT * FROM matches")
		data = cursor.fetchall()
		
		return jsonify({"matches": data}), 200
		
	except Exception as e:
		return jsonify({"error": str(e)}), 500
	
	finally:
		cursor.close()
		db.close()


@app.route("/matches/<int:match_id>",methods=["GET"])
def get_one_match(match_id):
	db = get_db()
	cursor = db.cursor(dictionary=True)
	
	try:
		sql_line = "SELECT * FROM matches WHERE id = %s"
		cursor.execute(sql_line,(match_id,))
		row = cursor.fetchone()
		return jsonify({"match details": row}),200
	except Exception as e:
		return jsonify({"error": str(e)})
	finally:
		cursor.close()
		db.close()

	
@app.route("/matches",methods=["POST"])
def create_match():
	data = request.get_json()
	db = get_db()
	cursor = db.cursor(dictionary=True)
	
	try:
		cursor.execute("INSERT INTO matches(team_a, team_b, match_date, total_tickets, available_tickets) VALUES(%s,%s,%s,%s,%s)",(data['team_a'],data['team_b'],data['match_date'],data['total_tickets'],data['available_tickets']))
		
		db.commit()
		return jsonify({"message": "match data added successfuly!"}),201
	except Exception as e:
		db.rollback()
		return jsonify({"error": str(e)}),500
	finally:
		cursor.close()
		db.close()
		
@app.route("/matches/<int:match_id>/book",methods=["PUT"])
def update_match(match_id):
	buy_tickets = request.get_json()
	db = get_db()
	cursor = db.cursor(dictionary=True)
	try:
		sql_line = "SELECT * FROM matches WHERE id = %s"
		cursor.execute(sql_line,(match_id,))
		row = cursor.fetchone()
		avl_t = row['available_tickets']
		new_avl_t = avl_t - buy_tickets['tickets_to_buy']
		
		cursor.execute("UPDATE matches SET available_tickets = %s WHERE id = %s",(new_avl_t,match_id))
		db.commit()
		return jsonify({"message": "Data is updated!"}),201
	except Exception as e:
		db.rollback()
		return jsonify({"error": str(e)}),500
	finally:
		cursor.close()
		db.close()
		
@app.route("/matches/<int:match_id>",methods=["DELETE"])
def delete_match(match_id):
	db = get_db()
	cursor = db.cursor(dictionary=True)
	
	try:
		cursor.execute("DELETE FROM matches WHERE id = %s",(match_id,))
		db.commit()
		return jsonify({"message":"match data deleted!"}),200
	except Exception as e:
		db.rollback()
		return jsonify({"error": str(e)}),500
	finally:
		cursor.close()
		db.close()
		
@app.route("/matches/<int:match_id>",methods=["PUT"])
def match_data_update(match_id):
	data = request.get_json()
	db = get_db()
	cursor = db.cursor(dictionary=True)
	
	try:
		sql = "UPDATE matches SET team_a = %s,team_b = %s, match_date = %s, total_tickets = %s WHERE id = %s"
		cursor.execute(sql,(data['team_a'],data['team_b'],data['match_date'],data['total_tickets'],match_id))
		
		db.commit()
		return jsonify({"message": "match details updated successfully!"}), 200
	except Exception as e:
		db.rollback()
		return jsonify({"error" : str(e)}),400
	finally:
		cursor.close()
		db.close()

if __name__ == "__main__":
	app.run(debug=True)
		
		
