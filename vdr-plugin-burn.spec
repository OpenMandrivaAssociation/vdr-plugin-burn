
%define plugin	burn
%define name	vdr-plugin-%plugin
%define version	0.2.0
%define prerel	beta4
%define rel	1
%define release	%mkrel 0.%prerel.%rel

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
BuildRoot:	%{_tmppath}/%{name}-buildroot
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
%if %mdkversion >= 200710
Requires:	cdrkit
Requires:	cdrkit-genisoimage
%endif
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

%if %mdkversion >= 200710
perl -pi -e 's/mkisofs/genisoimage/' *.sh
perl -pi -e 's/cdrecord/wodim/' *.sh
%endif

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

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/skins

cp -a burn/* %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{_localstatedir}/lib/vdr/iso-images
rm %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/counters/standard

%clean
rm -rf %{buildroot}

%post
%{_bindir}/gpasswd -a vdr cdrom >/dev/null
%{_bindir}/gpasswd -a vdr cdwriter >/dev/null
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc HISTORY README
%attr(-,vdr,vdr) %dir %{_vdr_plugin_cfgdir}/%{plugin}
%attr(-,vdr,vdr) %dir %{_vdr_plugin_cfgdir}/%{plugin}/counters
%attr(-,vdr,vdr) %dir %{_localstatedir}/lib/vdr/iso-images
%{_vdr_plugin_cfgdir}/%{plugin}/skins
%{_vdr_plugin_cfgdir}/%{plugin}/*.mp2
%{_vdr_plugin_cfgdir}/%{plugin}/fonts
%{_vdr_plugin_cfgdir}/%{plugin}/*.png
%{_vdr_plugin_cfgdir}/%{plugin}/*.ini
%{_bindir}/vdrburn-archive.sh
%{_bindir}/vdrburn-dvd.sh
%{_bindir}/burn-buffers


