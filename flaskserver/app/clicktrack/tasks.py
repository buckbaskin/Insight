'''
Define tasks for an async job queue to use for tracking clicks, etc.
'''

def mouse_move(user_id, path, scroll_x, scroll_y,
               mouse_x, mouse_y, time):
    track_type = 'move'
    print('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
          (path, user_id, track_type, scroll_x, scroll_y, 
           mouse_x, mouse_y, time,))
    return ('click: on page %s u %d %s (%d, %d (%d, %d)) at time %d' % 
            (path, user_id, track_type, scroll_x, scroll_y, 
             mouse_x, mouse_y, time,))

def page_load(user_id, path, screen_x, screen_y, window_x, window_y, window_w, window_h):
    print('load: on page %s u %d screen size (%d, %d)' % (path, user_id, screen_x, screen_y,)) 
    return ('load: on page %s u %d screen size (%d, %d)' % (path, user_id, screen_x, screen_y,))

