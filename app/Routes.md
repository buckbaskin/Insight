# Views for Insight
# Views is routes

- Home page (network canvas, search user) '/<int:trace>'

- User view (view profile) '/u/<int:id>/<int:trace>'
- Create user (create profile) '/u/new/<int:trace>'

- Queue Status '/q/<int:trace>'
- Site Analytics (all information collected, after everything else working) '/a/<int:trace>'

## Redirects
'/index' -> '/'
'/user/...' -> '/u/...'
'/user/new' -> '/u/new'
'/analytics' -> '/a'

## API endpoints (for Angular to get Data)