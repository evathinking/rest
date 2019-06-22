#!/bin/sh


ps -ef | grep "btc/Run.py" | grep -v "grep"

if [ $? -eq 0  ]

then
echo "$?"
echo "gateio process already started!"

else

echo "$?"
python /home/ubuntu/Gateio/btc/Run.py & #启动应用，修改成自己的启动应用脚本或命令
echo "gateio process has been restarted!"

fi
