nosetests \
--with-timer --timer-top-n 5 --timer-ok 250ms --timer-warning 500ms \
--with-coverage --cover-erase --cover-package=Insight --cover-html --cover-branches
# --cover-min-percentage=90
echo $?
echo "View coverage report @ file:///home/buck/Github/Insight/cover/index.html"
