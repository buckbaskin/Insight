'''
Define tasks for an async job queue to use for tracking clicks, etc.
'''

def mouse_move(user_id, path, track_type, mouse_x, mouse_y, time):
    print('%s %s %s %s' % (type(user_id), type(mouse_x), type(mouse_y), type(time),))
    print('click: on page %s u %d %s (%d, %d) at time %d' % 
          (path, user_id, track_type, mouse_x, mouse_y, time,))
    return ('click: on page %s u %d %s (%d, %d) at time %d' % 
            (path, user_id, track_type, mouse_x, mouse_y, time,))
