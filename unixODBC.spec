%define LIBMAJ 	1
%define libname %mklibname %name %LIBMAJ
%define develname %mklibname %name -d
%define old_libname %mklibname %{name} 2

Name: 		unixODBC
Version: 	2.3.0
Release:	4
Group: 		Databases
Summary: 	Unix ODBC driver manager and database drivers
License: 	GPLv2+ and LGPLv2+
URL: 		http://www.unixODBC.org/
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
Provides:	%{old_libname}
Obsoletes:	%{old_libname}

%description -n	%{libname}
unixODBC  libraries.

%package -n	%{develname}
Summary: 	Includes and shared libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{old_libname}-devel
Obsoletes:	%{_lib}unixODBC1-devel < %{version}-%{release}

%description -n	%{develname}
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and shared libraries for development.

%prep
%setup -q

%build
%configure2_5x \
  --with-included-ltdl=no \
  --with-ltdl-include=%{_includedir} \
  --with-ltdl-lib=%{_libdir} \
  --disable-static \
  --enable-drivers
%make

%install
rm -rf %{buildroot}

%makeinstall_std

%multiarch_binaries %buildroot/%_bindir/odbc_config

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files 
%doc AUTHORS INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
%dir %{_sysconfdir}/ODBCDataSources
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql

%files -n %{libname}
%_libdir/libodbc.so.%{LIBMAJ}*
%_libdir/libodbccr.so.%{LIBMAJ}*
%_libdir/libodbcinst.so.%{LIBMAJ}*
%_libdir/libnn.so.%{LIBMAJ}*
%_libdir/libtemplate.so.%{LIBMAJ}*
%_libdir/libodbcpsql.so.2
%_libdir/libodbcpsql.so.2.*

%files -n %{develname}
%doc doc/
%_bindir/odbc_config
%{_includedir}/*
%{_libdir}/lib*.so
%{multiarch_bindir}/odbc_config
