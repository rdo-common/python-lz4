%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

%global srcname lz4

Name:           python-%{srcname}
Version:        0.7.0
Release:        2%{?dist}
URL:            https://github.com/steeve/%{name}
Summary:        LZ4 Bindings for Python
License:        BSD
Source:         https://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz

# Build against system lz4 libs rather than bundled libs
Patch0:         python-lz4-systemlib.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  lz4-devel

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Python2 bindings for the lz4 compression library.


%if %{with python3}
%package -n python3-lz4
Summary:        LZ4 Bindings for Python3

%description -n python3-lz4
Python3 bindings for the lz4 compression library.
%endif # with python3


%prep
%setup -qc

# Python 2
mv %{srcname}-%{version} python2
pushd python2
# Remove bundled lz4 and build against system lib
%patch0 -p1
rm src/lz4*.[ch]
popd

# copy common doc files to top dir
cp -pr python2/README.rst .

# Python3
%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
popd

%if %{with python3}
pushd python3
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with python3


%install
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
# Fix permissions on shared objects
find %{buildroot}%{python3_sitearch} -name 'lz4*.so' \
    -exec chmod 0755 {} \;
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# Fix permissions on shared objects
find %{buildroot}%{python2_sitearch} -name 'lz4*.so' \
    -exec chmod 0755 {} \;
popd


%check
# No test suite at present, so we'll just try importing
PYTHONPATH=$RPM_BUILD_ROOT%{python2_sitearch} %{__python2} -c "import lz4"
%if %{with python3}
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} %{__python3} -c "import lz4"
%endif

%files
# Unfortunately there's no LICENSE/COPYING file included.
# Issue filed upstream:
# https://github.com/steeve/python-lz4/issues/38
%doc README.rst
%{python2_sitearch}/lz4*

%if %{with python3}
%files -n python3-lz4
%doc README.rst
%{python3_sitearch}/lz4*
%endif

%changelog
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
