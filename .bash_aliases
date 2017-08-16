test -r ~/.private && source ~/.private

test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
alias ls='ls --color=auto'
alias l='ls'
alias ll='ls -l'
alias la='ls -a'
alias lla='ls -la'

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ..2="cd ../.."
alias ..3="cd ../../.."
alias ..4="cd ../../../.."
alias ..5="cd ../../../../.."

alias g='git'
alias s='sudo'
alias gdb='gdb --quiet' # suppress the introductory and copyright messages
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

alias pastebinit='pastebinit -b https://paste.akawolf.org -a akaWolf'

# Compress the cd, ls -l series of commands.
function cl() {
	if [ $# = 0 ]; then
		cd && ll
	else
		cd "$*" && ll
	fi
}

# Upload files
function up()
{
	if [[ $1 == *.* ]]; then
		ext=.$(echo $1 | cut -d . -f 2)
	else
		ext=""
	fi
	name=$(basename "$1")
	curl --silent -b "uid=1; identifier=$BINIDENT" -F "file=@$1" -F "filename=$name" -F "api=1" https://bin.akawolf.org/u | awk "{print \"https://bin.akawolf.org/f/\"\$2\"$ext\"}"
}

# Paste files
function p()
{
	for last; do true; done
	name=$(basename "$last")
	pastebinit -t $name $@
}

# Compare md5 sum
function md5comp
{
	shopt -s nocasematch
	if [[ $(md5sum "$1") = $2* ]]; then
		echo "OK"
	else
		echo "FAIL"
	fi
}

# awk calculator (remember to quote arguments if they contain parentheses)
function c
{
	awk "BEGIN{ pi=4.0*atan2(1.0,1.0); deg=pi/180.0; print $* }";
}

# hex to bin
function h2b
{
	arg=$(echo "$1" | awk '{print toupper($0)}')
	echo "obase=2; ibase=16; $arg" | bc
}

# bin to hex
function b2h
{
	echo "obase=16; ibase=2; $1" | bc
}

# hex to dec
function h2d
{
	arg=$(echo "$1" | awk '{print toupper($0)}')
	echo "obase=10; ibase=16; $arg" | bc
}

# dec to hex
function d2h
{
	arg=$(echo "$1" | awk '{print toupper($0)}')
	echo "obase=16; ibase=10; $arg" | bc
}

# generate password: genpasswd [pass len]
genpasswd() {
	local len="$1"
	test "$len" == "" && len=8
	tr -dc "A-Za-z0-9" < /dev/urandom | head -c "$len"; printf "\n"
}

# Add an "alert" alias for long running commands. Use like so: sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
