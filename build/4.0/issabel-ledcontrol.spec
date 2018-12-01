%define modname ledcontrol

Summary: Issabel Led Control for UCR Micro
Name:    issabel-%{modname}
Version: 4.0.0
Release: 1
License: GPL
Group:   Applications/System
Source0: %{modname}_%{version}-%{release}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires(pre): issabel-framework >= 2.3.0-5
Requires: issabel-system

%description
Issabel Led Control for Issabel UCR Micro appliance

%prep
%setup -n %{name}_%{version}-%{release}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p    $RPM_BUILD_ROOT/usr/local/bin
mv setup/usr/local/bin/ledcontrol  $RPM_BUILD_ROOT/usr/local/bin

%pre

%post

# rules udev
echo 'KERNEL=="sd[a-z]*[0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/usr/local/bin/ledcontrol USBON"' >>/etc/udev/rules.d/99-local.rules
echo 'KERNEL=="sd[a-z]*[0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/usr/local/bin/ledcontrol USBOFF"' >>/etc/udev/rules.d/99-local.rules
echo 'KERNEL=="mmcblk0", SUBSYSTEMS=="block", ACTION=="add", RUN+="/usr/local/bin/ledcontrol TFON"' >>/etc/udev/rules.d/99-local.rules
echo 'KERNEL=="mmcblk0", SUBSYSTEMS=="block", ACTION=="remove", RUN+="/usr/local/bin/ledcontrol TFOFF"' >>/etc/udev/rules.d/99-local.rules
udevadm control --reload-rules

%clean
rm -rf $RPM_BUILD_ROOT

%preun

if [ $1 -eq 0 ] ; then # Validation for desinstall this rpm
# rules udev

sed -i "/ledcontrol USBON/d" /etc/udev/rules.d/99-local.rules
sed -i "/ledcontrol USBOFF/d" /etc/udev/rules.d/99-local.rules
sed -i "/ledcontrol TFON/d" /etc/udev/rules.d/99-local.rules
sed -i "/ledcontrol TFOFF/d" /etc/udev/rules.d/99-local.rules
udevadm control --reload-rules

fi

%files
%defattr(0755, root, root)
/usr/local/bin/ledcontrol

%changelog
