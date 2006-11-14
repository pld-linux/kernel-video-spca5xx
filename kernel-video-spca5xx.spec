# TODO:
# - remove hardcoded paths from kernel log.
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

# see kernel.spec
%ifarch sparc
%undefine	with_smp
%endif

%define		_snap 20060501
%define		_ver 0.60.00
%define		_rel	0.%{_snap}.1
Summary:	Linux driver for spca5xx
Summary(pl):	Sterownik dla Linuksa do spca5xx
Name:		kernel%{_alt_kernel}-video-spca5xx
Version:	%{_ver}
Release:	%{_rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://mxhaard.free.fr/spca50x/Download/spca5xx-%{_snap}.tar.gz
# Source0-md5:	8fcec25715aea10f9ebec5728c37e752
Patch0:		spca5xx-build.patch
URL:		http://mxhaard.free.fr/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	sed >= 4.0
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

%description -n kernel%{_alt_kernel}-video-spca5xx -l pl
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodaj±cego obs³ugê dla kamer i aparatów opartych na uk³adach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-video-spca5xx
Summary:	Linux SMP driver for spca5xx
Summary(pl):	Sterownik dla Linuksa SMP do spca5xx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-video-spca5xx
This is version %{_ver} the spca5xx video for linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This is driver for spca5xx for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-video-spca5xx -l pl
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodaj±cego obs³ugê dla kamer i aparatów opartych na uk³adach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Sterownik dla Linuksa do spca5xx.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n spca5xx-%{_snap}
%patch0 -p1
mv RGB-YUV{%2f,-}module-setting
sed -e '/#ifdef __KERNEL__/a#include <linux/version.h>' \
    -i drivers/usb/spca5xx.h

%build
%if %{with kernel}
%build_kernel_modules -m spca5xx
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m spca5xx -d kernel/drivers/media/video
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-video-spca5xx
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-video-spca5xx
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc CHANGELOG README README-TV8532 RGB-YUV-module-setting
/lib/modules/%{_kernel_ver}/kernel/drivers/media/video/spca5xx.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-video-spca5xx
%defattr(644,root,root,755)
%doc CHANGELOG README README-TV8532 RGB-YUV-module-setting
/lib/modules/%{_kernel_ver}smp/kernel/drivers/media/video/spca5xx.ko*
%endif
%endif
