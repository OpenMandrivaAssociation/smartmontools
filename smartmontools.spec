Summary:	For monitoring S.M.A.R.T. disks and devices
Name:		smartmontools
Version:	6.0
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://smartmontools.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	smartd.conf
Source2:	smartd.init
Source3:	smartd.sysconfig
Patch0:		smartmontools-6.0-service.patch
Obsoletes:	smartsuite
Provides:	smartsuite
Requires(post):	rpm-helper
Requires(preun): rpm-helper
BuildRequires:	libcap-ng-devel
BuildRequires:	pkgconfig(systemd)

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
%configure2_5x \
    --with-libcap-ng=yes \
    --enable-drivedb

%make

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}%{_sysconfdir}/sysconfig
%__install -d %{buildroot}%{_initrddir}

%makeinstall_std

%__install %{SOURCE1} %{buildroot}%{_sysconfdir}/
%__install %{SOURCE2} %{buildroot}%{_initrddir}/smartd
%__install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/smartd

%post
%_post_service smartd

%preun
%_preun_service smartd

%clean
%__rm -rf %{buildroot}

%files
%attr(0755,root,root) %{_initrddir}/smartd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smartd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/smartd
%{_sbindir}/*
%{_mandir}/man?/*
%{_docdir}/%{name}
%{_datadir}/%{name}/drivedb.h
/lib/systemd/system/smartd.service

%changelog
* Fri Apr 06 2012 Andrey Bondrov <abondrov@mandriva.org> 5.41-5
- Build for Rosa 2012 LTS
- Add pkgconfig(systemd) to BuildRequires for smartd.service path detection

* Fri Mar 02 2012 Oden Eriksson <oeriksson@mandriva.com> 5.41-1.2
- built for updates

* Tue Jan 10 2012 Andrey Bondrov <abondrov@mandriva.org> 5.41-1.1mdv2011.0
+ Revision: 759511
- Add patch0 to fix service path (bug #64477)

* Sun Jun 12 2011 Oden Eriksson <oeriksson@mandriva.com> 5.41-1
+ Revision: 684306
- fix build, take #2 (someone will have to marge changes from smartmontools-5.41-1.fc16.src.rpm i guess...)
- fix build, take #1
- 5.41

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 5.40-2
+ Revision: 669990
- mass rebuild

* Tue Nov 16 2010 Oden Eriksson <oeriksson@mandriva.com> 5.40-1mdv2011.0
+ Revision: 598045
- 5.40
- provide our own initscript
- fix deps

* Thu Jan 28 2010 Erwan Velu <erwan@mandriva.org> 5.39.1-1mdv2010.1
+ Revision: 497837
- 5.39.1

* Thu Dec 10 2009 Frederik Himpe <fhimpe@mandriva.org> 5.39-1mdv2010.1
+ Revision: 476084
- Update to new version 5.39
- Remove format error patch integrated upstream

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 5.38-5mdv2010.0
+ Revision: 427197
- rebuild

* Wed Feb 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.38-4mdv2009.1
+ Revision: 337587
- fix format errors
- install doc in expected location
- drop README.urpmi, just telling users to edit their configuration is a bit useless
- spec cleanup
- keep bash completion in its own package

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 5.38-3mdv2009.0
+ Revision: 225446
- rebuild

* Mon Mar 10 2008 Erwan Velu <erwan@mandriva.org> 5.38-2mdv2008.1
+ Revision: 183401
- 5.38 official release
  Remove patch0 (upstream)
  This release closes bug #37887

* Fri Feb 29 2008 Erwan Velu <erwan@mandriva.org> 5.38-1mdv2008.1
+ Revision: 176708
- Update source to 5.38
- Using 5.38 tag

* Sat Feb 02 2008 Thomas Backlund <tmb@mandriva.org> 5.38-0.1mdv2008.1
+ Revision: 161576
- update to 5.38 (cvs snapshot 20080203)
- drop patch1: hsm fix, merged upstream
- drop patch2: strange_buffer fix, merged upstream

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 22 2007 Erwan Velu <erwan@mandriva.org> 5.37-2mdv2008.0
+ Revision: 69152
- Preventing some some HSM violation  on sata_nv


* Mon Jan 15 2007 Erwan Velu <erwan@mandriva.org> 5.37-1mdv2007.0
+ Revision: 109094
- .asc file no more exists
- 5.37
- Import smartmontools

* Wed Apr 19 2006 Erwan Velu <erwan@mandriva.com> 5.36-1mdk
- 5.36

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 5.33-6mdk
- drop parallel-init patch (Patch0)
- Patch0: use standard LSB tags instead of X-UnitedLinux tags
- fix incorrect Requires(X)

* Sun Jan 01 2006 Couriousous <couriousous@mandriva.org> 5.33-5mdk
- Add parallel init stuff

* Wed Oct 05 2005 Erwan Velu <velu@seanodes.com> 5.33-4mdk
- Adding README.urpmi
- Adding mail example in config file

* Fri Jul 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 5.33-3mdk 
- bash completion

* Tue Jun 14 2005 Erwan Velu <velu@seanodes.com> 5.33-2mdk
- Fixing stupid errors

* Fri Oct 29 2004 Erwan Velu <erwan@mandrakesoft.com> 5.33-1mdk
- 5.33

* Tue Aug 17 2004 Erwan Velu <erwan@mandrakesoft.com> 5.32-2mdk
- Using a better default configuration file

* Tue Jul 13 2004 Erwan Velu <erwan@mandrakesoft.com> 5.32-1mdk
- 5.32

* Thu Jun 10 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.31-2mdk
- Fix spelling errors in description

* Mon May 17 2004 Abel Cheung <deaddog@deaddog.org> 5.31-1mdk
- New version
- Use tar.gz for source verification

* Tue Mar 09 2004 Erwan Velu <erwan@mandrakesoft.com> 5.30-1mdk
- New release

* Thu Feb 19 2004 Erwan Velu <erwan@mandrakesoft.com> 5.27-1mdk
- New Release

