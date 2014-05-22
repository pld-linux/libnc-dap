#
# Conditional build:
%bcond_without	tests		# perform tests
#
Summary:	The NetCDF interface to DAP-2 from OPeNDAP
Summary(pl.UTF-8):	Interfejs NetCDF do DAP-2 z OPeNDAP
Name:		libnc-dap
Version:	3.7.4
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opendap.org/pub/source/%{name}-%{version}.tar.gz
# Source0-md5:	671bf7ad07e00ed0be6518a80792c587
Patch0:		%{name}-libdap.patch
Patch1:		%{name}-format.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gcc-fortran >= 5:4.0
BuildRequires:	libdap-devel >= 3.9.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	libdap >= 3.9.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libnc-dap library is a call-for-call replacement for netcdf. It
can read and write to and from NetCDF files on the local machine and
it can read from DAP2 compatible data servers running on local or
remote machines. Data served using DAP2 need not be stored in NetCDF
files to be read using this replacement library.

Also included in this package is the ncdump utility, also bundled with
the original netcdf library, renamed dncdump, relinked with the
library and thus able to read from DAP2 compatible servers.

%description -l pl.UTF-8
Biblioteka libnc-dap to zamiennik biblioteki netcdf o identycznych
wywołaniach. Potrafi odczytywać i zapisywać pliki NetCDF na maszynie
lokalnej, a także czytać z serwerów danych zgodnych z DAP2
działających na lokalnej lub zdalnej maszynie. Dane serwowane przy
użyciu DAP2 nie muszą być zapisane w plikach NetCDF, aby były czytane
przez tę bibliotekę.

Dołączone jest także narzędzie ncdump (dołączane do oryginalnej
biblioteki netcdf), pod zmienioną nazwę dncdump i skonsolidowane z tą
biblioteką, dzięki czemu potrafi czytać z serwerów zgodnych z DAP2.

%package devel
Summary:	Header files for OPeNDAP NetCDF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OPeNDAP NetCDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdap-devel >= 3.9.2

%description devel
Header files for OPeNDAP NetCDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OPeNDAP NetCDF.

%package static
Summary:	Static OPeNDAP NetCDF library
Summary(pl.UTF-8):	Statyczna biblioteka OPeNDAP NetCDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OPeNDAP NetCDF library.

%description static -l pl.UTF-8
Statyczna biblioteka OPeNDAP NetCDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/ncdump $RPM_BUILD_ROOT%{_bindir}/dncdump

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog NEWS README*
%attr(755,root,root) %{_bindir}/dncdump
%attr(755,root,root) %{_libdir}/libnc-dap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnc-dap.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ncdap-config
%attr(755,root,root) %{_bindir}/ncdap-config-pkgconfig
%attr(755,root,root) %{_libdir}/libnc-dap.so
%{_includedir}/libnc-dap
%{_pkgconfigdir}/libnc-dap.pc
%{_aclocaldir}/libnc-dap.m4
%{_aclocaldir}/libnc-dap_header.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libnc-dap.a
