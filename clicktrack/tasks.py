'''
Define tasks for an async job queue to use for tracking clicks, etc.
'''

def mouse_move(user_id, path, track_type, scroll_x, scroll_y,
               mouse_x, mouse_y, time):
    print('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
          (path, user_id, track_type, scroll_x, scroll_y, 
           mouse_x, mouse_y, time,))
    return ('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
            (path, user_id, track_type, scroll_x, scroll_y, 
             mouse_x, mouse_y, time,))

def page_load(user_id, path, screen_x, screen_y, window_x, window_y):
    print('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
          (path, user_id, track_type, scroll_x, scroll_y, 
           mouse_x, mouse_y, time,))
    return ('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
            (path, user_id, track_type, scroll_x, scroll_y, 
             mouse_x, mouse_y, time,))

