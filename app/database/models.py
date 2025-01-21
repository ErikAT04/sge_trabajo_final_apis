from app.database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Boolean, DateTime, Double
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base

class User(Base):
    __tablename__="user"
    email = Column(VARCHAR(255), primary_key=True)
    username = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    image = Column(VARCHAR(255))
    payments = relationship('Payment', secondary='user_payment', back_populates="users")
    groups = relationship('Group', secondary='user_group', back_populates="users")
    notifications = relationship('Notification', backref="user", cascade="delete,merge")


class Group(Base):
    __tablename__="group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(VARCHAR(255))
    image = Column(VARCHAR(255))
    users = relationship('User', secondary='user_group', back_populates="groups")
    sent_notifs = relationship("Notification", backref="group")
    payments = relationship("Payment", backref="group")


class UserGroup(Base):
    __tablename__="user_group"
    user_email = Column(VARCHAR(255), ForeignKey('user.email', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    group_id = Column(VARCHAR(255), ForeignKey('group.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    debt = Column(Double)


class Notification(Base):
    __tablename__="notification"
    notif_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(VARCHAR(255), ForeignKey('user.email', ondelete="CASCADE", onupdate="CASCADE"))
    group_id = Column(VARCHAR(255), ForeignKey('group.id', ondelete="CASCADE", onupdate="CASCADE"))
    notif_date = Column(DateTime)


class Payment(Base):
    __tablename__="payment"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    payer_email = Column(VARCHAR(255), ForeignKey('user.email', ondelete="CASCADE", onupdate="CASCADE"))
    group_id = Column(VARCHAR(255), ForeignKey('group.id', ondelete="CASCADE", onupdate="CASCADE"))
    payment_date = Column(DateTime)
    payment_args = Column(VARCHAR(255))
    users = relationship('User', secondary='user_payment', back_populates="payments")
    


class UserPayment(Base):
    __tablename__="user_payment"
    payment_id = Column(Integer, ForeignKey('payment.payment_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_email = Column(Integer, ForeignKey('user.email', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    quantity = Column(Double)