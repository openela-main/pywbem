Name:           pywbem
Version:        0.11.0
Release:        8%{?dist}
Summary:        Python WBEM Client and Provider Interface
Group:          Development/Libraries
License:        LGPLv2
URL:            https://github.com/pywbem/pywbem
Source0:        https://github.com/pywbem/pywbem/archive/v%{version}.tar.gz

BuildRequires:  python3-pip python3-PyYAML python3-ply python3-devel
BuildArch:      noarch

# Remove python-twisted module, we don't want twisted in RHEL
Patch1: pywbem-remove-twisted.patch

%global _description\
A Python library for making CIM (Common Information Model) operations over HTTP\
using the WBEM CIM-XML protocol. It is based on the idea that a good WBEM\
client should be easy to use and not necessarily require a large amount of\
programming knowledge. It is suitable for a large range of tasks from simply\
poking around to writing web and GUI applications.\
\
WBEM, or Web Based Enterprise Management is a manageability protocol, like\
SNMP, standardized by the Distributed Management Task Force (DMTF) available\
at http://www.dmtf.org/standards/wbem.\
\
It also provides a Python provider interface, and is the fastest and\
easiest way to write providers on the planet.

%description %_description

%package -n python3-pywbem
Group:          Development/Libraries
Summary:        Python3 WBEM Client and Provider Interface
BuildArch:      noarch
Requires:       python3-PyYAML python3-six python3-ply

%description -n python3-pywbem
A WBEM client allows issuing operations to a WBEM server, using the CIM
operations over HTTP (CIM-XML) protocol defined in the DMTF standards DSP0200
and DSP0201. The CIM/WBEM infrastructure is used for a wide variety of systems
management tasks supported by systems running WBEM servers. See WBEM Standards
for more information about WBEM.

%prep
%setup -q -n %{name}-%{version}
%if 0%{?rhel}
%patch1 -p1
%endif

%build
CFLAGS="%{optflags}" %{__python3} setup.py build

%install

env PYTHONPATH=%{buildroot}/%{python3_sitelib} %{__python3} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}/usr/bin/*.bat
# wbemcli are conflicting with sblim-wbemcli
mv -v %{buildroot}/%{_bindir}/wbemcli %{buildroot}/%{_bindir}/pywbemcli
sed -i -e 's/wbemcli/pywbemcli/' %{buildroot}/%{_bindir}/pywbemcli
mv -v %{buildroot}/%{_bindir}/wbemcli.py %{buildroot}/%{_bindir}/pywbemcli.py

%files -n python3-pywbem
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/pywbem/
%{_bindir}/mof_compiler
%{_bindir}/pywbemcli
%{_bindir}/pywbemcli.py
%doc README.rst

%changelog
* Wed Nov 6 2019 Tony Asleson <tasleson@redhat.com> - 0.11.0-8
- Fix the conflict with sblim-wbemcli: RHBZ #1757855
- Corrected warning about multiple file inclusion

* Wed Jun 13 2018 Petr Viktorin <pviktori@redhat.com> - 0.11.0-7
- Drop the python2 subpackage

* Tue May 22 2018 Josh Boyer <jwboyer@redhat.coml - 0.11.0-6
- Remove python-twisted dependency (RHBZ 1561647)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 Lumír Balhar <lbalhar@redhat.com> - 0.11.0-4
- Fix directory ownership

* Thu Oct 19 2017 Gris Ge <fge@redhat.com> - 0.11.0-3
- Fedora 25 does not have python2-pip, use python-pip instead.

* Thu Oct 19 2017 Gris Ge <fge@redhat.com> - 0.11.0-2
- Add missing runtime dependency python2-ply and python3-ply

* Wed Oct 11 2017 Gris Ge <fge@redhat.com> - 0.11.0-1
- Upgrade to 0.11.0

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-3
- Python 2 binary package renamed to python2-pywbem
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Gris Ge <fge@redhat.com> - 0.10.0-1
- Upgrade to 0.10.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-2
- Rebuild for Python 3.6

* Thu Dec 08 2016 Gris Ge <fge@redhat.com> 0.9.1-1
- Upgrade to 0.9.1

* Wed Oct 19 2016 Gris Ge <fge@redhat.com> 0.9.0-3
- Add missing runtime dependency python3-six and python-six

* Tue Sep 27 2016 Gris Ge <fge@redhat.com> 0.9.0-2
- Add missing runtime dependency python3-PyYAML and PyYAML.

* Wed Sep 14 2016 Gris Ge <fge@redhat.com> - 0.9.0-1
- Upgrade to 0.9.0 and add python3 pacakge -- python3-pywbem.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-30.20131121svn626
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-29.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-28.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.0-27.svn
- Replace python-setuptools-devel BR with python-setuptools

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-26.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Michal Minar <miminar@redhat.com> 0.7.0-25.20131121svn656
- Fixed local authentication under root.

* Thu Jan 23 2014 Michal Minar <miminar@redhat.com> 0.7.0-24.20131121svn656
- Added support for non-ascii strings.

* Fri Jan 03 2014 Michal Minar <miminar@redhat.com> 0.7.0-23.20131121svn656
- Skip hostname check when no verification is desired.

* Fri Dec 27 2013 Michal Minar <miminar@redhat.com> 0.7.0-22.20131121svn656
- Work around M2Crypto's inability to handle unicode strings.

* Wed Dec 18 2013 Michal Minar <miminar@redhat.com> 0.7.0-21.20131121svn656
- Adjusted default certificates paths searched for cert validation.

* Tue Dec 17 2013 Michal Minar <miminar@redhat.com> 0.7.0-20.20131121svn656
- Tweaked the ssl_verify_host patch.

* Mon Dec 16 2013 Michal Minar <miminar@redhat.com> 0.7.0-18.20131121svn656
- Fixes TOCTOU vulnerability in certificate validation.
- Resolves: rhbz#1026891

* Thu Nov 21 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-17.20131121svn626
- Added '-d' option to /usr/bin/mofcomp to just check mof files and their
  includes.

* Tue Aug 27 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-16.20130827svn625
- Fixed parsing of IPv6 addresses.

* Fri Aug 09 2013 Michal Minar <miminar@redhat.com> 0.7.0-15.20130723svn623
- Fixed certificate verification issue.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-14.20130723svn623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013  <jsafrane@redhat.com> 0.7.0-13.20130702svn623
- Added subpackage with Twisted module to reduce dependencies of the main package.

* Tue Jul 23 2013  <jsafrane@redhat.com> 0.7.0-12.20130702svn623
- Fixed checking of CIMVERSION in CIM-XML.

* Tue Jul  2 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-11.20130702svn622
- New upstream version.
- Method parameters are now case-insensitive.

* Fri May 24 2013 Tomas Bzatek <tbzatek@redhat.com> 0.7.0-10.20130411svn619
- Fix module imports in /usr/bin/mofcomp

* Thu Apr 11 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-9.20130411svn619
- New upstream version.
- Removed debug 'print' statements.

* Mon Jan 28 2013 Michal Minar <miminar@redhat.com> 0.7.0-8.20130128svn613
- New upstream version.
- Added post-release snapshot version info.
- Removed obsoleted BuildRoot,

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jan 01 2010 David Nalley <david@gnsa.us> 0.7.0-3
- refined requires for epel compat
* Sun Jun 28 2009 David Nalley <david@gnsa.us> 0.7.0-2
- Added some verbiage regarding what WBEM is and expanding WBEM and CIM acronyms
- Added python-twisted as a dependency
* Thu Jun 25 2009 David Nalley <david@gnsa.us> 0.7.0-1
- Initial packaging

