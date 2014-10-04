Summary:	Virtual lighttable and darkroom for photographers
Name:		darktable
Version:	1.4.2
Release:	1
License:	GPL v3
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/darktable/%{name}-%{version}.tar.xz
# Source0-md5:	f86554329c2c809ffb009244a6f1d643
Patch0:		%{name}-kill-native.patch
URL:		http://darktable.org/
BuildRequires:	GraphicsMagick-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	exiv2-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	lcms2-devel
BuildRequires:	lensfun-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgomp-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libwebp-devel
BuildRequires:	libxml2-devel
BuildRequires:	lua52-devel
BuildRequires:	sqlite3-devel
BuildRequires:	zlib-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
darktable is an open source photography workflow application and RAW
developer. A virtual lighttable and darkroom for photographers.
It manages your digital negatives in a database, lets you view them
through a zoomable lighttable and enables you to develop raw images
and enhance them.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's/^[ \t]*//' data/%{name}.desktop

%build
install -d build
cd build
%cmake .. \
	-DBUILD_CMSTEST=ON				\
	-DDONT_INSTALL_GCONF_SCHEMAS=ON			\
	-DLENSFUN_INCLUDE_DIR=%{_includedir}/lensfun	\
	-DUSE_GCONF_BACKEND=OFF
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/darktable/{plugins,plugins/*,plugins/*/*,views}/*.la
%{__mv} $RPM_BUILD_ROOT%{_localedir}/pt{_PT,}

%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/darktable.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/{AUTHORS,ChangeLog,NEWS,README,TODO}
%attr(755,root,root) %{_bindir}/darktable
%attr(755,root,root) %{_bindir}/darktable-cli
%attr(755,root,root) %{_bindir}/darktable-cltest
%attr(755,root,root) %{_bindir}/darktable-cmstest
%attr(755,root,root) %{_bindir}/darktable-viewer

%dir %{_libdir}/darktable
%attr(755,root,root) %{_libdir}/darktable/libdarktable.so

%dir %{_libdir}/darktable/plugins
%dir %{_libdir}/darktable/plugins/imageio
%dir %{_libdir}/darktable/plugins/imageio/format
%dir %{_libdir}/darktable/plugins/imageio/storage
%dir %{_libdir}/darktable/plugins/lighttable
%attr(755,root,root) %{_libdir}/darktable/plugins/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/format/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/storage/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/lighttable/*.so

%dir %{_libdir}/darktable/views
%attr(755,root,root) %{_libdir}/darktable/views/*.so

%{_datadir}/%{name}
%{_desktopdir}/darktable.desktop
%{_iconsdir}/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/darktable*.1*

