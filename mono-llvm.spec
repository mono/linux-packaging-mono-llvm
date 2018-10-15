#
# spec file for package mono-llvm
#
# Copyright (c) 2018 Microsoft
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.



Name:           mono-llvm
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake3
BuildRequires:  python34
%if 0%{?rhel} < 7
BuildRequires:  devtoolset-2-toolchain
%endif
Url:            http://www.mono-project.com/docs/advanced/mono-llvm/
Version:	6.0+mono20180728010642
Release:	0.xamarin.9
Summary:        LLVM fork for Mono
License:        MIT and others
Group:          Development/Tools/IDE
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Requires:       mono-llvm-tools = %{version}
Requires:       mono-llvm-devel = %{version}
Dummy package for mono-llvm

%package tools
Summary:        Runtime files for Mono LLVM fork
Group:          Development/Languages/Mono

%description tools
Mono LLVM fork, tools needed for runtime

%package devel
Summary:        Development files for Mono LLVM fork
Group:          Development/Languages/Mono
Requires:       mono-llvm-tools = %{version}

%description devel
MonoDevelop is a full-featured integrated development
environment (IDE) for Mono and Gtk-Sharp. It was originally
a port of SharpDevelop 0.98.

This package contains development files for the IDE and plugins.

%prep
%setup -q -n mono-llvm-6.0

%build
%{?scl:scl enable %{scl} - << \EOF}
which g++
mkdir buildybuild/
cd buildybuild/
cmake3 -DLLVM_TARGETS_TO_BUILD="X86" -DLLVM_ENABLE_ASSERTIONS="ON" -DCMAKE_BUILD_TYPE="Release" -DCMAKE_INSTALL_PREFIX=%{_prefix}/lib/mono/llvm/ ..
make all
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
cd buildybuild/ && cmake3 -DPYTHON_EXECUTABLE="/usr/bin/python3" -DCMAKE_INSTALL_PREFIX=%{?buildroot}/%{_prefix}/lib/mono/llvm/ -P cmake_install.cmake
%{?scl:EOF}

%files tools
%defattr(-,root,root)
%{_prefix}/lib/mono/llvm/bin/opt
%{_prefix}/lib/mono/llvm/bin/llc

%files devel
%defattr(-,root,root)
%exclude %{_prefix}/lib/mono/llvm/bin/opt
%exclude %{_prefix}/lib/mono/llvm/bin/llc
%{_prefix}/lib/mono/llvm/*

%changelog

