#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	JOSE implementation for C
Summary(pl.UTF-8):	Implementacja JOSE dla C
Name:		cjose
Version:	0.6.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/cisco/cjose/releases
Source0:	https://github.com/cisco/cjose/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7618e839ea0ecfa38355fa7f58391f88
URL:		https://github.com/cisco/cjose
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	check-devel >= 0.9.4
%{?with_apidocs:BuildRequires:	doxygen >= 1.8}
BuildRequires:	gcc >= 6:4.5
BuildRequires:	jansson-devel >= 2.3
BuildRequires:	libtool >= 2:2.2
BuildRequires:	make >= 3.81
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig >= 1:0.20
Requires:	jansson >= 2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of JOSE (JavaScript Object Signing and Encryption) for
C/C++.

%description -l pl.UTF-8
Implementacja JOSE (JavaScript Object Signing and Encryption) dla
C/C++.

%package devel
Summary:	Header files for cjose library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cjose
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jansson-devel >= 2.3
Requires:	openssl-devel >= 1.0.1

%description devel
Header files for cjose library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cjose.

%package static
Summary:	Static cjose library
Summary(pl.UTF-8):	Statyczna biblioteka cjose
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cjose library.

%description static -l pl.UTF-8
Statyczna biblioteka cjose.

%package apidocs
Summary:	API documentation for cjose library
Summary(pl.UTF-8):	Dokumentacja API biblioteki cjose
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for cjose library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki cjose.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-doxygen-doc} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcjose.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libcjose.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcjose.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcjose.so
%{_includedir}/cjose
%{_pkgconfigdir}/cjose.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcjose.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{search,*.css,*.html,*.png}
%endif
