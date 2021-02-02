Summary:	For monitoring S.M.A.R.T. disks and devices
Name:		smartmontools
Version:	7.2
Release:	2
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	smartd.sysconfig
#semi-automatic update of drivedb.h
%global		UrlSource3 https://raw.githubusercontent.com/smartmontools/smartmontools/master/smartmontools/drivedb.h
# (tpg) pull it from https://github.com/smartmontools/smartmontools/blob/master/smartmontools/drivedb.h
Source3:	drivedb.h
Patch0:		smartmontools-7.2-service.patch
Patch1:		smartmontools-6.2-keep-automatic-offline-tests-and-attribute-save-on.patch
%rename		smartsuite
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	curl

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
%autosetup -p1
curl %{UrlSource3} -o %{SOURCE3} ||:
cp %{SOURCE3} .

%build
%configure \
	--with-libcap-ng=yes \
	--with-drivedbdir=yes \
	--with-update-smart-drivedb=yes \
	--with-initscriptdir=no \
	--with-libsystemd \
	--with-systemdsystemunitdir=%{_unitdir} \
	--with-nvme-devicescan \
	--with-smartdscriptdir=%{_libexecdir}/%{name} \
	--with-smartdplugindir=%{_libexecdir}/%{name}

%make_build BUILD_INFO='"(%{distribution} %{version}-%{release})"'

%install
%make_install
install -p -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/smartd

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-smartd.preset << EOF
enable smartd.service
EOF

%preun
%systemd_preun smartd.service

%post
%systemd_post smartd.service

%postun
%systemd_postun_with_restart smartd.service

%files
%config(noreplace) %{_sysconfdir}/smartd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/smartd
%attr(0644,root,root) %{_unitdir}/smartd.service
%{_libexecdir}/%{name}
%{_presetdir}/86-smartd.preset
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
%{_datadir}/%{name}/drivedb.h
