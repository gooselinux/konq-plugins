# Review Request: http://bugzilla.redhat.com/438126

Name:           konq-plugins
Version:        4.3.3
Release:        5%{?dist}
Summary:        Additional plugins that interact with konqueror

Group:          Applications/Internet
License:        GPLv2+ and LGPLv2+
URL:            http://extragear.kde.org
Source0:        ftp://ftp.kde.org/pub/kde/stable/%{version}/src/extragear/konq-plugins-%{version}.tar.bz2
Patch0:         konq-plugins-4.3.3-webkit_found.patch
Patch1:         konq-plugins-4.3.3-desktopfiles.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: gettext
BuildRequires: kdebase4-devel >= %{version}

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires:      kdebase4%{?_isa} >= %{version}
Requires:      %{name}-doc = %{version}-%{release}

%description
Some additional plugins that interact with konqueror
* adblock: AdBlock plugin
* akregator: Add feeds directly to akregator (kdepim is needed)
* autorefresh: Refresh websites after a specifig period
* babelfish: Translate a website with babelfish
* crashes: Crash monitor
* dirfilter: Filter the current directory in many ways
* domtreeviewer: Displays the document object model in a box
* fsview: Graphical Disk Usage for inode/directory
* imagerotation: service menu to image operations
* khtmlsettingsplugin: Enable/disable some HTML settings
* kimggalleryplugin:  Creates an HTML page with thumbnails of
  all the images in the current directory.
* mediarealfolder:  service menu to open a medium mountpoints
* minitools: Implement bookmarklets into konqueror
* rellinks: Allows access to relations defined in the header of a document
* searchbar: Search Bar
* sidebar: a small embedded mediaplayer, for songs/video preview
* smbmounter: provides two menus items to smbmount/umount samba shares
* uachanger: Change the user agent for websites
* validators: Website validators
* webarchiver: Web Archiver


%package doc
Group:          System Environment/Libraries
Summary:        Documentation files for konq-plugins
BuildArch:      noarch

%description doc
This package includes the documentation for konq-plugins.

%prep
%setup -q
%patch0 -p1 -b webkit_found
%patch1 -p1 -b .desktopfiles


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --all-name

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING COPYING.DOC COPYING.LIB README
%{_kde4_bindir}/fsview
%{_datadir}/config/translaterc
# co-owned with kdepim, since there's no shared dep
%{_kde4_appsdir}/akregator/
%{_kde4_appsdir}/dolphinpart/kpartplugins/*
%{_kde4_appsdir}/domtreeviewer/
%{_kde4_appsdir}/fsview/
%{_kde4_appsdir}/khtml/kpartplugins/*
%{_kde4_appsdir}/konqueror/icons/*
%{_kde4_appsdir}/konqueror/kpartplugins/*
%{_kde4_appsdir}/konqueror/opensearch/*
%{_kde4_datadir}/config.kcfg/validators.kcfg
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/*.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_libdir}/kde4/*.so


%files doc
%defattr(-,root,root,-)
%{_docdir}/HTML/*/konq-plugins/

%changelog
* Fri Jun 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.3.3-5
- Resolves: #605069 - RPMdiff run failed for package konq-plugins-4.3.3-3.el6
  (sanitize .desktop files)

* Thu Jun 17 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.3.3-4
- Resolves: #605069 - RPMdiff run failed for package konq-plugins-4.3.3-3.el6
  (create a noarch doc subpackage to fix multilib issues)

* Fri Dec 18 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.3.3-3
- do not install KDE webkitpart files in RHEL

* Mon Nov 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-2
- BR: webkitpart-devel >= 0.0.2

* Sat Nov 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 26 2009 Than Ngo <than@redhat.com> - 4.3.1-3
- rhel cleanup

* Sun Sep 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- BR: webkitpart-devel
- use %%find_lang --all-names --with-kde
- Requires: kdebase4%%{_?isa} >= %%version

* Tue Sep 01 2009 Sebastian Vahl <svahl@fedoraproject.org> - 4.3.1-1
- 4.3.1
- use scriplet for HTML docdirs

* Tue Aug 11 2009 Sebastian Vahl <fedora@deadbabylon.de> 4.3.0-1
* KDE 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.3-1
- 4.2.3

* Tue Apr  7 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Wed Mar 25 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-4
- fixup handbook install
- optimize scriptlets

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-2
- update %%description
- Requires: kdebase4 >= 4.2

* Fri Jan 23 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Mon Jan 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.1.3-4
- make install/fast
- jpegorient is not installed (#478736, kdebug#178612)

* Sun Dec 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.3-3
- rebuild for Python 2.6 (contains Python bytecode despite no dependencies)

* Tue Nov 11 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.1.3-2
- include adblock language files

* Tue Nov 11 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.1.3-1
- 4.1.3

* Sat Oct 04 2008 Than Ngo <than@redhat.com> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Thu Aug 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.1.0-2
- fix data files from akregator plugin not getting installed

* Wed Aug 06 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.1.0-1
- 4.1.0
- drop searchbar-crash patch (no longer needed with Konqueror 4.1)

* Sun May 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.3-0.3.20080409svn
- fix searchbar plugin crash (#445144)

* Wed Apr 16 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.3-0.2.20080409svn
- rebuild because of corrupt PPC RPM causing signing failure (#442761)

* Wed Apr 09 2008 Sebastian Vahl <fedora@deadbabylon.de> - 4.0.3-0.1.20080409svn
- new svn checkout
- some minor spec cleanups
- License: GPLv2+ and LGPLv2+
- drop icons patch

* Tue Apr 01 2008 Sebastian Vahl <fedora@deadbabylon.de> - 4.0.2-0.2.20080303svn
- rebuild for NDEBUG and _kde4_libexecdir
- enhance %%description a bit

* Wed Feb 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 4.0.2-0.1.20080303svn
- new svn checkout (for KDE 4.0.2)
- update cmakelists patch
- remove icons patch (not needed anymore)
- add "svn" to release

* Wed Feb 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 4.0.1-0.2.20080214svn
- added konq-plugins-4.0.1-icons.patch
- add .po files to tarball

* Wed Feb 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 4.0.1-0.1.20080213svn
- initial version
