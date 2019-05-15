sudo apt-get install gpgv2 autoconf bison build-essential curl git-core libapr1 libaprutil1 libcurl4-openssl-dev libgmp3-dev libpcap-dev libpq-dev libreadline6-dev libsqlite3-dev libssl-dev libsvn1 libtool libxml2 libxml2-dev libxslt-dev libyaml-dev locate ncurses-dev openssl postgresql postgresql-contrib wget xsel zlib1g zlib1g-dev -y

echo "Type The following : "
echo "createuser msfuser -S -R -P"
echo "createdb msfdb -O msfuser"
echo "exit"
sleep 2
sudo su postgres
sudo update-rc.d postgresql enable
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -sSL https://get.rvm.io | bash -s stable --ruby
source ~/.rvm/scripts/rvm
git clone https://github.com/rapid7/metasploit-framework.git
cd metasploit-framework/
apt install ruby -y
rvm --install .ruby-version
echo "Installing nokogiri..."
sleep 2
sudo apt-get install build-essential patch ruby-dev zlib1g-dev liblzma-dev -y
gem install nokogiri
gem install bundler
bundle install
clear
echo "Metasploit Installed!"
echo "Starting metasploit..."
sleep 2
./msfconsole
