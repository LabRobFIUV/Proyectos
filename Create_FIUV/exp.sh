ip=`hostname -I`
ip="$(echo "$ip" | tr -d ' ')"
echo $ip
export ROS_IP=$ip
export ROS_MASTER_URI=http://$ip:11311
