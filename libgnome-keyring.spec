#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	vala		# do not build Vala API
#
Summary:	libgnome-keyring library
Summary(pl.UTF-8):	Biblioteka libgnome-keyring
Name:		libgnome-keyring
Version:	3.8.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgnome-keyring/3.8/%{name}-%{version}.tar.xz
# Source0-md5:	caec6bcfac4d1fce6927c2338bdc5058
URL:		http://live.gnome.org/GnomeKeyring
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.16.0}
BuildRequires:	xz
Requires:	glib2 >= 1:2.16.0
Requires:	libgcrypt >= 1.2.2
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
Requires:	libgcrypt-devel >= 1.2.2
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

%package -n vala-libgnome-keyring
Summary:	libgnome-keyring API for Vala language
Summary(pl.UTF-8):	API libgnome-keyring dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0

%description -n vala-libgnome-keyring
libgnome-keyring API for Vala language.

%description -n vala-libgnome-keyring -l pl.UTF-8
API libgnome-keyring dla języka Vala.

%prep
%setup -q

%build
%{?with_apidocs:%{__gtkdocize}}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I build/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	%{__enable_disable vala vala} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%if %{without apidocs}
rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README
%attr(755,root,root) %{_libdir}/libgnome-keyring.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-keyring.so.0
%{_libdir}/girepository-1.0/GnomeKeyring-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-keyring.so
%{_datadir}/gir-1.0/GnomeKeyring-1.0.gir
%{_includedir}/gnome-keyring-1
%{_pkgconfigdir}/gnome-keyring-1.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-keyring
%endif

%if %{with vala}
%files -n vala-libgnome-keyring
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gnome-keyring-1.vapi
%endif
