'''
Created on Aug 27, 2015

@author: buck
'''

from web_app.app import models
from web_app.app.models import PageLoad
# from sqlalchemy import desc

trace_id = 37

session = models.Trace.query.get(trace_id) # @UndefinedVariable
page_loads = models.PageLoad.query.filter_by(trace_id=trace_id).order_by(PageLoad.time).all() # @UndefinedVariable
print 'page_loads from trace '+str(session)
for page in page_loads:
    print page.time.strftime('%I:%M.%S %m/%d/%Y')+' '+str(page.page_id)