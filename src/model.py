from src import db
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(), nullable=False)    
    lastname = db.Column(db.String(), nullable=False)    
    phone_number = db.Column(db.String(), unique=True, nullable=False)    
    email = db.Column(db.String(), unique=True, nullable=False)    
    password = db.Column(db.String(), nullable=False)    
    is_login = db.Column(db.Boolean, nullable=False, default=True)    
    is_deactivate = db.Column(db.Boolean, nullable=False, default=False)    
    created_at = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())
    role = db.Column(db.String(), default="guest")    

    __table_args__ = (
        db.CheckConstraint(role.in_(['guest', 'admin']), name='role_types'),      
    )

    def get_by_email(email):        
        db_user = User.query.filter(User.email == email).first()
        return db_user

    def __repr__(self):
        return f"<User {self.email}>"
    
class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(), nullable=False)    
    bank_name = db.Column(db.String(), nullable=False)    
    account_balance = db.Column(db.Float(), nullable=False)    
    user_id = db.Column(db.Integer, nullable=False)    
    created_at = db.Column(db.Date, nullable=False,default=datetime.datetime.utcnow())
    updated_at = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())


    def __init__(self,account_number, bank_name, account_balance, user_id):
        self.account_balance = account_balance
        self.bank_name= bank_name
        self.account_number =account_number
        self.user_id=user_id
    
    def get_account_balance(self, user_id, id):
        get_account_balance = Account.query.filter([Account.user_id==user_id, Account.id==id]).first
        return get_account_balance.account_balance
    

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.String(), unique=False, nullable=False)    
    description = db.Column(db.String(), nullable=False)    
    transaction_ref = db.Column(db.String(), nullable=False)    
    user_ip = db.Column(db.String(), nullable=True)
    timezone = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)
    transaction_type = db.Column(db.String(), nullable=True, default="debit")
    status = db.Column(db.String(), nullable=False, default="pending")
    account_id = db.Column(db.Integer, nullable=False)    
    created_at = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())
    
    def transactions(self, transaction_id):        
        db_user = Transaction.query.filter(Transaction.id == transaction_id).all()
        if not db_user:
            db.session.add(self)
            db.session.commit()
        
        return True