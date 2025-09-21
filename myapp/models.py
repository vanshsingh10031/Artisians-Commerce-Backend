
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cart(models.Model):
    cartid = models.AutoField(db_column='CartID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cart'


class Cartitems(models.Model):
    cartitemid = models.AutoField(db_column='CartItemID', primary_key=True)  # Field name made lowercase.
    cartid = models.ForeignKey(Cart, models.DO_NOTHING, db_column='CartID')  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CartItems'


class Categories(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categories'


class Orderitems(models.Model):
    orderitemid = models.AutoField(db_column='OrderItemID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orders', models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrderItems'


class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    totalamount = models.DecimalField(db_column='TotalAmount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orders'


class Payments(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Orders, models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateTimeField(db_column='PaymentDate', blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payments'


class Products(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(null=True, blank=True)  # comma-separated tags
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    imagepath = models.CharField(max_length=500, blank=True, null=True)  # stores file path or UR
    class Meta:
        db_table = 'Products'


class Reviews(models.Model):
    reviewid = models.AutoField(db_column='ReviewID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Products, models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reviews'


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='ShopName', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bio = models.TextField(db_column='Bio', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aadhaarno = models.CharField(db_column='AadhaarNo', unique=True, max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    panno = models.CharField(db_column='PANNo', unique=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'