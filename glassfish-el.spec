%{?scl:%scl_package glassfish-el}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global artifactId javax.el

Name:           %{?scl_prefix}glassfish-el
Version:        3.0.0
Release:        5.1%{?dist}
Summary:        J2EE Expression Language Implementation
License:        CDDL or GPLv2 with exceptions
URL:            http://uel.java.net
# ./generate_tarball.sh
Source0:        %{pkg_name}-%{version}.tar.gz
Source1:        generate_tarball.sh
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_java_common}mvn(javax.el:javax.el-api)
BuildRequires:  %{?scl_prefix_maven}mvn(net.java:jvnet-parent:pom:)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.surefire:surefire-junit47)
BuildRequires:  %{?scl_prefix_maven}mvn(org.codehaus.mojo:build-helper-maven-plugin)

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
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -n %{pkg_name}-%{version} -q

%mvn_compat_version *:* %{version}
%mvn_file :%{artifactId} %{pkg_name}
%mvn_alias :%{artifactId} "org.eclipse.jetty.orbit:com.sun.el" "org.glassfish.web:javax.el"

# missing (unneeded) dep org.glassfish:legal
%pom_remove_plugin :maven-remote-resources-plugin
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Jun 29 2015 Mat Booth <mat.booth@redhat.com> - 3.0.0-5.1
- Import latest from Fedora

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-4
- Fix build-requires on jvnet-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.0-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Dec 09 2013 Michal Srb <msrb@redhat.com> - 3.0.0-1
- Update to upstream version 3.0.0

* Mon Aug 12 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.5-5
- Move xmvn customizations to prep.

* Wed Aug 07 2013 gil cattaneo <puntogil@libero.it> 2.2.5-4
- switch to XMvn, fix for rhbz#992384
- install license file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.5-2
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#918514

* Fri Feb 1 2013 David Xie <david.scriptfan@gmail.com> - 2.2.5-1
- Initial version of package
