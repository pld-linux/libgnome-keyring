#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	libgnome-keyring library
Summary(pl.UTF-8):	Biblioteka libgnome-keyring
Name:		libgnome-keyring
Version:	2.29.4
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgnome-keyring/2.29/%{name}-%{version}.tar.bz2
# Source0-md5:	09e2fba1ffad767b7a2f678fc37f64aa
URL:		http://live.gnome.org/GnomeKeyring
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	eggdbus-devel >= 0.4
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
Conflicts:	gnome-keyring-libs < 2.29.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libgnome-keyring library is used by applications to integrate with
the gnome-keyring system.

%description -l pl.UTF-8
Biblioteka libgnome-keyring jest używana w celu zintegrowania
aplikacji z systemem gnome-keyring.

%package devel
Summary:	Header files for libgnome-keyring library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgnome-keyring
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.16.0
Conflicts:	gnome-keyring-devel < 2.29.0

%description devel
Header files for libgnome-keyring library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgnome-keyring.

%package apidocs
Summary:	libgnome-keyring library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgnome-keyring
Group:		Documentation
Requires:	gtk-doc-common
Conflicts:	gnome-keyring-apidocs < 2.29.0

%description apidocs
libgnome-keyring library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgnome-keyring.

%prep
%setup -q

%build
%{?with_apidocs:%{__gtkdocize}}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{without apidocs}
rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README
%attr(755,root,root) %{_libdir}/libgnome-keyring.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-keyring.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-keyring.so
%{_libdir}/libgnome-keyring.la
%{_includedir}/gnome-keyring-1
%{_pkgconfigdir}/gnome-keyring-1.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-keyring
%endif
