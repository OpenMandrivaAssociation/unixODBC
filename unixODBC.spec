%define _disable_rebuild_configure 1

# unixODBC is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define devel32name %mklib32name %{name} -d

Summary:	Unix ODBC driver manager and database drivers
Name:		unixODBC
Version:	2.3.12
Release:	1
Group:		Databases
License:	GPLv2+ and LGPLv2+
URL:		https://www.unixODBC.org/
Source0:	https://github.com/lurcher/unixODBC/releases/download/%{version}/unixODBC-%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	byacc
BuildRequires:	atomic-devel
BuildRequires:	libltdl-devel
%if %{with compat32}
BuildRequires:	devel(libltdl)
%endif

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

%if %{with compat32}
%package -n	%{lib32name}
Summary:	Libraries unixODBC (32-bit)
Group:		System/Libraries

%description -n	%{lib32name}
This package contains the shared unixODBC libraries.

%package -n	%{devel32name}
Summary: 	Includes and shared libraries for ODBC development (32-bit)
Group: 		Development/Other
Requires: 	%{develname} >= %{version}-%{release}
Requires: 	%{lib32name} >= %{version}-%{release}

%description -n	%{devel32name}
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and shared libraries for development.
%endif

%prep
%autosetup -p1

chmod 0644 Drivers/MiniSQL/*.c
chmod 0644 Drivers/nn/*.c
chmod 0644 Drivers/template/*.c
chmod 0644 doc/ProgrammerManual/Tutorial/*.html
chmod 0644 doc/lst/*
chmod 0644 include/odbcinst.h


#sed -i 's!touch $@!!g' libltdl/Makefile.in Makefile.in

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 \
  --with-included-ltdl=no \
  --with-gnu-ld=yes \
  --enable-threads=yes \
  --enable-drivers
cd ..
%endif

mkdir build
cd build
%configure \
  --with-included-ltdl=no \
  --with-gnu-ld=yes \
  --enable-threads=yes \
  --enable-drivers

%build

%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
mkdir -p %{buildroot}%{_sysconfdir}
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files
%doc AUTHORS INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
%dir %{_sysconfdir}/ODBCDataSources
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql
%{_bindir}/slencheck
%doc %{_mandir}/man1/*.1.*
%doc %{_mandir}/man5/*.5.*
%doc %{_mandir}/man7/*.7.*

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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libodbccr.so.%{major}*
%{_prefix}/lib/libodbcinst.so.%{major}*
%{_prefix}/lib/libodbcpsql.so.%{major}*
%{_prefix}/lib/libodbc.so.%{major}*
%{_prefix}/lib/libnn.so.1*
%{_prefix}/lib/libtemplate.so.1*

%files -n %{devel32name}
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
