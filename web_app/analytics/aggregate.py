'''
Created on Aug 28, 2015

@author: buck
'''

from web_app.app.models import Trace, PageLoad

def favorite(page_list):
    pages = dict()
    for p in page_list:
        if p.page_id in pages:
            pages[p.page_id] = pages[p.page_id] + 1
        else:
            pages[p.page_id] = 1
    
    max_visits = 0
    max_visit = 'index'
    for k, v in pages:
        if v > max_visits:
            max_visits = v
            max_visit = k
    
    return max_visit

def markov_forward(page_list):
    pages = dict()
    for i in range(0,len(page_list)-1):
        origin = pages[i]
        next_page = pages[i+1]
        if origin in pages:
            if next_page in pages[origin]:
                pages[origin][next_page] = pages[origin][next_page] + 1
            else:
                pages[origin][next_page] = 1
        else:
            pages[origin] = dict()
            pages[origin][next_page] = 1
        
        out = []
        for k, v in pages:
            likely_page = ''
            likely_count = 0
            for key, val in pages[v]:
                if val > likely_count:
                    likely_count = val
                    likely_page = key
                
            out.append((k, likely_page,))
        return out

def markov_backward(page_list):
    pages = dict()
    for i in range(1,len(page_list)):
        origin = pages[i]
        ref_page = pages[i-1]
        if origin in pages:
            if ref_page in pages[origin]:
                pages[origin][ref_page] = pages[origin][ref_page] + 1
            else:
                pages[origin][ref_page] = 1
        else:
            pages[origin] = dict()
            pages[origin][ref_page] = 1
        
        out = []
        for k, v in pages:
            likely_page = ''
            likely_count = 0
            for key, val in pages[v]:
                if val > likely_count:
                    likely_count = val
                    likely_page = key
                
            out.append((k, likely_page,))
        return out
# def enhance():
#     print 'enhanching Trace with analytics'
#     Trace.favorite = favorite()
#     
# enhance()