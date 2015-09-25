from app import db
from app.models import User, FollowTree, FollowTreeNode
from insight_apis.twitter_access import TwitterManager
from insight_apis.twitter_access import initialize as initialize_twitter

def collect_friends(t_screen_name):
    # Query twitter for the followers of this user
    # make sure that it is compliant with rate limits
    
    # in twitter speak:
    # a user is followed by "followers"
    # a user follows their "friends"
    # In this case, we are trying to find all of the people that a user follows (friends)
    #  and then construct a tree of friends where each edge points from a follower to it's friend 
    api = initialize_twitter().get_api()
    # example
    print 'xxx ' + str(api.uriparts)
    if len(api.uriparts) > 1:
        api.uriparts = (api.uriparts[0],)
    print 'yyy ' + str(api.uriparts)
    # comment
    result = api.friends.ids(screen_name=t_screen_name, count=5000)
    friends = result['ids']
    while result['next_cursor']:
        result = api.friends.ids(screen_name=t_screen_name, count=5000, cursor=result['next_cursor'])
        friends.extend(result['ids'])
    print 'found ' + str(len(friends)) + ' friends'
    # TODO(buckbaskin): save to db
    return friends

def aggregate_followers(t_screen_name):
    # For all followers of given t_screen_name
    # Create a tree modeling the rough order that the user found them
    # Allows analysis to determine interest of the user
    user = User.query.filter_by(t_screen_name=t_screen_name).first() # @UndefinedVariable
    existing_tree = FollowTree.query.filter_by(user_id=user.id).first() # @UndefinedVariable
    
    if existing_tree:
        tree = existing_tree
    else:
        tree = FollowTree(t_screen_name)
        db.session.add(tree)
        db.session.commit()
        
    followers = user.followers
    existing_roots = FollowTreeNode.query.filter_by(tree=tree.id).filter_by(parent=None).all() # @UndefinedVariable
    
    max_in_session = 10
    
    for follower in followers:
        existing_node = FollowTreeNode.query.filter_by(tree=tree.id).filter_by(user_id=follower.id).first() # @UndefinedVariable
        if existing_node:
            # do not move/do anything to a node if it is already in the tree
            pass
        else:
            # create a new node for that user/follower
            node = FollowTreeNode(tree=tree.id, user=follower.id)
            db.session.add(node)
            max_in_session = max_in_session - 1
            
            # point all existing roots (by parent) to this new node if they follow the node
            
            i = 0
            while (i < len(existing_roots)):
                root_node = existing_roots[i]
                if root_node.is_following(node.user_id):
                    root_node.parent = node.id
                    db.session.add(node)
                    max_in_session = max_in_session - 1
                    del existing_roots[i]
                else:
                    i = i + 1
                
            # add the new node as a root
            existing_roots.append(node)
            
            # if 10 or more changes need to be committed, commit changed to db
            # this is done to reduce the number of database writes. It may make sense to commit after every one if this is a problem
            if max_in_session <= 0:
                db.session.commit()
                max_in_session = 10
    # push all outstanding changes to db          
    db.session.commit()
    
    return True