nosetests \
--with-timer --timer-top-n 5 --timer-ok 250ms --timer-warning 500ms \
--with-coverage --cover-erase --cover-package=Insight --cover-html --cover-branches
# --cover-min-percentage=90
result=$?
echo "View coverage report @ file:///home/buck/Github/Insight/cover/index.html"
if [ $result != 0 ]; then
    echo $result
    exit 1
else
    exit 0
fi
