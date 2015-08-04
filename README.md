# The Insight Project

## Phase 1: Individual Characterization

### Follower Structure
 - Analyze the way that the user has followed other users to find patterns in their current search for relevant tweets
   - Build a tree based on the order and connections of accounts the user follows
   - Ex. A follows B, and {user} follows both. B was followed first. This results in a tree like: {user} <-- A <-- B
   - Ex. A doesn't follow B, otherwise the same. This results in a tree like: A --> {user} <-- B

### Content Consumption
 - Analyze active times by day and time of day
 - Tie in correlations to content that the user engaged with relative to their average feed
 - Measure successful consumption, interest in topics by retweets, favorites, replies and other engagements

### Content Creation
 - Analyze actives times by day and time of day
 - Tie in correlations to content created in specific time periods relative to their average content
 - Measure output by tweets and retweets by topic, etc.
 - Success is measured by downstream engagement of the followers
 
## Phase 2: Network Characterization

### Merged Content Creation and Consumption
 - Identify successful pairs of content creation (friends) and content consumption (user) or creation (by the user) and consumption (followers).
 - Use this model to find accounts that the user should engage best with based on timing, content, etc.
 
## Phase 3: Bi-directional Recommendation

### For Content Consumption Focused Users
 - Recommendation 1: Find accounts where the quantified content creation profile matches the profile of content creators that the user engaged most with
 - Recommendation 2: Find content consumers that are quantified to be similar, and then add their highest engaging creators to the recommendation. This is more standard collaborative filtering
 - Recommendation Methods: Different ways of looking for similar users.
   - Note: The method needs to be efficient when it comes to finding users in terms of API calls, or perhaps leverage the Streaming API.
   - This would likely be achieved by implementing a k-nearest neighbors search in a normalized search space based on the quantified user information
   - Another implementation that I would be interested in looking into is a neural network that takes two users as inputs and returns an estimate of similarity from 0 to 1
   - A third method would be to use supervised learning to learn what kinds of users are similar, with labeling by exploring and offering two users and then a binary yes or no if they are similar

### For Content Creation Focused Users
 - Recommendation 1: Find users that engage the same way with content that the user's most active followers engage. See above methods.
 - Recommendation 2: Find content creators that are similar, and look to attract users that they are engaging well with. See above methods.
 - Recommendation 3: Find users with a follow tree that is accessible (recently expanded, with long branches to indicate interest). Then tailor content creation to attract that user
 - Recommendation 4: Recommend content creation topics and timing to optimize current follower response
 - Recommendation 5: Recommend content creation topics and timing to optimize second level follower response based on the retweet rates of content by followers