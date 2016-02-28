%global srcname lz4

Name:           python-%{srcname}
Version:        0.7.0
Release:        6%{?dist}
URL:            https://github.com/steeve/%{name}
Summary:        LZ4 Bindings for Python
License:        BSD
Source:         https://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz

# This patch enables building against system lz4 and adds new functions to the class.
# https://github.com/steeve/python-lz4/pull/41
# Hopefully can be removed post 0.7.0
Patch0:         python-lz4-0.7.0-pr41.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  lz4-devel
BuildRequires:  python-nose
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose

%description
Python bindings for the lz4 compression library.

%package -n python2-lz4
Summary:        LZ4 Bindings for Python 2
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-lz4
Python 2 bindings for the lz4 compression library.


%package -n python3-lz4
Summary:        LZ4 Bindings for Python 3
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-lz4
Python 3 bindings for the lz4 compression library.


%prep
%autosetup -n %{srcname}-%{version} -p1

# Remove bundled lz4 as we're building against system lib
rm src/lz4*.[ch]


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install

# Fix permissions on shared objects
find %{buildroot}%{python3_sitearch} -name 'lz4*.so' \
    -exec chmod 0755 {} \;

find %{buildroot}%{python2_sitearch} -name 'lz4*.so' \
    -exec chmod 0755 {} \;


%check
# First we'll just try importing
PYTHONPATH=$RPM_BUILD_ROOT%{python2_sitearch} %{__python2} -c "import lz4"
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} %{__python3} -c "import lz4"

# And also run the tests included
%{__python2} setup.py test
%{__python3} setup.py test



%files -n python2-lz4
# Unfortunately there's no LICENSE/COPYING file included.
# Issue filed upstream:
# https://github.com/steeve/python-lz4/issues/38
%doc README.rst
%{python2_sitearch}/lz4*


%files -n python3-lz4
%doc README.rst
%{python3_sitearch}/lz4*


%changelog
* Sun Feb 28 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-6
- Spec file cleanup
- Add use of python_provide macro
- Remove python 3 conditional build - always build
- Use standard python packaging build and install macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.7.0-4
- Rebuilt for Python3.5 rebuild

* Mon Jun 29 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-3
- Update patch to build against system libs and add compress_fast method
- Add BR for python[3]-nose
- Run bundled test in %%check

* Sat Jun 27 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-2
- Drop unneeded Requires for lz4
- Remove commented out cruft from spec
- Regenerate setup.py patch to use libraries=["lz4"]
- Remove bundled lz4 code in %%prep

* Sat Jun 27 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-1
- Build against system lz4 libs
- Rudimentary check to see if we can import the module

* Sat Jun 27 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-0.2
- Include README.rst in python3 package as well

* Sat Jun 27 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-0.1
- Fix permissions of shared objects to be 0755

* Sat Jun 27 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.7.0-0
- Initial package for Fedora

