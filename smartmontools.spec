Summary:	For monitoring S.M.A.R.T. disks and devices
Name:		smartmontools
Version:	6.2
Release:	6
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	smartd.conf
Source3:	smartd.sysconfig
Source5:	%{name}.rpmlintrc
Patch0:		smartmontools-6.0-service.patch
%rename		smartsuite
Requires(post):	rpm-helper
Requires(preun):rpm-helper
BuildRequires:	systemd-units
BuildRequires:	libcap-ng-devel

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
%patch0 -p0

%build
%configure2_5x	--with-libcap-ng=yes \
		--enable-drivedb

%make

%install
%makeinstall_std

install -p -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/smartd.conf
install -p -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/sysconfig/smartd

%post
%_post_service smartd

%preun
%_preun_service smartd

%files
%config(noreplace) %{_sysconfdir}/smartd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smartd_warning.sh
%config(noreplace) %{_sysconfdir}/sysconfig/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
%{_datadir}/%{name}/drivedb.h
