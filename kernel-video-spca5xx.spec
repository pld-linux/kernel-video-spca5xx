#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

Summary:	Linux driver for spca5xx
Summary(pl):	Sterownik dla Linuksa do spca5xx
Name:		kernel-video-spca5xx
%define		_snap 20050601
%define		_ver 0.56.03
Version:	%{_ver}
%define		_rel	0.%{_snap}.1
Release:	%{_rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://mxhaard.free.fr/spca50x/Download/spca5xx-%{_snap}.tar.gz
# Source0-md5:	c23af1747804ad283305d6004bb98f1a
Patch0:		spca5xx-build.patch
URL:		http://spca50x.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is version %{_ver} of the spca5xx Video for Linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This package contains Linux module.

%description -n kernel-video-spca5xx -l pl
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodaj�cego obs�ug� dla kamer i aparat�w opartych na uk�adach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Ten pakiet zawiera modu� j�dra Linuksa.

%package -n kernel-smp-video-spca5xx
Summary:	Linux SMP driver for spca5xx
Summary(pl):	Sterownik dla Linuksa SMP do spca5xx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-video-spca5xx
This is version %{_ver} the spca5xx video for linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This is driver for spca5xx for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-video-spca5xx -l pl
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodaj�cego obs�ug� dla kamer i aparat�w opartych na uk�adach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Sterownik dla Linuksa do spca5xx.

Ten pakiet zawiera modu� j�dra Linuksa SMP.

%prep
%setup -q -n spca5xx-%{_snap}
%patch0 -p1
mv RGB-YUV{%2f,-}module-setting

%build
%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1} \
		KERNEL_VERSION=%{__kernel_ver}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1} \
		KERNEL_VERSION=%{__kernel_ver}

	mv spca5xx{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/video
install spca5xx-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/spca5xx.ko
%if %{with smp} && %{with dist_kernel}
install spca5xx-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/spca5xx.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-video-spca5xx
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-video-spca5xx
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc CHANGELOG README README-TV8532 RGB-YUV-module-setting
/lib/modules/%{_kernel_ver}/video/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-video-spca5xx
%defattr(644,root,root,755)
%doc CHANGELOG README README-TV8532 RGB-YUV-module-setting
/lib/modules/%{_kernel_ver}smp/video/*.ko*
%endif
%endif
