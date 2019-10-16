LOG=../spider.log
OUTPUT=../conversations

EMAIL="marepoli@imailpro.net"
PASSWORD="abrakadabra"

cd facebook
if [ -f "$LOG" ]; then rm $LOG; fi
if [ "$(ls $OUTPUT | grep .json)" ]; then rm $OUTPUT/*.json; fi
scrapy crawl --logfile=$LOG conversations -a email=$EMAIL -a password=$PASSWORD
