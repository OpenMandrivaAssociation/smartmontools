%define name smartmontools
%define version 5.38
%define release %mkrel 4

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	SMARTmontools - for monitoring S.M.A.R.T. disks and devices
License:	GPL
Group:		System/Kernel and hardware
URL:            http://smartmontools.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source2:	smartd.conf
Source4:	readme.urpmi.%{name}
Obsoletes:	smartsuite
Provides:	smartsuite
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description 
SMARTmontools controls and monitors storage devices using the
Self-Monitoring, Analysis and Reporting Technology System (S.M.A.R.T.)
built into ATA and SCSI Hard Drives. This is used to check the
reliability of the hard drive and predict drive failures. The suite
contains two utilities.  The first, smartctl, is a command-line
utility designed to perform simple S.M.A.R.T. tasks. The second,
smartd, is a daemon that periodically monitors smart status and
reports errors to syslog.  The package is compatible with the
ATA/ATAPI-5 specification.  Future releases will be compatible with
the ATA/ATAPI-6 and ATA/ATAPI-7 specifications.  The package is
intended to incorporate as much "vendor specific" and "reserved"
information as possible about disk drives.  man smartctl and man
smartd will provide more information.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
install %{SOURCE2} $RPM_BUILD_ROOT/etc/
install %{SOURCE4} $RPM_BUILD_ROOT/%_docdir/%name-%version/README.urpmi

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service smartd

%preun
%_preun_service smartd


%files
%defattr(-,root,root)
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/smartd.conf
%{_initrddir}/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}-%{version}


