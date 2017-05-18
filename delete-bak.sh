#定时删除30天以上的日志文件
find /Users/liangxinxin/git2/toutiao2/social/logs -type f -mtime +30 -exec rm -f {}  \;