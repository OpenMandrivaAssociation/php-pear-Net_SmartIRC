%define		_class		Net
%define		_subclass	SmartIRC
%define		_status		stable
%define		_pearname	%{_class}_%{_subclass}

%define		_requires_exceptions pear(../SmartIRC.php)

Summary:	%{_pearname} - IRC client class
Name:		php-pear-%{_pearname}
Version:	0.5.5p1
Release:	%mkrel 8
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
Patch0:		%{name}-fix_includes.patch
URL:		http://pear.php.net/package/Net_SmartIRC/	
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Net_SmartIRC is a PHP class for communication with IRC networks, which
conforms to the RFC 2812 (IRC protocol). It's an API that handles all
IRC protocol messages. This class is designed for creating IRC bots,
chats and show irc related info on webpages.

Featurelist:
- actionhandler for the API
- messagehandler for the API
- send/receive floodprotection
- detects and changes nickname on nickname collisions
- time events
- full object oriented programmed
- autoreconnect
- debugging/logging system
- supports fsocks and PHP socket extension
- supports PHP 4.1.x to 4.3.0
- sendbuffer with priority levels
- channel synching (tracking of users/modes/topic etc in variables)
- IRC functions: op, deop, voice, devoice, ban, unban, join, part,
  action, message, query, ctcp, mode, topic, nick, invite

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U
%patch0 -p0

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}
install %{_pearname}-%{version}/SmartIRC/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/{CHANGELOG,CREDITS,FEATURES,LICENSE,README,docs,examples}
%dir %{_datadir}/pear/%{_class}/%{_subclass}
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/*.php

%{_datadir}/pear/packages/%{_pearname}.xml


