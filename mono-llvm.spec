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
%if 0%{?rhel} < 8
BuildRequires:  python34
%else
BuildRequires:  python36
%endif
%if 0%{?rhel} < 7
BuildRequires:  devtoolset-2-toolchain
%endif
Url:            http://www.mono-project.com/docs/advanced/mono-llvm/
Version:	6.0+mono20190308102247b
Release:	0.nightly.2
Summary:        LLVM fork for Mono
License:        MIT and others
Group:          Development/Tools/IDE
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define debug_package %{nil}

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
Mono LLVM fork, tools needed for build time

%prep
%setup -q -n mono-llvm-6.0

%build
%{?scl:scl enable %{scl} - << \EOF}
which g++
mkdir buildybuild/
cd buildybuild/
cmake3 \
	-DLLVM_TARGETS_TO_BUILD="Native" \
	-DLLVM_ENABLE_ASSERTIONS="OFF" \
	-DCMAKE_BUILD_TYPE="Release" \
	-DLLVM_BUILD_TESTS="OFF" \
	-DLLVM_INCLUDE_TESTS="OFF" \
	-DLLVM_BUILD_EXAMPLES="OFF" \
	-DLLVM_INCLUDE_EXAMPLES="OFF" \
	-DPYTHON_EXECUTABLE:FILEPATH="/usr/bin/python3" \
	-DLLVM_TOOLS_TO_BUILD="opt;llc;llvm-config;llvm-dis" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix}/lib/mono/llvm/ ..
make all
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
cd buildybuild/ && cmake3 -DCMAKE_INSTALL_PREFIX=%{?buildroot}/%{_prefix}/lib/mono/llvm/ -P cmake_install.cmake
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

