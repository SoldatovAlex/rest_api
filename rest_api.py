import json
from setup_db import Base, engine, User, Transaction


from flask import Flask, jsonify, request, abort, Response
from flask_restful import Resource, Api


from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
api = Api(app)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def post_alchemy_serializer_user(obj):
    return {
        'id': obj.id,
        'first_name': str(obj.first_name),
        'last_name': str(obj.last_name),
        'email': str(obj.email)
    }


def post_alchemy_serializer_transaction(obj):
    return {
        'id': obj.id,
        'user_id': str(obj.user_id),
        'amount': str(obj.amount),
        'date': str(obj.date)
    }


class UserView(Resource):
    # input param is user id, in response info about user
    def get(self, id):
        if db_session.query(User).filter_by(id=id).first() is None:
            abort(400)
        return jsonify(post_alchemy_serializer_user(db_session.query(User).filter_by(id=id).first()))


    # input param is user id, if user with user id is exist - change his params. If in db user dont exist, will create new user
    def put(self, id):
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        if email is None or first_name is None or last_name is None:
            abort(400)
        if db_session.query(User).filter_by(id=id).first() is not None:
            user_obj = db_session.query(User).get(id)
            user_obj.email = email
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            db_session.commit()
            return jsonify(post_alchemy_serializer_user(db_session.query(User).filter_by(id=id).first()))
        user = User(email=email, first_name= first_name, last_name = last_name)
        db_session.add(user)
        db_session.commit()
        return 'OK, was created new user', 201


    # input param is user id, if user with user id is exist - delete him. Else response with status_code = 400, and message {'error': 'no such user'}
    def delete(self, id):
        user_obj = db_session.query(User).get(id)
        if user_obj is None:
            return Response(json.dumps({'error': 'no such user'}), status=400, mimetype='application/json')
        db_session.delete(user_obj)
        db_session.commit()
        return jsonify({'status': 'ok'})


class UserViewPost(Resource):
    # create new user. in request must be header, in body json with data. For example: {"first_name": "Michail", "last_name": "Zubenko", "email": "@gmail.com"}
    def post(self):
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        if email is None or first_name is None or last_name is None:
            abort(400)
        user = User(email=email, first_name= first_name, last_name = last_name)
        db_session.add(user)
        db_session.commit()
        return 'OK', 201


class TransactionView(Resource):
    # input param is transaction id, in response info about transaction
    def get(self, id):
        if db_session.query(Transaction).filter_by(id=id).first() is None:
            abort(400)
        return jsonify(post_alchemy_serializer_transaction(db_session.query(Transaction).filter_by(id=id).first()))


    # input param is transaction id, if transaction with transaction id is exist - change his params. If in db transaction dont exist, will create new transaction
    def put(self, id):
        user_id = request.json.get('user_id')
        amount = request.json.get('amount')

        if user_id is None or amount is None:
            abort(400)
        if db_session.query(Transaction).filter_by(id=id).first() is not None:
            transaction_obj = db_session.query(Transaction).get(id)
            transaction_obj.user_id = user_id
            transaction_obj.amount = amount
            db_session.commit()
            return jsonify(post_alchemy_serializer_transaction(db_session.query(Transaction).filter_by(id=id).first()))
        transaction = Transaction(user_id=user_id, amount=amount)
        db_session.add(transaction)
        db_session.commit()
        return 'OK, was created new transaction', 201

    # input param is transaction id, if transaction with id is exist - delete him. Else response with status_code = 400, and message {'error': 'no such transaction'}
    def delete(self, id):
        transaction_obj = db_session.query(Transaction).get(id)
        if transaction_obj is None:
            return Response(json.dumps({'error': 'no such transaction'}), status=400,  mimetype='application/json')
        db_session.delete(transaction_obj)
        db_session.commit()
        return jsonify({'status': 'ok'})


class TransactionViewPost(Resource):
    # create new transaction. in request must be header, in body json with data. For example: {"user_id": "3", "amount": "500"}
    # if it outcome transaction enter amount with '-'. if income just enter number.
    # For example: {"user_id": "3", "amount": "500"} - income transaction
    # For example: {"user_id": "3", "amount": "-500"} - outcome transaction
    def post(self):
        user_id = request.json.get('user_id')
        amount = request.json.get('amount')

        if user_id is None or amount is None:
            abort(400)
        transaction = Transaction(user_id=user_id, amount=amount)
        db_session.add(transaction)
        db_session.commit()
        return 'OK', 201


api.add_resource(UserView, '/user/<int:id>', endpoint='UserView')
api.add_resource(UserViewPost, '/user', endpoint='UserViewPost')
api.add_resource(TransactionView, '/transaction/<int:id>', endpoint='TransactionView')
api.add_resource(TransactionViewPost, '/transaction', endpoint='TransactionViewPost')


@app.route('/userstransaction/<int:user_id>', methods=['GET'])
# input param is user id, in response all users transaction
def users_transaction(user_id):
    if user_id is None:
        abort(400)
    if db_session.query(Transaction).filter_by(user_id=user_id).first() is None:
        return jsonify({'error': 'no such user_id'}), 404
    return jsonify([post_alchemy_serializer_transaction(trans) for trans in db_session.query(Transaction).filter_by(user_id=user_id).all()])


@app.route('/sumbydate/<int:user_id>', methods=['GET'])
# input param is user id, in response  sum all users transactions group by date. This method can helps understand, day was with posite or negative balance.
def group_by_date(user_id):
    if user_id is None:
        abort(400)
    if db_session.query(Transaction).filter_by(user_id=user_id).first() is None:
        return jsonify({'error': 'no such user_id'}), 404
    dates = list(set([trans.date for trans in db_session.query(Transaction).filter_by(user_id=user_id).all()]))
    total = []
    for date in dates:
        day_amount = [int(trans.amount) for trans in db_session.query(Transaction).filter_by(date=date).all()]
        total.append(sum(day_amount))
    return json.dumps([{str(dates[i]): total[i]} for i in range(len(dates))])


@app.route('/transactiontype/<int:id>', methods=['GET'])
# input param is transaction id, in response type of transaction
def define_transaction_type(id):
    if db_session.query(Transaction).filter_by(id=id).first() is None:
        return jsonify({'error': 'no such transaction_id'}), 404
    transaction = db_session.query(Transaction).filter_by(id=id).first()
    try:
        int_value = int(transaction.amount)
        if int_value > 0:
            return jsonify({'transaction type': 'income'})
        else:
            return jsonify({'transaction type': 'outcome'})
    except:
        return jsonify({'error': 'incorrect amount'}), 409


@app.route('/transactionamountsort/<int:user_id>', methods=['GET'])
# input param is user id, in response all users transactions sorted
def user_trans_amount_sort(user_id):
    if user_id is None:
        abort(400)
    if db_session.query(Transaction).filter_by(user_id=user_id).first() is None:
        return jsonify({'error': 'no such user_id'}), 404
    all_trans = db_session.query(Transaction).filter_by(user_id=user_id).order_by(Transaction.amount).all()
    return jsonify([post_alchemy_serializer_transaction(trans) for trans in all_trans])


if __name__ == '__main__':
    app.run(debug=True, port=8000)