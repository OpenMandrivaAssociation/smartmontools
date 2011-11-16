Summary:	For monitoring S.M.A.R.T. disks and devices
Name:           smartmontools
Version:        5.42
Release:        %mkrel 1
License:	GPL
Group:		System/Kernel and hardware
URL:		http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	smartd.conf
Source2:	smartd.init
Source3:	smartd.sysconfig
Obsoletes:	smartsuite
Provides:	smartsuite
Requires(post):	rpm-helper
Requires(preun): rpm-helper
BuildRequires:	libcap-ng-devel
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

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}

%makeinstall_std

install %{SOURCE1} %{buildroot}%{_sysconfdir}/
install %{SOURCE2} %{buildroot}%{_initrddir}/smartd
install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/smartd

%post
%_post_service smartd

%preun
%_preun_service smartd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/smartd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smartd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
%{_datadir}/%{name}/drivedb.h
/lib/systemd/system/smartd.service
