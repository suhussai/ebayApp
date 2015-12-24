i="0"

while [ $i -lt 1 ]
do
file_date=$(ls -l ../ | grep 'My eBay.html' | awk '// {print$8}')
cur_date=$(date +"%H:%M")
echo $file_date
echo $cur_date
if [ "$file_date" == "$cur_date" ]; then
	echo "good"
	mv ../My\ eBay.html .
	i="2"
else
	bash getPage.sh
	sleep 5 
fi
done

