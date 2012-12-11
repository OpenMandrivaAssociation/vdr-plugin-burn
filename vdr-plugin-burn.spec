
%define plugin	burn
%define name	vdr-plugin-%plugin
%define version	0.2.0
%define prerel	beta4
%define rel	2
%define release	0.%prerel.%rel

# backportability
%define _localstatedir %{_var}

Summary:	VDR plugin: Versatile convert-and-burn plugin
Name:		%name
Version:	%version
Release:	%release
Group:		Video
License:	GPL+
URL:		http://projects.vdr-developer.org/projects/plg-burn/
Source:		vdr-%plugin-%version-%prerel.tgz
Patch1:		burn-0.1.0-pre21-jpackage-java.patch
# add subtitle track descriptions also when no dvd menu is created (untested)
Patch9:		vdr-burn-subpicture-id-when-no-menu.patch
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	gd-devel
BuildRequires:	boost-devel
Requires:	vdr-abi = %vdr_abi
Requires:	vdrsync
Requires:	m2vrequantizer
Requires:	dvdauthor
Requires:	dvd+rw-tools
Requires:	mjpegtools
Requires:	eject
Suggests:	pxsup2dast
Requires:	cdrkit
Requires:	cdrkit-genisoimage
Requires(post):	vdr-common

%description
This Plugin enables VDR to write compliant DVDs from VDR recordings while
being able to control the process and to watch progress from inside VDRs
on-screen-display. If the selected recordings don't fit the DVD, the video
tracks are requantized (shrinked) automatically.

The created menus support multipage-descriptions (in case the recording
summary exceeds one page).

If you wish to have subtitles support, you have to install package
projectx and enable ProjectX in the plugin setup menu.

%prep
%setup -q -n %plugin-%version-%prerel
find -name CVS -print0 | xargs -0 rm -rf
%apply_patches

perl -pi -e 's/mkisofs/genisoimage/' *.sh
perl -pi -e 's/cdrecord/wodim/' *.sh

%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# directory for temporary files
# MUST be on UNIX filesystem
var=TEMPDIR
param=--tempdir=TEMPDIR
# directory for temporary datafiles
var=DATADIR
param=--datadir=DATADIR
# DVD writer
var=DVD_DEVICE
param=--dvd=DVD_DEVICE
# ISO image storage directory
# default: %{_localstatedir}/lib/vdr/iso-images
var=ISO_DIR
param=--iso=ISO_DIR
%vdr_plugin_params_end

%build
%vdr_plugin_build ISODIR=%{_localstatedir}/lib/vdr/iso-images

%install
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %{buildroot}%{_bindir}
install -m755 vdrburn-*.sh %{buildroot}%{_bindir}
install -m755 burn-buffers %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}/skins

cp -a burn/* %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{_localstatedir}/lib/vdr/iso-images
rm %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}/counters/standard

%post
%{_bindir}/gpasswd -a vdr cdrom >/dev/null
%{_bindir}/gpasswd -a vdr cdwriter >/dev/null
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc HISTORY README
%attr(-,vdr,vdr) %dir %{vdr_plugin_cfgdir}/%{plugin}
%attr(-,vdr,vdr) %dir %{vdr_plugin_cfgdir}/%{plugin}/counters
%attr(-,vdr,vdr) %dir %{_localstatedir}/lib/vdr/iso-images
%{vdr_plugin_cfgdir}/%{plugin}/skins
%{vdr_plugin_cfgdir}/%{plugin}/*.mp2
%{vdr_plugin_cfgdir}/%{plugin}/fonts
%{vdr_plugin_cfgdir}/%{plugin}/*.png
%{vdr_plugin_cfgdir}/%{plugin}/*.ini
%{_bindir}/vdrburn-archive.sh
%{_bindir}/vdrburn-dvd.sh
%{_bindir}/burn-buffers




%changelog
* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 0.2.0-0.beta4.1mdv2011.0
+ Revision: 576000
- new version 0.2.0-beta4
- new URL
- update license tag for current policy
- remove now unneeded patches (2,3,4,5,6,7,8,9)
- add subtitle description even when no menu is created
  (subpicture-id-when-no-menu.patch)
- rediff jpackage-java.patch

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre22.4mdv2011.0
+ Revision: 401088
- rebuild for new VDR

* Sat Mar 21 2009 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre22.3mdv2009.1
+ Revision: 359404
- rediff i18n-gettext.patch
- rebuild for new vdr
- define %%_localstatedir locally for backportability

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Mon Apr 28 2008 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre22.2mdv2009.0
+ Revision: 197906
- rebuild for new vdr

* Sat Apr 26 2008 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre22.1mdv2009.0
+ Revision: 197637
- 0.1.0-pre22
- add vdr_plugin_prep
- bump buildrequires on vdr-devel
- i18n fixes (P2 from e-tobi)
- requantizer fixes (P3 from e-tobi)
- adapt to gettext i18n of VDR 1.6 (P4 from e-tobi)
- add French translation (P5 from e-tobi)
- fix build with gcc 4.3 (P6 from Ville Skytt?\195?\164)
- fix charsets with VDR 1.5+ (P7 from Gentoo)
- adapt burn script for new projectx (P8)
- add subpicture ids to burned DVDs (P9 from Rolf Ahrenberg)
- requires eject
- suggests pxsup2dast instead of requiring it

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.8mdv2008.1
+ Revision: 145043
- rebuild for new vdr

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.7mdv2008.1
+ Revision: 144993
- rebuild for new vdr

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.6mdv2008.1
+ Revision: 103069
- rebuild for new vdr

* Sun Jul 08 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.5mdv2008.0
+ Revision: 49975
- rebuild for new vdr

* Thu Jun 21 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.4mdv2008.0
+ Revision: 42062
- rebuild for new vdr

* Sat May 05 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.3mdv2008.0
+ Revision: 22717
- rebuild for new vdr


* Fri Mar 23 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.2mdv2007.1
+ Revision: 148695
- require cdrkit-genisoimage

* Sun Jan 21 2007 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre21.1mdv2007.1
+ Revision: 111517
- 0.1.0-pre21
- rediff patch1
- drop patch2, applied upstream
- adapt buildrequires for new version
- require pxsup2dast explicitely
- adapt to cdrkit on Mandriva 2007.1

* Tue Dec 05 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.9mdv2007.1
+ Revision: 90897
- rebuild for new vdr
- add vdr user to cdwriter group

* Tue Oct 31 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.8mdv2007.1
+ Revision: 73961
- rebuild for new vdr
- Import vdr-plugin-burn

* Thu Sep 07 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.7mdv2007.0
- rebuild for new vdr

* Fri Sep 01 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.6mdv2007.0
- add vdr to cdrom group

* Thu Aug 24 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.5mdv2007.0
- stricter abi requires

* Mon Aug 07 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.4mdv2007.0
- rebuild for new vdr

* Wed Jul 26 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.3mdv2007.0
- rebuild for new vdr

* Thu Jul 20 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.2mdv2007.0
- fix buildrequires

* Tue Jul 18 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre20.1mdv2007.0
- 0.1.0-pre20
- add note about subtitles to description
- rediff patch1
- patch2: srt support

* Tue Jun 20 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-0.pre18.1mdv2007.0
- initial Mandriva release

