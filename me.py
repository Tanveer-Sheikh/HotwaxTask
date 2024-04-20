import pyodbc
from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=DESKTOP-1H3F6QG;'
                      'DATABASE=newdatabase;'
                      'UID=Tanveer;'
                      'PWD=tanveer')

cursor = conn.cursor()

class Party(Resource):
    def get(self, emp_id=None):
        cursor.execute("SELECT * FROM [newdatabase].[dbo].[Party]")
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            try:
                record = {
                    "party_id": row.party_id,
                    "party_enum_type_id": row.party_enum_type_id
                }
                records.append(record)
            except TypeError:
                # Skip rows that don't match the expected format
                continue
        
        return jsonify(records)


    def post(self):
        data = request.get_json()
        cursor.execute("INSERT INTO [newdatabase].[dbo].[party] (party_id,party_enum_type_id) VALUES (?,?);",
                       data['party_id'],data['party_enum_type_id'])
        conn.commit()
        print("yheegfdsklgfjdgkdf")
        return {"message": "Party added successfully"}, 201

    def put(self):
        data = request.get_json()
        cursor.execute("""
            UPDATE [newdatabase].[dbo].[party]
            SET party_enum_type_id = ?
            WHERE party_id = ?;
        """, data['party_enum_type_id'], data['party_id'])
        conn.commit()
        return {"message": "Party Updated successfully"}, 201

    def delete(self,party_id):
        cursor.execute("DELETE FROM [newdatabase].[dbo].[party] WHERE party_id=?", party_id)
        conn.commit()
        return jsonify({"message": "Party deleted successfully"})




class Person(Resource):
    def get(self):
        cursor.execute("SELECT * FROM [newdatabase].[dbo].[person];")
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            try:
                record = {
                    "party_id": row[0],  
                    "first_name": row[1],  
                    "middle_name": row[2], 
                    "last_name": row[3], 
                    "gender": row[4],  
                    "birth_date": str(row[5]), 
                    "marital_status_enum_id": row[6], 
                    "employment_status_enum_id": row[7],
                    "occupation": row[8] 
                }
                records.append(record)
            except TypeError:
                
                continue
        
        return jsonify(records)

    def post(self):
        data = request.get_json()
        
        # Extract values from JSON data
        party_id = data.get('party_id')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        last_name = data.get('last_name')
        gender = data.get('gender')
        birth_date = data.get('birth_date')
        marital_status_enum_id = data.get('marital_status_enum_id')
        employment_status_enum_id = data.get('employment_status_enum_id')
        occupation = data.get('occupation')
        
        # Check if party_id is provided
        if not party_id:
            return {"message": "party_id is required"}, 400
        
        try:
            cursor.execute("""
                INSERT INTO [newdatabase].[dbo].[person] 
                (party_id, first_name, middle_name, last_name, gender, birth_date, 
                marital_status_enum_id, employment_status_enum_id, occupation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, party_id, first_name, middle_name, last_name, gender, birth_date, 
                marital_status_enum_id, employment_status_enum_id, occupation)
            
            conn.commit()
            
            return {"message": "Person added successfully"}, 201
        
        except Exception as e:
            return {"message": f"Error adding person: {str(e)}"}, 500


    def put(self):
        data = request.get_json()
        
        party_id = data.get('party_id')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        last_name = data.get('last_name')
        gender = data.get('gender')
        birth_date = data.get('birth_date')
        marital_status_enum_id = data.get('marital_status_enum_id')
        employment_status_enum_id = data.get('employment_status_enum_id')
        occupation = data.get('occupation')
        
        if not any([first_name, middle_name, last_name, gender, birth_date,
                    marital_status_enum_id, employment_status_enum_id, occupation]):
            return {"message": "At least one field is required for update"}, 400
        
        try:
            cursor.execute("""
                UPDATE [newdatabase].[dbo].[person]
                SET first_name = ?,
                    middle_name = ?,
                    last_name = ?,
                    gender = ?,
                    birth_date = ?,
                    marital_status_enum_id = ?,
                    employment_status_enum_id = ?,
                    occupation = ?
                WHERE party_id = ?;
            """, first_name, middle_name, last_name, gender, birth_date,
                marital_status_enum_id, employment_status_enum_id, occupation,
                party_id)
            
            conn.commit()
            
            return {"message": "Person updated successfully"}, 200
        
        except Exception as e:
            return {"message": f"Error updating person: {str(e)}"}, 500


    def delete(self,party_id):
        cursor.execute("DELETE FROM [newdatabase].[dbo].[Person] WHERE party_id=?", party_id)
        conn.commit()
        return jsonify({"message": "Person deleted successfully"})


class OrderHeader(Resource):
    def get(self):
        cursor.execute("""
            SELECT 
                [order_id],
                [order_name],
                [placed_date],
                [approved_date],
                [status_id],
                [party_id],
                [currency_uom_id],
                [product_store_id],
                [sales_channel_enum_id],
                [grand_total],
                [completed_date],
                  [credit_card]
            FROM [newdatabase].[dbo].[order_header];
        """)
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            try:
                record = {
                    "order_id": row[0],
                    "order_name": row[1],
                    "placed_date": str(row[2]),
                    "approved_date": str(row[3]),
                    "status_id": row[4],
                    "party_id": row[5],
                    "currency_uom_id": row[6],
                    "product_store_id": row[7],
                    "sales_channel_enum_id": row[8],
                    "grand_total": float(row[9]),  # Convert to float if needed
                    "completed_date": str(row[10]),
                    "credit_card": str(row[11])
                }
                records.append(record)
            except TypeError:
          
                continue
        
        return jsonify(records)

    def post(self):
        data = request.get_json()
        
        order_id = data.get('order_id')
        order_name = data.get('order_name')
        placed_date = data.get('placed_date')
        approved_date = data.get('approved_date')
        status_id = data.get('status_id')
        party_id = data.get('party_id')
        currency_uom_id = data.get('currency_uom_id')
        product_store_id = data.get('product_store_id')
        sales_channel_enum_id = data.get('sales_channel_enum_id')
        grand_total = data.get('grand_total')
        completed_date = data.get('completed_date')
        credit_card = data.get('credit_card')
        
        if not order_id:
            return {"message": "order_id is required"}, 400
        
        try:
            cursor.execute("""
                INSERT INTO [newdatabase].[dbo].[order_header] 
                (order_id, order_name, placed_date, approved_date, status_id, party_id, 
                currency_uom_id, product_store_id, sales_channel_enum_id, grand_total, completed_date,credit_card)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?);
            """, order_id, order_name, placed_date, approved_date, status_id, party_id, 
            currency_uom_id, product_store_id, sales_channel_enum_id, grand_total, completed_date,credit_card)
            
            conn.commit()
            
            return {"message": "Order added successfully"}, 201
        
        except Exception as e:
            return {"message": f"Error adding order: {str(e)}"}, 500


    def put(self):
        data = request.get_json()
        
        order_id = data.get('order_id')
        order_name = data.get('order_name')
        placed_date = data.get('placed_date')
        approved_date = data.get('approved_date')
        status_id = data.get('status_id')
        party_id = data.get('party_id')
        currency_uom_id = data.get('currency_uom_id')
        product_store_id = data.get('product_store_id')
        sales_channel_enum_id = data.get('sales_channel_enum_id')
        grand_total = data.get('grand_total')
        completed_date = data.get('completed_date')
        
        if not any([order_name, placed_date, approved_date, status_id, party_id,
                    currency_uom_id, product_store_id, sales_channel_enum_id,
                    grand_total, completed_date]):
            return {"message": "At least one field is required for update"}, 400
        
        try:
            cursor.execute("""
                UPDATE [newdatabase].[dbo].[order_header]
                SET order_name = ?,
                    placed_date = ?,
                    approved_date = ?,
                    status_id = ?,
                    party_id = ?,
                    currency_uom_id = ?,
                    product_store_id = ?,
                    sales_channel_enum_id = ?,
                    grand_total = ?,
                    completed_date = ?
                WHERE order_id = ?;
            """, order_name, placed_date, approved_date, status_id, party_id,
            currency_uom_id, product_store_id, sales_channel_enum_id,
            grand_total, completed_date, order_id)
            
            conn.commit()
            
            return {"message": "Order updated successfully"}, 200
        
        except Exception as e:
            return {"message": f"Error updating order: {str(e)}"}, 500



    def delete(self,Orderheader_Id):
        cursor.execute("DELETE FROM [newdatabase].[dbo].[order_header] WHERE order_id=?", Orderheader_Id)
        conn.commit()
        return jsonify({"message": "Order deleted successfully"})


class Product(Resource):

    def get(self):
        cursor.execute("""
            SELECT 
                [product_id],
                [party_id],
                [product_name],
                [description],
                [charge_shipping],
                [returnable]
            FROM [newdatabase].[dbo].[product];
        """)
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            try:
                record = {
                    "product_id": row[0],
                    "party_id": row[1],
                    "product_name": row[2],
                    "description": row[3],
                    "charge_shipping": row[4],
                    "returnable": row[5]
                }
                records.append(record)
            except TypeError:
                continue 
    
        return jsonify(records)
    
    def post(self):
        data = request.get_json()
        
        product_id = data.get('product_id')
        party_id = data.get('party_id')
        product_name = data.get('product_name')
        description = data.get('description')
        charge_shipping = data.get('charge_shipping')
        returnable = data.get('returnable')
        
        if not product_id:
            return {"message": "product_id is required"}, 400
        
        try:
            cursor.execute("""
                INSERT INTO [newdatabase].[dbo].[product] 
                (product_id, party_id, product_name, description, charge_shipping, returnable)
                VALUES (?, ?, ?, ?, ?, ?);
            """, product_id, party_id, product_name, description, charge_shipping, returnable)
            
            conn.commit()
            
            return {"message": "Product added successfully"}, 201
        
        except Exception as e:
            return {"message": f"Error adding product: {str(e)}"}, 500
    
    def put(self, product_id):
        data = request.get_json()
        
        party_id = data.get('party_id')
        product_name = data.get('product_name')
        description = data.get('description')
        charge_shipping = data.get('charge_shipping')
        returnable = data.get('returnable')
        

        
        try:
            cursor.execute("""
                UPDATE [newdatabase].[dbo].[product]
                SET party_id = ?,
                    product_name = ?,
                    description = ?,
                    charge_shipping = ?,
                    returnable = ?
                WHERE product_id = ?;
            """, party_id, product_name, description, charge_shipping, returnable, product_id)
            
            conn.commit()
            
            if cursor.rowcount == 0:
                return {"message": "Product not found"}, 404
            
            return {"message": "Product updated successfully"}, 200
        
        except pyodbc.IntegrityError:
            return {"message": "Duplicate product_id. Product with this product_id already exists."}, 400
        
        except Exception as e:
            return {"message": f"Error updating product: {str(e)}"}, 500
    
    def delete(self, product_id):
        cursor.execute("DELETE FROM [newdatabase].[dbo].[product] WHERE product_id=?", product_id)
        conn.commit()
        return jsonify({"message": "Product deleted successfully"})

class OrderItem(Resource):

    def get(self):
        cursor.execute("""
            SELECT 
                [order_id],
                [order_item_seq_id],
                [product_id],
                [item_description],
                [quantity],
                [unit_amount],
                [item_type_enum_id]
            FROM [newdatabase].[dbo].[order_item];
        """)
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            try:
                record = {
                    "order_id": row[0],
                    "order_item_seq_id": row[1],
                    "product_id": row[2],
                    "item_description": row[3],
                    "quantity": float(row[4]), 
                    "unit_amount": float(row[5]), 
                    "item_type_enum_id": row[6]
                }
                records.append(record)
            except TypeError:
                continue  
    
        return jsonify(records)
    
    def post(self):
        data = request.get_json()
        
        
        order_id = data.get('order_id')
        order_item_seq_id = data.get('order_item_seq_id')
        product_id = data.get('product_id')
        item_description = data.get('item_description')
        quantity = data.get('quantity')
        unit_amount = data.get('unit_amount')
        item_type_enum_id = data.get('item_type_enum_id')
        
      
        if not order_id or not order_item_seq_id:
            return {"message": "order_id and order_item_seq_id are required"}, 400
        
        try:
            cursor.execute("""
                INSERT INTO [newdatabase].[dbo].[order_item] 
                (order_id, order_item_seq_id, product_id, item_description, quantity, unit_amount, item_type_enum_id)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, order_id, order_item_seq_id, product_id, item_description, quantity, unit_amount, item_type_enum_id)
            
            conn.commit()
            
            return {"message": "Order item added successfully"}, 201
        
        except Exception as e:
            return {"message": f"Error adding order item: {str(e)}"}, 500
    
    def put(self,Order_Id):
        data = request.get_json()
        
 
       
        item_description = data.get('item_description')
        product_id = data.get('product_id')
        item_description = data.get('item_description')
        quantity = data.get('quantity')
        unit_amount = data.get('unit_amount')
        order_item_seq_id= data.get('order_item_seq_id')
        item_type_enum_id = data.get('item_type_enum_id')
        
       
        try:
            cursor.execute("""
                UPDATE [newdatabase].[dbo].[order_item]
                SET 
                    item_description = ?,
                    quantity = ?,
                    unit_amount = ?,
                    item_type_enum_id = ? ,
                    order_item_seq_id=? 
                WHERE order_id = ? AND product_id  = ?;
            """,  item_description, quantity, unit_amount, item_type_enum_id,order_item_seq_id, Order_Id, product_id)
            
            conn.commit()
            
            if cursor.rowcount == 0:
                return {"message": "Order item not found"}, 404
            
            return {"message": "Order item updated successfully"}, 200
        
        except pyodbc.IntegrityError:
            return {"message": "Duplicate order_id and order_item_seq_id. Order item with this combination already exists."}, 400
        
        except Exception as e:
            return {"message": f"Error updating order item: {str(e)}"}, 500
    
    def delete(self, order_id, order_item_seq_id):
        cursor.execute("DELETE FROM [newdatabase].[dbo].[order_item] WHERE order_id=? AND order_item_seq_id=?", order_id, order_item_seq_id)
        conn.commit()
        return jsonify({"message": "Order item deleted successfully"})


api.add_resource(Party, '/Party', '/Party/<string:party_id>')
api.add_resource(Person, '/Person', '/Person/<string:party_id>')
api.add_resource(Product, '/Product', '/Product/<string:product_id>')
api.add_resource(OrderHeader, '/Order', '/Order/<string:Orderheader_Id>')
api.add_resource(OrderItem, '/OrderItem', '/OrderItem/<string:Order_Id>')

if __name__ == '__main__':
    app.run(debug=True)
