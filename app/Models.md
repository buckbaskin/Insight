# Models for Insight

## Twitter

###User
	id
	#### Site Info
	tracking
	last_updated
	
	#### Twitter Info
	t_screen_name (index, unique)
	statuses (relationship to Status)
	contributors
	created_at
	description
	favorites_count
	followers_count
	friends_count
	t_id
	name
	statuses_count
	verified
	profile_url
	followed (relationship thru table to User)
	
	#### + methods
	
### Status
	id
	
	#### Twitter Info
	hashtags (relationship thru table to Hashtag)
	mentions (relationship thru table to User)
	in_reply_to (relationship to Status)
	t_id
	text
	created_at
	user_id (foreignKey to User)

### Hashtag
	text (is id)
	
## Site

### Trace
	id
	start
	pages
	
	#### + methods
	
### PageLoad
	id
	time
	page_id
	trace_id (foreignKey to Trace)

## Redis

### Result (example)
	__tablename__
	id
	url
	result_all (JSON)
	result_no_stop_words (JSON)
	
	#### + methods