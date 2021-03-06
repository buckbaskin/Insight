export STATUS=TESTING
echo $STATUS
nosetests \
--with-timer --timer-top-n 5 --timer-ok 250ms --timer-warning 500ms \
--with-coverage --cover-erase --cover-html --cover-package=app --cover-branches \
flaskserver/tests/ service1/tests/
# --cover-min-percentage=90
result=$?
echo "View coverage report @ file:///home/buck/Github/Insight/cover/index.html"
export STATUS=Production
if [ $result != 0 ]; then
    echo $result
    exit 1
else
    codecov
    exit 0
fi
