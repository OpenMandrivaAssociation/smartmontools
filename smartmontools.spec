%define name smartmontools
%define version 5.38
%define release %mkrel 5

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	For monitoring S.M.A.R.T. disks and devices
License:	GPL
Group:		System/Kernel and hardware
URL:        http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source2:	smartd.conf
Patch:      smartmontools-5.38-fix-format-errors.patch
Obsoletes:	smartsuite
Provides:	smartsuite
Requires(post):	rpm-helper
Requires(preun): rpm-helper
BuildRoot:      %{_tmppath}/%{name}-%{version}

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
%patch -p 1

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install %{SOURCE2} %{buildroot}/etc/

mv %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post
%_post_service smartd

%preun
%_preun_service smartd

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/smartd.conf
%{_initrddir}/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
