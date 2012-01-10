Summary:	For monitoring S.M.A.R.T. disks and devices
Name:		smartmontools
Version:	5.42
Release:	%mkrel 2
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	smartd.conf
Source2:	smartd.service
Source3:	smartd.sysconfig
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post):	systemd-sysv
BuildRequires:	libcap-ng-devel
BuildRequires:	systemd-units
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
SMARTmontools controls and monitors storage devices using the Self-Monitoring,
Analysis and Reporting Technology System (S.M.A.R.T.) built into ATA and SCSI
Hard Drives. This is used to check the reliability of the hard drive and
predict drive failures. The suite contains two utilities. The first, smartctl,
is a command-line utility designed to perform simple S.M.A.R.T. tasks. The
second, smartd, is a daemon that periodically monitors smart status and
reports errors to syslog. The package is compatible with the ATA/ATAPI-5
specification. Future releases will be compatible with the ATA/ATAPI-6 and
ATA/ATAPI-7 specifications. The package is intended to incorporate as much
"vendor specific" and "reserved" information as possible about disk drives.
man smartctl and man smartd will provide more information.

%prep

%setup -q

%build
%configure2_5x \
    --with-libcap-ng=yes \
    --enable-drivedb

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

%makeinstall_std

install %{SOURCE1} %{buildroot}%{_sysconfdir}/
install %{SOURCE2} %{buildroot}%{_unitdir}/smartd.service
install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/smartd

# cleanup
rm -rf %{buildroot}%{_initrddir}

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable smartd.service >/dev/null 2>&1 || :
    /bin/systemctl stop smartd.service > /dev/null 2>&1 || :
fi

%post
if [ $1 -eq 1 ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
else
    if [ -n "$(find /etc/rc.d/rc5.d/ -name 'S??smartd' 2>/dev/null)" ]; then
	/bin/systemctl enable smartd.service >/dev/null 2>&1 || :
    fi
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart smartd.service >/dev/null 2>&1 || :
fi

%triggerun -- smartmontools < 5.42-1
# Save the current service runlevel info
# User must manually run 
#  systemd-sysv-convert --apply smartd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save smartd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del smartd >/dev/null 2>&1 || :
/bin/systemctl try-restart smartd.service >/dev/null 2>&1 || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smartd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
%{_datadir}/%{name}/drivedb.h
%{_unitdir}/smartd.service
