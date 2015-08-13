%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Unix ODBC driver manager and database drivers
Name:		unixODBC
Version:	2.3.2
Release:	4
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
%configure \
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
%{_bindir}/slencheck
%{_mandir}/man1/*.1.*
%{_mandir}/man5/*.5.*

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
