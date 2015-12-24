#firefox &
WID=`xdotool search --title "Mozilla Firefox" | head -1`
xdotool windowfocus $WID
xdotool key ctrl+t
url="http://my.ebay.com/ws/eBayISAPI.dll?MyEbayBeta&CurrentPage=LabelManagement"
xdotool type $url
xdotool key "Return"
sleep 2
xdotool key ctrl+s
WID=`xdotool search --title "Save As" | head -1`
sleep 0.5
xdotool key "Return"
sleep 0.5
xdotool key "Return"

#http://xmodulo.com/simulate-key-press-mouse-movement-linux.html
