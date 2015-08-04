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