
%define plugin	burn
%define name	vdr-plugin-%plugin
%define version	0.1.0
%define prerel	pre21
%define rel	6
%define release	%mkrel 0.%prerel.%rel

Summary:	VDR plugin: Versatile convert-and-burn plugin
Name:		%name
Version:	%version
Release:	%release
Group:		Video
License:	GPL
URL:		http://www.magoa.net/linux/contrib/
Source:		http://www.magoa.net/linux/contrib/vdr-%plugin-%version-%prerel.tar.bz2
Patch1:		burn-0.1.0-pre21-jpackage-java.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.4.1-6
BuildRequires:	gd-devel
BuildRequires:	boost-devel
Requires:	vdr-abi = %vdr_abi
Requires:	vdrsync
Requires:	m2vrequantizer
Requires:	dvdauthor
Requires:	dvd+rw-tools
Requires:	mjpegtools
Requires:	pxsup2dast
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
%setup -q -c
cd %plugin
find -name CVS -print0 | xargs -0 rm -rf
%patch1 -p1 -b .java

%if %mdkversion >= 200710
perl -pi -e 's/mkisofs/genisoimage/' *.sh
perl -pi -e 's/cdrecord/wodim/' *.sh
%endif

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
# default: %{_localstatedir}/vdr/iso-images
var=ISO_DIR
param=--iso=ISO_DIR
%vdr_plugin_params_end

%build
cd %plugin
%vdr_plugin_build ISODIR=%{_localstatedir}/vdr/iso-images

%install
rm -rf %{buildroot}
cd %plugin
%vdr_plugin_install

install -d -m755 %{buildroot}%{_bindir}
install -m755 vdrburn-*.sh %{buildroot}%{_bindir}
install -m755 burn-buffers %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/skins

cp -a burn/* %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
install -d -m755 %{buildroot}%{_localstatedir}/vdr/iso-images
rm %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/counters/standard

%clean
rm -rf %{buildroot}

%post
%{_bindir}/gpasswd -a vdr cdrom >/dev/null
%{_bindir}/gpasswd -a vdr cdwriter >/dev/null
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin/%plugin.vdr
%defattr(-,root,root)
%doc %plugin/CONTRIBUTORS %plugin/HISTORY %plugin/README
%attr(-,vdr,vdr) %dir %{_vdr_plugin_cfgdir}/%{plugin}
%attr(-,vdr,vdr) %dir %{_vdr_plugin_cfgdir}/%{plugin}/counters
%attr(-,vdr,vdr) %dir %{_localstatedir}/vdr/iso-images
%{_vdr_plugin_cfgdir}/%{plugin}/skins
%{_vdr_plugin_cfgdir}/%{plugin}/*.mp2
%{_vdr_plugin_cfgdir}/%{plugin}/fonts
%{_vdr_plugin_cfgdir}/%{plugin}/*.png
%{_vdr_plugin_cfgdir}/%{plugin}/*.ini
%{_bindir}/vdrburn-archive.sh
%{_bindir}/vdrburn-dvd.sh
%{_bindir}/burn-buffers


