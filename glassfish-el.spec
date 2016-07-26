%global pkg_name glassfish-el
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global artifactId javax.el

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.2.5
Release:        6.6%{?dist}
Summary:        J2EE Expression Language Implementation
License:        CDDL or GPLv2 with exceptions
URL:            http://uel.java.net
# svn export https://svn.java.net/svn/uel~svn/tags/javax.el-2.2.5/ javax.el-2.2.5
# tar cvJf javax.el-2.2.5.tar.xz javax.el-2.2.5/
Source0:        %{artifactId}-%{version}.tar.xz
Source1:        generate_tarball.sh
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}jvnet-parent
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}maven
BuildRequires:  %{?scl_prefix}maven-source-plugin
BuildRequires:  %{?scl_prefix}mvn(javax.el:javax.el-api)

%description
This project provides an implementation of the Expression Language (EL).
The main goals are:
 * Improves current implementation: bug fixes and performance improvements
 * Provides API for use by other tools, such as Netbeans

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{artifactId}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

%mvn_file : %{pkg_name}
%mvn_alias : "org.eclipse.jetty.orbit:com.sun.el"
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-6.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.2.5-6
- Mass rebuild 2013-12-27

* Thu Aug 22 2013 Michal Srb <msrb@redhat.com> - 2.2.5-5
- Migrate away from mvn-rpmbuild (Resolves: #997471)

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 2.2.5-4
- Add generate_tarball.sh script to SRPM

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-2
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#918514

* Fri Feb 1 2013 David Xie <david.scriptfan@gmail.com> - 2.2.5-1
- Initial version of package
