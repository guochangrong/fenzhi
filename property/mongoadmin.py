# import the MongoAdmin base class
from mongonaut.sites import MongoAdmin
###import your custom models###
# from property.models import Employee
from property.models import Question
# instantiate the MongoAdmin class
# Then attach the mongoadmin to your model
# Employee.mongoadmin = MongoAdmin()
Question.mongoadmin = MongoAdmin()
