%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Unix ODBC driver manager and database drivers
Name:		unixODBC
Version:	2.3.7
Release:	1
Group:		Databases
License:	GPLv2+ and LGPLv2+
URL:		http://www.unixODBC.org/
Source0:	ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	byacc
BuildRequires:	atomic-devel
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
%autosetup -p1

chmod 0644 Drivers/MiniSQL/*.c
chmod 0644 Drivers/nn/*.c
chmod 0644 Drivers/template/*.c
chmod 0644 doc/ProgrammerManual/Tutorial/*.html
chmod 0644 doc/lst/*
chmod 0644 include/odbcinst.h

# Blow away the embedded libtool and replace with build system's libtool.
# (We will use the installed libtool anyway, but this makes sure they match.)
rm -rf config.guess config.sub install-sh ltmain.sh libltdl depcomp missing
# this hack is so we can build with either libtool 2.2 or 1.5
libtoolize --install --copy --force || libtoolize --copy --force

aclocal
#automake --add-missing
#autoheader
#autoconf

#sed -i 's!touch $@!!g' libltdl/Makefile.in Makefile.in

%build
%configure \
  --with-ltdl-include=%{_includedir} \
  --with-included-ltdl=no \
  --with-ltdl-lib=%{_libdir} \
  --with-gnu-ld=yes \
  --enable-threads=yes \
  --disable-static \
  --enable-drivers

# don't touch my system files
unlink libltdl/config-h.in
cp -f %{_datadir}/libtool/config-h.in libltdl/config-h.in
%make_build

%install
mkdir -p %{buildroot}%{_sysconfdir}
%make_install

%files
%doc AUTHORS INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
%dir %{_sysconfdir}/ODBCDataSources
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql
%{_bindir}/slencheck
%{_mandir}/man1/*.1.*
%{_mandir}/man5/*.5.*
%{_mandir}/man7/*.7.*

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
%{_libdir}/pkgconfig/*.pc
