import sys
sys.path.append('/home/buck/Github/Insight')

from insight_apis import twitter_access
import follow_tree

process_friends = follow_tree.tasks.process_friends