%global makeflags PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SYSTEMDUNITDIR=%{_unitdir}

Name: earlyoom
Version: 1.6.2
Release: 2%{?dist}

License: MIT
URL: https://github.com/rfjakob/%{name}
Summary: Early OOM Daemon for Linux
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: pandoc
BuildRequires: gcc

%description
The oom-killer generally has a bad reputation among Linux users.
This may be part of the reason Linux invokes it only when it has
absolutely no other choice. It will swap out the desktop
environment, drop the whole page cache and empty every buffer
before it will ultimately kill a process. At least that's what
I think what it will do. I have yet to be patient enough to wait
for it, sitting in front of an unresponsive system.

%prep
%autosetup -p1
sed -e '/systemctl/d' -e 's/gzip -f -k .*/gzip -c $< > $@/' -i Makefile
%if 0%{?el7}
sed -e '/DynamicUser=/d' \
    -e 's/ProtectSystem=strict/ProtectSystem=full/' \
    -e 's/MemoryMax=/MemoryLimit=/' \
    -i earlyoom.service.in
%endif

%build
%set_build_flags
%make_build VERSION=%{version} %{makeflags}

%install
%make_install %{makeflags}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%config(noreplace) %{_sysconfdir}/default/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Fri Jul 10 2020 Massimiliano Torromeo <massimiliano.torromeo@gmail.com> - 1.6.1-1
- Updated to version 1.6.1

* Mon Mar 23 2020 Massimiliano Torromeo <massimiliano.torromeo@gmail.com> - 1.5-1
- Update to version 1.5.

* Tue Mar 03 2020 Massimiliano Torromeo <massimiliano.torromeo@gmail.com> - 1.4-2
- fixed systemd unit for el7

* Mon Mar 02 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.4-1
- Updated to version 1.4.

* Fri Feb 28 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.1-1
- Updated to version 1.3.1.

* Fri Feb 21 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3-4
- Rebuilt for Fedora 32.
- Backported security hardening patches.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3-2
- Forwarded version to compiled binary.

* Mon May 27 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3-1
- Updated to version 1.3.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2-1
- Updated to version 1.2.

* Wed Aug 15 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1-1
- Initial SPEC release.
