%define debug_package %{nil}
%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: plasma-firewall
Version: 5.21.0
Release: 1
Source0: http://download.kde.org/%{stable}/plasma/%{plasmaver}/%{name}-%{version}.tar.xz
Summary: Firewall module for System Settings
URL: http://kde.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Xml)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: cmake(KF5Plasma)
BuildRequires: cmake(KF5PlasmaQuick)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5Declarative)
BuildRequires: cmake(KF5Auth)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(PythonInterp)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5KCMUtils)
BuildRequires: cmake(KF5Codecs)
BuildRequires: cmake(Qt5QmlModels)
BuildRequires: cmake(KF5Service)
BuildRequires: cmake(KF5Package)

%description
Firewall module for System Settings

%prep
%autosetup -p1
%cmake_kde5

%build
%ninja_build -C build

%install
%ninja_install -C build
%find_lang %{name} --all-name --with-html

%files -f %{name}.lang
%{_libdir}/libexec/kauth/kde_ufw_plugin_helper
%{_libdir}/libexec/kde_ufw_plugin_helper.py
%{_libdir}/libkcm_firewall_core.so
%{_libdir}/qt5/plugins/kcms/kcm_firewall.so
%{_libdir}/qt5/plugins/kf5/plasma_firewall/firewalldbackend.so
%{_libdir}/qt5/plugins/kf5/plasma_firewall/ufwbackend.so
%{_datadir}/dbus-1/system-services/org.kde.ufw.service
%{_datadir}/dbus-1/system.d/org.kde.ufw.conf
%{_datadir}/kcm_ufw
%{_datadir}/kpackage/kcms/kcm_firewall
%{_datadir}/kservices5/kcm_firewall.desktop
%{_datadir}/metainfo/org.kde.plasma.firewall.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.ufw.policy