# TODO:
# - remove hardcoded paths from kernel log.
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_snap v4l1goodbye
%define		_ver 0.61.00
%define		_rel	0.%{_snap}.1
Summary:	Linux driver for spca5xx
Summary(pl.UTF-8):	Sterownik dla Linuksa do spca5xx
Name:		kernel%{_alt_kernel}-video-spca5xx
Version:	%{_ver}
Release:	%{_rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://mxhaard.free.fr/spca50x/Download/spca5xx-%{_snap}.tar.gz
# Source0-md5:	63bbe5d5c833f9b6b266fb58c54bf25e
Patch0:		spca5xx-build.patch
URL:		http://mxhaard.free.fr/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRequires:	sed >= 4.0
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is version %{_ver} of the spca5xx Video for Linux (v4l) driver,
providing support for webcams and digital cameras based on the spca5xx
range of chips manufactured by SunPlus Sonix Z-star Vimicro Conexant
Etoms and Transvision.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-video-spca5xx -l pl.UTF-8
To jest wersja %{_ver} sterownika Video for Linux (v4l) spca5xx
dodającego obsługę dla kamer i aparatów opartych na układach spca5xx
produkowanych przez SunPlus Sonix Z-star Vimicro Conexant Etoms and
Transvision.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n spca5xx-%{_snap}
%patch0 -p1
mv RGB-YUV{%2f,-}module-setting
%{__sed} -e '/#ifdef __KERNEL__/a#include <linux/version.h>\n#include <media/v4l2-dev.h>' \
    -i drivers/usb/spca5xx.h
%{__sed} -i -e 's/CFLAGS/EXTRA_CFLAGS/g' Makefile

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

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc CHANGELOG README-KERNEL-UPTO-2.6.16 readme README-TV8532 RGB-YUV-module-setting
/lib/modules/%{_kernel_ver}/kernel/drivers/media/video/spca5xx.ko*
%endif
