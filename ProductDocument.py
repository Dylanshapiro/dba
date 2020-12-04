from pymongo import MongoClient
from decimal import Decimal

import random

class Product:
    def __init__(self,_id=None, products_name=None,products_price=None, products_stock=None,products_description=None,products_restock_level=None, products_category=None, products_sale_flag=None):
        
        if _id is not None:
            self._id = _id 
        if products_name is not None:
            self.products_name = products_name
        if products_price is not None:
            self.products_price = products_price
        if products_stock is not None: 
            self.products_stock = products_stock
        if products_description is not None:
            self.products_description = products_description
        if products_restock_level is not None:
            self.products_restock_level = products_restock_level
        if products_category is not None:
            self.products_category =products_category
        if products_sale_flag is not None:
            self.products_sale_flag = products_sale_flag

    def documentToProduct(self,product):
        return Product(**product)

    def printObj(self):
        print("BeginObject:~~~~~~~~~~~~~~")
        print(self.__dict__)
        print("EndObject:~~~~~~~~~~~~~~")

    def QueryPrintFromDatabase(self):
        print("BeginprintFromDatabase:~~~~~~~~~~~~~~")
        client = MongoClient('mongodb://127.0.0.1:27017/')
        mydb = client["AMAZON"]
        mycol = mydb["Products"]
        try:
            mydoc = mycol.find(self.__dict__)
        except TypeError as te:
            print("issue looking up : {0}, Error Thrown : {1} ".format(self.__dict__,te))
        for doc in mydoc:
            print(doc)
        print("EndprintFromDatabase:~~~~~~~~~~~~~~")

    def updateProductDocument(self,products_name=None,products_price=None, products_stock=None,products_description=None,products_restock_level=None, products_category=None, products_sale_flag=None):
        client = MongoClient('mongodb://127.0.0.1:27017/')
        mydb = client["AMAZON"]
        mycol = mydb["Products"]
        try:
            if self._id is not None:
                pass
        except:
            result = self.getDocumentProductFromDB()
            pass
        if result == None:
            return None
        myquery = self.__dict__
        p=Product(_id=None,products_name=products_name,products_price=products_price, products_stock=products_stock,products_description=products_description,products_restock_level=products_restock_level, products_category=products_category, products_sale_flag=products_sale_flag)
        newvalues= p.__dict__
        mycol.find_one_and_update(myquery,{"$set":newvalues},upsert=True)
        self.updateProductObj(products_name=products_name,products_price=products_price, products_stock=products_stock,products_description=products_description,products_restock_level=products_restock_level, products_category=products_category, products_sale_flag=products_sale_flag)
        return self

    def updateProductObj(self,_id=None,products_name=None,products_price=None, products_stock=None,products_description=None,products_restock_level=None, products_category=None, products_sale_flag=None):
        if products_name is not None:
            self._id= _id
        if products_name is not None:
            self.products_name = products_name
        if products_price is not None:
            self.products_price = products_price
        if products_stock is not None: 
            self.products_stock = products_stock
        if products_description is not None:
            self.products_description = products_description
        if products_restock_level is not None:
            self.products_restock_level = products_restock_level
        if products_category is not None:
            self.products_category =products_category
        if products_sale_flag is not None:
            self.products_sale_flag = products_sale_flag

    def insertDocumentIntoDB(self):
        client = MongoClient('mongodb://127.0.0.1:27017/')
        mydb = client["AMAZON"]
        mycol = mydb["Products"]
        mycol.insert_one(self.__dict__)

    def getDocumentProductFromDB(self):
        client = MongoClient('mongodb://127.0.0.1:27017/')
        mydb = client["AMAZON"]
        mycol = mydb["Products"]
        myfields = self.__dict__
        try:
            mydoc = mycol.find(myfields)
        except TypeError as te:
            print("issue looking up : {0}, Error Thrown : {1} ".format(self.__dict__,te))
        count =0
        docs =[]

        for doc in mydoc:
            count +=1
            docs.append(doc)
        if count ==1:
            product = docs[0]
            self.updateProductObj(**product)
            return self
        return None


class ProductTable():

    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.mydb = self.client["AMAZON"]
        self.mycol = self.mydb["Products"]
    
    def printProductTable(self):     
        for product in self.mycol.find(): 
            print(product)

    def populatetolist(self, products_names, filename):
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        # Strips the newline character 
        for productname in Lines: 
            products_names.append(productname.rstrip())
        file1.close()

    def createProductList(self,productList,products_names,products_descriptions,products_categorys):
        for product in products_names:
            productList.append(Product(products_name=product,products_price=float(format(random.uniform(0.1,1000.0),'.2f')),products_stock=random.randint(0,1000),products_description=random.choice(products_descriptions), products_restock_level=random.randint(0,10),products_category=random.choice(products_categorys), products_sale_flag=random.randint(0,1)))

    def createProductTable(self):
        products_names = []
        self.populatetolist(products_names,'productNames.txt')

        products_descriptions = ['generic description 1', 'generic description 2']

        products_categorys = []
        self.populatetolist(products_categorys,'productCategorys.txt')
        productList = []
        self.createProductList(productList,products_names,products_descriptions,products_categorys)

        self.mycol.drop()

        for product in productList:
            product.insertDocumentIntoDB()
