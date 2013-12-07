%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Unix ODBC driver manager and database drivers
Name:		unixODBC
Version:	2.3.1
Release:	7
Group:		Databases
License:	GPLv2+ and LGPLv2+
URL:		http://www.unixODBC.org/
Source0:	http://www.unixodbc.org/%{name}-%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	byacc
BuildRequires:	libltdl-devel

%description
UnixODBC is a free/open specification for providing application developers 
with a predictable API with which to access Data Sources. Data Sources include 
SQL Servers and any Data Source with an ODBC Driver.

%package -n	%{libname}
Summary:	Libraries unixODBC
Group:		System/Libraries
Obsoletes:	%{mklibname unixODBC 1} < 2.3.1

%description -n	%{libname}
This package contains the shared unixODBC libraries.

%package -n	%{develname}
Summary: 	Includes and shared libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and shared libraries for development.

%prep
%setup -q

# Blow away the embedded libtool and replace with build system's libtool.
# (We will use the installed libtool anyway, but this makes sure they match.)
rm -rf config.guess config.sub install-sh ltmain.sh libltdl
# this hack is so we can build with either libtool 2.2 or 1.5
libtoolize --install || libtoolize

%build
autoreconf -fi
%configure2_5x \
  --with-included-ltdl=no \
  --with-ltdl-include=%{_includedir} \
  --with-ltdl-lib=%{_libdir} \
  --disable-static \
  --enable-drivers
%make

%install
mkdir -p %{buildroot}%{_sysconfdir}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/odbc_config

%files
%doc AUTHORS INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
%dir %{_sysconfdir}/ODBCDataSources
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql

%files -n %{libname}
%{_libdir}/libodbccr.so.%{major}*
%{_libdir}/libodbcinst.so.%{major}*
%{_libdir}/libodbcpsql.so.%{major}*
%{_libdir}/libodbc.so.%{major}*
%{_libdir}/libnn.so.1*
%{_libdir}/libtemplate.so.1*

%files -n %{develname}
%doc doc/
%{_bindir}/odbc_config
%{_includedir}/*
%{_libdir}/lib*.so
%{multiarch_bindir}/odbc_config


%changelog
* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-2
+ Revision: 739158
- use the wrong way to save time...

* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-1
+ Revision: 739097
- 2.3.1
- new major 2 (again)
- various cleanups

* Tue Dec 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.0-4
+ Revision: 738300
- drop the static lib, its sub package and the libtool *.la file
- various fixes

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.0-3
+ Revision: 661753
- multiarch fixes

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 2.3.0-2mdv2011.0
+ Revision: 593904
- enalbe drivers

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 2.3.0-1mdv2011.0
+ Revision: 593895
- update file list
- New version 2.3.0 (gui has been spliited)
- drop old patch for gui parts
- there is no need to install sample odbcinst.ini now, cause drivers are splitted too

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 2.2.14-10mdv2011.0
+ Revision: 563954
- BR qt-assistant-adp

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.14-9mdv2010.1
+ Revision: 519077
- rebuild

* Thu Sep 17 2009 Helio Chissini de Castro <helio@mandriva.com> 2.2.14-8mdv2010.0
+ Revision: 443703
- Proper fix Qt dialog. Library was not a library, but a dyn loaded module. Old library package was deprecated.

* Wed Sep 16 2009 Helio Chissini de Castro <helio@mandriva.com> 2.2.14-7mdv2010.0
+ Revision: 443596
- Bring Qt back in their Qt4 form
- Removed old inavlid patches and finish the legacy !!

* Tue Jun 23 2009 Helio Chissini de Castro <helio@mandriva.com> 2.2.14-5mdv2010.0
+ Revision: 388789
- Move odbc_config for multiarch devel
- No need chrpath

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.14-4mdv2009.1
+ Revision: 344741
- disable the qt build for now, enable it again when qt is fixed
- rebuilt against new readline

* Thu Jan 29 2009 Funda Wang <fwang@mandriva.org> 2.2.14-3mdv2009.1
+ Revision: 335078
- fix qt detct & enable gui
- follow mandriva devel lib name policy

* Wed Jan 28 2009 Götz Waschk <waschk@mandriva.org> 2.2.14-2mdv2009.1
+ Revision: 334822
- rebuild for new libltdl

* Mon Jan 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.14-1mdv2009.1
+ Revision: 331215
- 2.2.14
- rediff patches
- fix build with -Werror=format-security (P5)
- add more examples in S2
- disable broken kde4/qt4 make foo for now

* Thu Jun 19 2008 Helio Chissini de Castro <helio@mandriva.com> 2.2.12-9mdv2009.0
+ Revision: 226809
- Since we're moved qt3 libraries to libdir, we just need a small changes to make it compiles again.
  The extra qt3 m4 patch is not needed anymore

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix build
    - re-enable the qt3 stuff
    - make it possible to build it without the qt gui parts

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - kill explicit icon extension

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Nov 21 2007 Helio Chissini de Castro <helio@mandriva.com> 2.2.12-4mdv2008.1
+ Revision: 111021
- Remove odbcinstQ link on devel file to avoid devel package requires qt3-devel mandatory. Since
  this library is not used for common unixodbc usage, this will allow build qt4 with unixodbc
  support without requiring qt3-devel package.

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Jul 26 2007 Helio Chissini de Castro <helio@mandriva.com> 2.2.12-3mdv2008.0
+ Revision: 56063
- Bunzip patch2 for qt3
- Cleaned up autoconf, configure and qt dirs related issues ( removal of libltld subdir is related
  for same issues )
- Created static-devel package


* Mon Jan 15 2007 Stew Benedict <sbenedict@mandriva.com> 2.2.12-2mdv2007.0
+ Revision: 109119
- re-add, rediff P3
  more %%_lib substitution in configure for 64bit
- 2.2.12

* Thu Sep 07 2006 Andreas Hasenack <andreas@mandriva.com> 2.2.11-13mdv2007.0
+ Revision: 60407
- bumped release
- synced with cooker. Changes:
  * Tue Sep 05 2006 Stew Benedict <sbenedict@mandriva.com> 2.2.11-12mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes
  * Thu Aug 31 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.2.11-11mdv2007.0
- fix old unixODBC2 obsoletes/provides (lib64)
- drop explicit libodbc{,inst}.so provides in -devel packages,
  acroread & jre packages were already fixed for some time
  * Mon Jul 03 2006 Stew Benedict <sbenedict@mandriva.com> 2.2.11-10mdv2007.0
- disable gtk build (gtk+1.2->contrib, bug #23449, Cris B)
- xdg menu, docs shouldn't be executable
  * Sun Jun 18 2006 Laurent MONTEL <lmontel@mandriva.com> 2.2.11-9
- Reactivate gtk/qt build
  * Fri Jun 16 2006 Laurent MONTEL <lmontel@mandriva.com> 2.2.11-8
- Rebuild with new png
  * Wed May 17 2006 Laurent MONTEL <lmontel@mandriva.com> 2.2.11-7
- Rebuild against new xorg Disable gtk gui until we rebuild it
  * Mon May 08 2006 Stefan van der Eijk <stefan@eijk.nu> 2.2.11-6mdk
- rebuild for sparc
  * Tue Aug 16 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.2.11-5mdk
- built-in libtool fixes
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

  + Helio Chissini de Castro <helio@mandriva.com>
    - Uploading package ./unixODBC

* Thu May 19 2005 Stew Benedict <sbenedict@mandriva.com> 2.2.11-4mdk
- fix provides

* Fri May 13 2005 Stew Benedict <sbenedict@mandriva.com> 2.2.11-3mdk
- try again, half the upload rejected

* Thu May 12 2005 Stew Benedict <sbenedict@mandriva.com> 2.2.11-2mdk
- 64 bit build fix (define EGREP, gets lost for some reason?)

* Thu May 05 2005 Stew Benedict <sbenedict@mandriva.com> 2.2.11-1mdk
- 2.2.11, mkrel, rpmlint, buildrequires

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.2.10-3mdk
- rebuild for new readline

* Tue Nov 23 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.2.10-2mdk
- add BuildRequires: libltdl-devel

* Mon Nov 22 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.10-1mdk
- 2.2.10, rpmlint, correct LIBMAJ

* Wed Oct 13 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.8-3mdk
- fix 10.1 build (automake and friends)
- Installed (but unpackaged) file(s)

* Fri Jun 04 2004 Laurent Montel <lmontel@mandrakesoft.com> 2.2.8-2mdk
- Rebuild against libstdc++

* Tue May 04 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.8-1mdk
- 2.2.8

