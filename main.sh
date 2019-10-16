LOG=../spider.log
OUTPUT=../conversations

EMAIL="tigas@vxmail2.net"
PASSWORD="AbraKadabra"

cd facebook
if [ -f "$LOG" ]; then rm $LOG; fi
if [ -f "$OUTPUT/*.json" ]; then rm $OUTPUT/*.json; fi
scrapy crawl --logfile=$LOG conversations -a email=$EMAIL -a password=$PASSWORD
