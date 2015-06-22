from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

class Word(Node):
       
    element_type = "word"
    
    name = String(nullable=False)
    
       

class RelatesTo(Relationship):

    label = "relatesTo"
    
    created = DateTime(default=current_datetime, nullable=False)
    tests = Integer(nullable=False)
    occurences = Integer(nullable=False)