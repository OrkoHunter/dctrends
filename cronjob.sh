if (( kill $(ps aux | grep '[x]fce4-terminal -e' | awk '{print $2}') )); then
	python3 /home/hunter/workspace/dctrends/move_logs.py
	rm /home/hunter/.ncdc/stderr.log
fi

xfce4-terminal -e "/home/hunter/workspace/ncdc" &
