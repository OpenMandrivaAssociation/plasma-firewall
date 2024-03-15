%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

# (tpg) firewalld is default backend, disable it so ufw backend becomes default
%bcond_without firewalld

Name: plasma6-firewall
Version: 6.0.2
Release: %{?git:0.%{git}.}2
%if 0%{?git:1}
Source0: https://invent.kde.org/plasma/plasma-firewall/-/archive/%{gitbranch}/plasma-firewall-%{gitbranchd}.tar.bz2#/plasma-firewall-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{plasmaver}/plasma-firewall-%{version}.tar.xz
%endif
Summary: Firewall module for System Settings
URL: http://kde.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Xml)
BuildRequires: cmake(Plasma) >= 5.90.0
BuildRequires: cmake(PlasmaQuick) >= 5.90.0
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6Declarative)
BuildRequires: cmake(KF6Auth)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(PythonInterp)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Codecs)
BuildRequires: cmake(Qt6QmlModels)
BuildRequires: cmake(KF6Service)
BuildRequires: cmake(KF6Package)
Requires: iproute2
Requires: net-tools
%rename nx-firewall
%if %{with firewalld}
Requires: firewalld
%else
Requires: ufw
Requires: dbus-common
Requires: polkit
%endif

%description
Firewall module for System Settings.

%prep
%autosetup -p1 -n plasma-firewall-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
%if %{with firewalld}
	-DBUILD_FIREWALLD_BACKEND=ON \
	-DBUILD_UFW_BACKEND=OFF \
%else
	-DBUILD_FIREWALLD_BACKEND=OFF \
	-DBUILD_UFW_BACKEND=ON \
%endif
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# (tpg) get rid of UFW when it is not default firewall backend
%if %{with firewalld}
rm -rf %{buildroot}%{_libdir}/libexec/kauth/kde_ufw_plugin_helper
rm -rf %{buildroot}%{_libdir}/libexec/kde_ufw_plugin_helper.py
rm -rf %{buildroot}%{_qtdir}/plugins/kf6/plasma_firewall/ufwbackend.so
rm -rf %{buildroot}%{_datadir}/dbus-1/system-services/org.kde.ufw.service
rm -rf %{buildroot}%{_datadir}/dbus-1/system.d/org.kde.ufw.conf
rm -rf %{buildroot}%{_datadir}/kcm_ufw
rm -rf %{buildroot}%{_datadir}/polkit-1/actions/org.kde.ufw.policy
%endif

%find_lang %{name} --all-name --with-html

%files -f %{name}.lang
%if %{with firewalld}
%{_qtdir}/plugins/kf6/plasma_firewall/firewalldbackend.so
%else
%{_libdir}/libexec/kauth/kde_ufw_plugin_helper
%{_libdir}/libexec/kde_ufw_plugin_helper.py
%{_qtdir}/plugins/kf6/plasma_firewall/ufwbackend.so
%{_datadir}/dbus-1/system-services/org.kde.ufw.service
%{_datadir}/dbus-1/system.d/org.kde.ufw.conf
%{_datadir}/kcm_ufw
%{_datadir}/polkit-1/actions/org.kde.ufw.policy
%endif
%{_libdir}/libkcm_firewall_core.so
%{_datadir}/metainfo/org.kde.plasma.firewall.metainfo.xml
%{_qtdir}/plugins/plasma/kcms/systemsettings/kcm_firewall.so
%{_datadir}/applications/kcm_firewall.desktop
