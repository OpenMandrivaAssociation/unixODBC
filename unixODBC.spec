%define LIBMAJ 	1
%define libname %mklibname %name %LIBMAJ
%define develname %mklibname %name -d
%define sdevelname %mklibname %name -d -s
%define libgtkgui_major	0
%define libgtkgui_name	%mklibname gtkodbcconfig %{libgtkgui_major}
%define old_libname %mklibname %{name} 2

%define bcond_without qt_gui
%define bcond_with gtk

Name: 		unixODBC
Version: 	2.2.14
Release:	%mkrel 8
Group: 		Databases
Summary: 	Unix ODBC driver manager and database drivers
License: 	GPLv2+ and LGPLv2+
URL: 		http://www.unixODBC.org/
Source0:	http://www.unixodbc.org/%{name}-%{version}.tar.gz
Source2:	odbcinst.ini
Patch0:		unixODBC-2.2.12-libtool.patch
Patch1:		unixodbc-fix-external-ltdl.patch
Patch2:		unixODBC-2.2.14-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:     unixodbc-fix-2.2.14-fix-qt-detect.patch
Patch4:     unixODBC-2.2.14-qt4-module.patch
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

%if %with gtk_gui
%package -n	%{libgtkgui_name}
Summary:	gODBCConfig libraries
Group: 		System/Libraries
BuildRequires:	gnome-common
BuildRequires:	gnome-libs-devel

%description -n	%{libgtkgui_name}
gODBCConfig libraries.
%endif

%if %without qt_gui
%package	gui-qt
Summary: 	ODBC configurator, Data Source browser and ODBC test tool based on Qt
Group: 		Databases
BuildRequires: qt4-devel
Requires: 	%{name} = %{version} 
Requires:   usermode 
Requires:   usermode-consoleonly
Obsoletes:  %{libname}-qt

%description	gui-qt
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains two Qt based GUI programs for unixODBC: 
ODBCConfig and DataManager
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

%if %with gtk_gui
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

%setup -q
%patch0 -p1 -b .libtool
%patch1 -p1 -b .ltdl
%patch2 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch3 -p0 -b .qt4
%patch4 -p0 -b .qt4

%build
export EGREP='grep -E'

# we don't need run a bogus uselless configure
rm -rf libltdl
# We don't need pre generated moc files from old Qt's 
rm -f $(grep generated odbcinstQ4/*.cpp | sed -e "s,:.*,,g")

autoreconf -f -i

export MOC=%{qt4bin}/moc
export UIC=%{qt4bin}/uic

%configure2_5x \
%if %without qt_gui
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


# Multiarch fixes
%multiarch_binaries %buildroot/%_bindir/odbc_config

# (sb) use the versioned symlinks, rather than the .so's, this should 
# eliminate the issues with requiring -devel packages or having 
# to override auto requires

pushd %{buildroot}
newlink=`find usr/%{_lib} -type l -name 'libodbcpsql.so.*' | tail -1`
perl -pi -e "s,usr/%{_lib}/libodbcpsql.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
newlink=`find usr/%{_lib} -type l -name 'libodbcpsqlS.so.*'`
perl -pi -e "s,usr/%{_lib}/libodbcpsqlS.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
popd

%if %with gtk_gui
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

# Menu entries

# setup links for consolehelpper support to allow root System DSN config
install -d %{buildroot}%{_sbindir}

%if %with gtk_gui
pushd %{buildroot}%{_bindir}
	ln -sf consolehelper gODBCConfig-root
	ln -s ../bin/gODBCConfig %{buildroot}%{_sbindir}/gODBCConfig-root
popd
%endif

%if %without qt_gui
pushd %{buildroot}%{_bindir}
	ln -sf consolehelper ODBCConfig-root
	ln -s ../bin/ODBCConfig %{buildroot}%{_sbindir}/ODBCConfig-root
popd

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

find doc -name Makefile\* -exec rm {} \;
find doc -type f -exec chmod -x {} \;
dos2unix doc/ProgrammerManual/Tutorial/index.html


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
	  
%files -n %{libname}
%defattr(-,root, root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/
%_bindir/odbc_config
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.la
%if %without qt_gui
%exclude %{_libdir}/lib*Q4.*
%endif
%multiarch %_bindir/%multiarch_platform/odbc_config

%files -n %{sdevelname}
%defattr(-,root,root)
%{_libdir}/*.a

%if %without qt_gui

%files gui-qt
%defattr(-, root, root)
%{_bindir}/ODBCConfig*
%{_sbindir}/ODBCConfig*
%{_datadir}/applications/mandriva-ODBC*.desktop
%{_libdir}/lib*Q4.*
%exclude %{_libdir}/lib*Q4.a
%endif

%if %with gui-gtk
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
