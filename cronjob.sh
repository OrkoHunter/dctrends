export DISPLAY=:0.0
if (( kill $(ps aux | grep '[x]fce4-terminal -e' | awk '{print $2}') )); then
	python3 /home/hunter/workspace/dctrends/move_logs.py
	rm /home/hunter/.ncdc/stderr.log
	cd /home/hunter/workspace/dctrends
	git add -A
	git commit -m "Update"
	git push origin master
	/usr/bin/xfce4-terminal -e "/home/hunter/workspace/ncdc" &
fi
