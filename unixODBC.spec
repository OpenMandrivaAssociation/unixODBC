%define LIBMAJ 	1
%define libname %mklibname %name %LIBMAJ
%define libgtkgui_major	0
%define libgtkgui_name	%mklibname gtkodbcconfig %{libgtkgui_major}
%define old_libname %mklibname %{name} 2

%define qt_gui  1
%define gtk_gui 0

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_QT:	%%global qt_gui 0}}
%{expand: %{?_without_GTK:	%%global gtk_gui 0}}

# Allow --without <front-end> at rpm command line build
%{expand: %{?_with_QT:		%%global qt_gui 1}}
%{expand: %{?_with_GTK:		%%global gtk_gui 1}}

Summary: 	Unix ODBC driver manager and database drivers
Name: 		unixODBC
Version: 	2.2.12
Release:	%mkrel 3

Source: 	http://www.unixodbc.org/%{name}-%{version}.tar.bz2
Source2:	odbcinst.ini
Source3:	qt-attic.tar.bz2
Source4:	qt-attic2.tar.bz2
Patch1:		unixodbc-fix-compile-with-qt-3.1.1.patch
Patch2:		unixodbc-fix-compile-with-qt-3.1.1.patch2
Patch3:		unixODBC-2.2.12-libtool.patch
Patch4:     unixodbc-fix-external-ltdl.patch

Group: 		Databases
License: 	LGPL
URL: 		http://www.unixODBC.org/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf2.5 >= 2.52
BuildRequires: autoconf
BuildRequires: bison 
BuildRequires: flex 
BuildRequires: readline-devel 
BuildRequires: chrpath
BuildRequires: byacc
BuildRequires: dos2unix 
BuildRequires: libltdl-devel
BuildRequires: pth-devel
%if %{qt_gui}
BuildRequires: qt3-devel
%endif
%if %gtk_gui
BuildRequires: gnome-common
BuildRequires: gnome-libs-devel
%endif

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

%if %gtk_gui
%package -n	%{libgtkgui_name}
Summary:	gODBCConfig libraries
Group: 		System/Libraries

%description -n	%{libgtkgui_name}
gODBCConfig libraries.
%endif

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

%package -n	%{libname}-devel
Summary: 	Includes and shared libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel lib%{name}-devel %{old_libname}-devel
Obsoletes:	%{name}-devel %{old_libname}-devel

%description -n	%{libname}-devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and shared libraries for development.

%package -n	%{libname}-static-devel
Summary: 	Static libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname}-devel = %{version}
Provides:	%{name}-static-devel lib%{name}-static-devel %{old_libname}-static-devel
Obsoletes:	%{name}-devel %{old_libname}-devel

%description -n	%{libname}-static-devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains static libraries for development.

%package	gui-qt
Summary: 	ODBC configurator, Data Source browser and ODBC test tool based on Qt
Group: 		Databases
Requires: 	%{name} = %{version} %{name}-qt usermode usermode-consoleonly

%description	gui-qt
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains two Qt based GUI programs for unixODBC: 
ODBCConfig and DataManager

%package	gui-gtk
Summary: 	ODBC configurator based on GTK+ and GTK+ widget for gnome-db
Group:		Databases
Requires: 	%{name} = %{version} usermode usermode-consoleonly

%description	gui-gtk
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains one GTK+ based GUI program for unixODBC: gODBCConfig

%prep
%setup -q -a3 -a4
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .libtool
%patch4 -p1 -b .ltdl


%build
export EGREP='grep -E'

# we don't need run a bogus uselless configure
rm -rf libltdl

aclocal && libtoolize -c -f && automake -a && autoconf

%configure2_5x \
    %if %{qt_gui}
    --with-qt-dir=%qt3dir \
    --with-qt-includes=%qt3include \
    --with-qt-libraries=%qt3lib \
    --with-qt-programs=%qt3dir/bin \
    %endif
    --enable-ltdllib=yes \
    --enable-static

%make

%install
rm -fr %buildroot
export EGREP='grep -E'

# Short Circuit Compliant (tm).
[ ! -f doc/Makefile ] && {
	cd doc
	echo -en "install:\n\n" > Makefile
	cd ..
}

%makeinstall

install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/
perl -pi -e "s,/lib/,/%{_lib}/," $RPM_BUILD_ROOT%{_sysconfdir}/odbcinst.ini

# (sb) use the versioned symlinks, rather than the .so's, this should 
# eliminate the issues with requiring -devel packages or having 
# to override auto requires

pushd $RPM_BUILD_ROOT
newlink=`find usr/%{_lib} -type l -name 'libodbcpsql.so.*' | tail -1`
perl -pi -e "s,usr/%{_lib}/libodbcpsql.so,$newlink,g" $RPM_BUILD_ROOT%{_sysconfdir}/odbcinst.ini
newlink=`find usr/%{_lib} -type l -name 'libodbcpsqlS.so.*'`
perl -pi -e "s,usr/%{_lib}/libodbcpsqlS.so,$newlink,g" $RPM_BUILD_ROOT%{_sysconfdir}/odbcinst.ini
popd

%if %gtk_gui
# gODBCConfig must be built after installing the main unixODBC parts
cd gODBCConfig
%configure2_5x --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --with-odbc=$RPM_BUILD_ROOT%{_prefix}

# (sb) can't find depcomp
cp ../depcomp .
%make
# ugly hack.
%makeinstall || true
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/gODBCConfig
for pixmap in ./pixmaps/*;do
   install -m 644 $pixmap $RPM_BUILD_ROOT%{_datadir}/pixmaps/gODBCConfig
done
cd ..
%endif

# drill out shared libraries for gODBCConfig *sigh*
# also drill out the Qt inst library that doesn't seem to be used at the moment
# by anyone ATM?
echo "%defattr(-,root,root)" > libodbc-libs.filelist
find $RPM_BUILD_ROOT%_libdir -name '*.so.*' | sed -e "s|$RPM_BUILD_ROOT||g" | grep -v -e gtk -e instQ >> libodbc-libs.filelist

# Uncomment the following if you wish to split off development libraries
# as well so development with ODBC does not require X11 libraries installed.
# Also you need to add in the appropriate description and filelist.
if 0; then

echo "%defattr(-, root, root)" > libodbc-devellibs.filelist
find $RPM_BUILD_ROOT%{_libdir} -name '*.so' -o -name '*.la' -o -name '*.a' | sed -e "s|$RPM_BUILD_ROOT||g" | grep -v -e gtk -e instQ>> libodbc-devellibs.filelist

fi

#rpaths on x86, x86_64
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*
chrpath -d $RPM_BUILD_ROOT%{_libdir}/*.0.0

# Menu entries
install -d $RPM_BUILD_ROOT%{_menudir}

# setup links for consolehelpper support to allow root System DSN config
install -d $RPM_BUILD_ROOT%{_sbindir}
pushd $RPM_BUILD_ROOT%{_bindir}
%if %{qt_gui}
ln -sf consolehelper ODBCConfig-root
ln -s ../bin/ODBCConfig $RPM_BUILD_ROOT%{_sbindir}/ODBCConfig-root
%endif
%if %{gtk_gui}
ln -sf consolehelper gODBCConfig-root
ln -s ../bin/gODBCConfig $RPM_BUILD_ROOT%{_sbindir}/gODBCConfig-root
%endif
popd

%if %{qt_gui}
# ODBCConfig
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/unixODBC-gui-qt
?package(%{name}-gui-qt): \
needs="x11" \
section="More Applications/Databases" \
longtitle="ODBCConfig" \
title="ODBCConfig" \
icon="databases_section.png" \
command="ODBCConfig" \
xdg="true"

?package(%{name}-gui-qt): \
needs="x11" \
section="More Applications/Databases" \
longtitle="ODBCConfig (root user)" \
title="ODBCConfig (root user)" \
icon="databases_section.png" \
command="ODBCConfig-root" \
xdg="true"

?package(%{name}-gui-qt): \
needs="x11" \
section="More Applications/Databases" \
longtitle="DataManager" \
title="DataManager" \
icon="databases_section.png" \
command="DataManager" \
xdg="true"

?package(%{name}-gui-qt): \
needs="x11" \
section="More Applications/Databases" \
longtitle="ODBCtest" \
title="ODBCtest" \
icon="databases_section.png" \
command="odbctest" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-ODBCConfig.desktop << EOF
[Desktop Entry]
Name=ODBCConfig
Comment=ODBC Configuration Tool
Exec=%{_bindir}/ODBCConfig
Icon=databases_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-ODBCConfig-root.desktop << EOF
[Desktop Entry]
Name=ODBConfig (Root User)
Comment=ODBC Configuration Tool (Root User)
Exec=%{_bindir}/ODBCConfig-root
Icon=databases_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-DataManager.desktop << EOF
[Desktop Entry]
Name=DataManager
Comment=ODBC Data Management Tool
Exec=%{_bindir}/DataManager
Icon=databases_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-odbctest.desktop << EOF
[Desktop Entry]
Name=ODBCTest
Comment=ODBC Test Tool
Exec=%{_bindir}/odbctest
Icon=databases_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Database;Office;X-MandrivaLinux-MoreApplications-Databases;
EOF
%endif

%if %gtk_gui
# gODBCConfig
# Put capital G in title and longtitle to shut rpmlint warnings
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/unixODBC-gui-gtk
?package(%{name}-gui-gtk): \
needs="x11" \
section="More Applications/Databases" \
longtitle="GODBCConfig" \
title="GODBCConfig" \
icon="databases_section.png" \
command="gODBCConfig" 
xdg="true"

?package(%{name}-gui-gtk): \
needs="x11" \
section="More Applications/Databases" \
longtitle="GODBCConfig (root user)" \
title="GODBCConfig (root user)" \
icon="databases_section.png" \
command="gODBCConfig-root" 
xdg="true"
EOF
%endif

find doc -name Makefile\* -exec rm {} \;
find doc -type f -exec chmod -x {} \;
dos2unix doc/ProgrammerManual/Tutorial/index.html

%clean
rm -rf $RPM_BUILD_ROOT 
#rm -f libodbc-libs.filelist

%if %gtk_gui
%post -n %{libgtkgui_name} -p /sbin/ldconfig
%postun -n %{libgtkgui_name} -p /sbin/ldconfig
%endif

%if %{qt_gui}
%post -n %{libname}-qt -p /sbin/ldconfig
%postun -n %{libname}-qt -p /sbin/ldconfig
%endif

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%if %{qt_gui}
%post gui-qt
%{update_menus}

%postun gui-qt
%{clean_menus}
%endif

%if %gtk_gui
%post gui-gtk
%{update_menus}

%postun gui-gtk
%{clean_menus}
%endif


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

%files -n %{libname}-devel 
%defattr(-,root,root)
%doc doc/
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.la

%files -n %{libname}-static-devel 
%defattr(-,root,root)
%{_libdir}/*.a

%if %{qt_gui}
%files -n %{libname}-qt
%defattr(-, root, root)
%{_libdir}/lib*instQ.so.*

%files gui-qt
%defattr(-, root, root)
%{_bindir}/DataManager
%{_bindir}/DataManagerII
%{_bindir}/ODBCConfig*
%{_sbindir}/ODBCConfig*
%{_bindir}/odbctest
%{_menudir}/unixODBC-gui-qt
%{_datadir}/applications/mandriva-ODBC*.desktop
%{_datadir}/applications/mandriva-odbctest.desktop
%{_datadir}/applications/mandriva-DataManager.desktop
%endif

%if %gtk_gui
%files -n %{libgtkgui_name}
%defattr(-,root, root)
%{_libdir}/libgtk*.so.*

%files gui-gtk 
%defattr(-, root, root)
%doc NEWS README AUTHORS
%{_bindir}/gODBCConfig*
%{_sbindir}/gODBCConfig*
%{_menudir}/unixODBC-gui-gtk
%{_datadir}/pixmaps/*
%endif


