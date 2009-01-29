%define LIBMAJ 	1
%define libname %mklibname %name %LIBMAJ
%define develname %mklibname %name -d
%define sdevelname %mklibname %name -d -s
%define libgtkgui_major	0
%define libgtkgui_name	%mklibname gtkodbcconfig %{libgtkgui_major}
%define old_libname %mklibname %{name} 2

%define qt_gui  1
%{?_without_qt: %{expand: %%global qt_gui 0}}

%define gtk_gui 0
%{?_with_gtk: %{expand: %%global gtk_gui 1}}

Summary: 	Unix ODBC driver manager and database drivers
Name: 		unixODBC
Version: 	2.2.14
Release:	%mkrel 3
Group: 		Databases
License: 	GPLv2+ and LGPLv2+
URL: 		http://www.unixODBC.org/
Source0:	http://www.unixodbc.org/%{name}-%{version}.tar.gz
Source2:	odbcinst.ini
Source3:	qt-attic.tar.bz2
Source4:	qt-attic2.tar.bz2
Patch1:		unixodbc-fix-compile-with-qt-3.1.1.patch
Patch2:		unixodbc-fix-compile-with-qt-3.1.1.patch2
Patch3:		unixODBC-2.2.12-libtool.patch
Patch4:		unixodbc-fix-external-ltdl.patch
Patch5:		unixODBC-2.2.14-format_not_a_string_literal_and_no_format_arguments.diff
Patch6:		unixodbc-fix-2.2.14-fix-qt-detect.patch
BuildRequires:	autoconf2.5 >= 2.52
BuildRequires:	autoconf
BuildRequires:	bison 
BuildRequires:	flex 
BuildRequires:	readline-devel 
BuildRequires:	chrpath
BuildRequires:	byacc
BuildRequires:	dos2unix 
BuildRequires:	libltdl-devel
BuildRequires:	pth-devel
%if %{qt_gui}
BuildRequires:	qt4-devel
%endif
%if %{gtk_gui}
BuildRequires:	gnome-common
BuildRequires:	gnome-libs-devel
%endif
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
UnixODBC is a free/open specification for providing application developers 
with a predictable API with which to access Data Sources. Data Sources include 
SQL Servers and any Data Source with an ODBC Driver.

%package -n	%{libname}
Summary:	Libraries unixODBC 
Group:		System/Libraries
Provides:	%{old_libname}
Obsoletes:	%{old_libname}

%description -n	%{libname}
unixODBC  libraries.

%if %{gtk_gui}
%package -n	%{libgtkgui_name}
Summary:	gODBCConfig libraries
Group: 		System/Libraries

%description -n	%{libgtkgui_name}
gODBCConfig libraries.
%endif

%if %{qt_gui}
%package -n	%{libname}-qt
Group:		System/Libraries
Summary:	UnixODBC library, with Qt
Provides:	%{old_libname}-qt
Provides:	%{name}-qt
Obsoletes:	%{old_libname}-qt

%description -n	%{libname}-qt
unixODBC inst library, Qt flavored.

This has been split off from the main unixODBC libraries so you don't
require X11 and qt if you wish to use unixODBC.
%endif

%package -n	%{develname}
Summary: 	Includes and shared libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{old_libname}-devel
Obsoletes:	%{_lib}unixODBC1-devel < %{version}-%{release}

%description -n	%{develname}
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and shared libraries for development.

%package -n	%{sdevelname}
Summary: 	Static libraries for ODBC development
Group: 		Development/Other
Requires: 	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{name}-devel %{old_libname}-static-devel
Obsoletes:	%{_lib}unixODBC1-static-devel < %{version}-%{release}

%description -n	%{sdevelname}
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains static libraries for development.

%if %{qt_gui}
%package	gui-qt
Summary: 	ODBC configurator, Data Source browser and ODBC test tool based on Qt
Group: 		Databases
Requires: 	%{name} = %{version} %{name}-qt usermode usermode-consoleonly

%description	gui-qt
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains two Qt based GUI programs for unixODBC: 
ODBCConfig and DataManager
%endif

%if %{gtk_gui}
%package	gui-gtk
Summary: 	ODBC configurator based on GTK+ and GTK+ widget for gnome-db
Group:		Databases
Requires: 	%{name} = %{version} usermode usermode-consoleonly

%description	gui-gtk
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains one GTK+ based GUI program for unixODBC: gODBCConfig
%endif

%prep

%setup -q -a3 -a4
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .libtool
%patch4 -p1 -b .ltdl
%patch5 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch6 -p0 -b .qt

%build
export EGREP='grep -E'

# we don't need run a bogus uselless configure
rm -rf libltdl

libtoolize --copy --force; aclocal; automake -a; autoconf

%if %{qt_gui}
export MOC=%{qt4bin}/moc
export UIC=%{qt4bin}/uic
%endif

%configure2_5x \
%if %{qt_gui}
    --with-qt-dir=%qt4dir \
    --with-qt-libraries=%qt4lib \
    --with-qt-includes=%qt4include \
    --with-qt-programs=%qt4bin \
%else
    --disable-gui \
%endif
    --enable-ltdllib=yes \
    --enable-static

%make

%install
rm -rf %{buildroot} 

export EGREP='grep -E'

# Short Circuit Compliant (tm).
[ ! -f doc/Makefile ] && {
	cd doc
	echo -en "install:\n\n" > Makefile
	cd ..
}

%makeinstall

install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/
perl -pi -e "s,/lib/,/%{_lib}/," %{buildroot}%{_sysconfdir}/odbcinst.ini

# (sb) use the versioned symlinks, rather than the .so's, this should 
# eliminate the issues with requiring -devel packages or having 
# to override auto requires

pushd %{buildroot}
newlink=`find usr/%{_lib} -type l -name 'libodbcpsql.so.*' | tail -1`
perl -pi -e "s,usr/%{_lib}/libodbcpsql.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
newlink=`find usr/%{_lib} -type l -name 'libodbcpsqlS.so.*'`
perl -pi -e "s,usr/%{_lib}/libodbcpsqlS.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
popd

%if %{gtk_gui}
# gODBCConfig must be built after installing the main unixODBC parts
cd gODBCConfig
%configure2_5x --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --with-odbc=%{buildroot}%{_prefix}

# (sb) can't find depcomp
cp ../depcomp .
%make
# ugly hack.
%makeinstall || true
mkdir -p %{buildroot}%{_datadir}/pixmaps/gODBCConfig
for pixmap in ./pixmaps/*;do
   install -m 644 $pixmap %{buildroot}%{_datadir}/pixmaps/gODBCConfig
done
cd ..
%endif

# drill out shared libraries for gODBCConfig *sigh*
# also drill out the Qt inst library that doesn't seem to be used at the moment
# by anyone ATM?
echo "%defattr(-,root,root)" > libodbc-libs.filelist
find %{buildroot}%_libdir -name '*.so.*' | sed -e "s|%{buildroot}||g" | grep -v -e gtk -e instQ >> libodbc-libs.filelist

# Uncomment the following if you wish to split off development libraries
# as well so development with ODBC does not require X11 libraries installed.
# Also you need to add in the appropriate description and filelist.
if 0; then

echo "%defattr(-, root, root)" > libodbc-devellibs.filelist
find %{buildroot}%{_libdir} -name '*.so' -o -name '*.la' -o -name '*.a' | sed -e "s|%{buildroot}||g" | grep -v -e gtk -e instQ >> libodbc-devellibs.filelist

fi

#rpaths on x86, x86_64
chrpath -d %{buildroot}%{_bindir}/*
chrpath -d %{buildroot}%{_libdir}/*.0.0

# Menu entries

# setup links for consolehelpper support to allow root System DSN config
install -d %{buildroot}%{_sbindir}
pushd %{buildroot}%{_bindir}
%if %{qt_gui}
ln -sf consolehelper ODBCConfig-root
ln -s ../bin/ODBCConfig %{buildroot}%{_sbindir}/ODBCConfig-root
%endif
%if %{gtk_gui}
ln -sf consolehelper gODBCConfig-root
ln -s ../bin/gODBCConfig %{buildroot}%{_sbindir}/gODBCConfig-root
%endif
popd

%if %{qt_gui}
# ODBCConfig

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-ODBCConfig.desktop << EOF
[Desktop Entry]
Name=ODBCConfig
Comment=ODBC Configuration Tool
Exec=%{_bindir}/ODBCConfig
Icon=databases_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-ODBCConfig-root.desktop << EOF
[Desktop Entry]
Name=ODBConfig (Root User)
Comment=ODBC Configuration Tool (Root User)
Exec=%{_bindir}/ODBCConfig-root
Icon=databases_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF

%endif

%if %{gtk_gui}
# gODBCConfig
# Put capital G in title and longtitle to shut rpmlint warnings
%endif

find doc -name Makefile\* -exec rm {} \;
find doc -type f -exec chmod -x {} \;
dos2unix doc/ProgrammerManual/Tutorial/index.html

%if %{gtk_gui}
%if %mdkversion < 200900
%post -n %{libgtkgui_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libgtkgui_name} -p /sbin/ldconfig
%endif
%endif

%if %{qt_gui}
%if %mdkversion < 200900
%post -n %{libname}-qt -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname}-qt -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %{qt_gui}
%if %mdkversion < 200900
%post gui-qt
%update_menus
%endif

%if %mdkversion < 200900
%postun gui-qt
%clean_menus
%endif
%endif

%if %{gtk_gui}
%if %mdkversion < 200900
%post gui-gtk
%update_menus
%endif

%if %mdkversion < 200900
%postun gui-gtk
%clean_menus
%endif
%endif

%clean
rm -rf %{buildroot} 
#rm -f libodbc-libs.filelist

%files 
%defattr(-,root,root)
%doc AUTHORS INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime)  %{_sysconfdir}/odbc*.ini
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql
%{_bindir}/odbc_config
	  
%files -n %{libname} -f libodbc-libs.filelist
%defattr(-,root, root)

%files -n %{develname}
%defattr(-,root,root)
%doc doc/
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.la
%if %{qt_gui}
%exclude %{_libdir}/lib*instQ4.so
%exclude %{_libdir}/lib*instQ4.la
%endif

%files -n %{sdevelname}
%defattr(-,root,root)
%{_libdir}/*.a

%if %{qt_gui}
%files -n %{libname}-qt
%defattr(-, root, root)
%{_libdir}/lib*instQ4.so.*

%files gui-qt
%defattr(-, root, root)
%{_bindir}/ODBCConfig*
%{_sbindir}/ODBCConfig*
%{_datadir}/applications/mandriva-ODBC*.desktop
%endif

%if %{gtk_gui}
%files -n %{libgtkgui_name}
%defattr(-,root, root)
%{_libdir}/libgtk*.so.*

%files gui-gtk 
%defattr(-, root, root)
%doc NEWS README AUTHORS
%{_bindir}/gODBCConfig*
%{_sbindir}/gODBCConfig*
%{_datadir}/pixmaps/*
%endif
