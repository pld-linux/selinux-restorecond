Summary:	restorecond - daemon which corrects contexts of newly created files
Summary(pl.UTF-8):	restorecond - demon poprawiający konteksty nowo tworzonych plików
Name:		selinux-restorecond
Version:	3.7
Release:	1
License:	GPL v2+
Group:		Daemons
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/restorecond-%{version}.tar.gz
# Source0-md5:	ef0f60e53adacd6c9377d02ac0dbd791
Patch0:		restorecond-init.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	pkgconfig
BuildRequires:	pcre-devel
BuildRequires:	libselinux-devel >= 3.7
BuildRequires:	rpmbuild(macros) >= 2.011
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	libselinux >= 3.7
Requires:	rc-scripts
Requires:	systemd-units >= 1:250.1
Obsoletes:	policycoreutils-restorecond < 2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number of
utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type Enforcement, Role-based Access Control, and
Multi-level Security.

restorecond daemon uses inotify to watch files listed in the
/etc/selinux/restorecond.conf, when they are created, this daemon will
make sure they have the correct file context associated with the
policy.

%description -l pl.UTF-8
Security-enhanced Linux jest prototypem jądra Linuksa i wielu
aplikacji użytkowych o funkcjach podwyższonego bezpieczeństwa.
Zaprojektowany jest tak, aby w prosty sposób ukazać znaczenie
obowiązkowej kontroli dostępu dla społeczności linuksowej. Ukazuje
również jak taką kontrolę można dodać do istniejącego systemu typu
Linux. Jądro SELinux zawiera nowe składniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeństwa systemu operacyjnego
Flask. Te elementy zapewniają ogólne wsparcie we wdrażaniu wielu typów
polityk obowiązkowej kontroli dostępu, włączając te wzorowane na: Type
Enforcement (TE), kontroli dostępu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

Demon restorecond używa inotify do śledzenia plików wymienionych w
pliku /etc/selinux/restorecond.conf, aby przy ich tworzeniu upewnić
się, że mają przypisane właściwe konteksty plików z polityki.

%prep
%setup -q -n restorecond-%{version}
%patch -P0 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -W" \
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir} \
	SYSTEMDSYSTEMUNITDIR=%{systemdunitdir} \
	SYSTEMDUSERUNITDIR=%{systemduserunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add restorecond
%service restorecond restart
%systemd_user_post restorecond_user.service

%preun
if [ "$1" = "0" ]; then
	%service restorecond stop
	/sbin/chkconfig --del restorecond
fi
%systemd_user_preun restorecond_user.service

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/restorecond
%attr(754,root,root) /etc/rc.d/init.d/restorecond
%{systemdunitdir}/restorecond.service
%{systemduserunitdir}/restorecond_user.service
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/selinux/restorecond.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/selinux/restorecond_user.conf
%{_mandir}/man8/restorecond.8*
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
