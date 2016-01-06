%{?scl:%scl_package glassfish-el}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global artifactId javax.el

Name:           %{?scl_prefix}glassfish-el
Version:        3.0.0
Release:        6%{?dist}
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

%{?scl:Requires: %scl_runtime}

%description
This project provides an implementation of the Expression Language (EL).
The main goals are:
 * Improves current implementation: bug fixes and performance improvements
 * Provides API for use by other tools, such as Netbeans

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{pkg_name}-%{version}

scl enable %{scl_maven} %{scl} - <<"EOF"
%mvn_compat_version *:* %{version}
%mvn_file :%{artifactId} %{pkg_name}
%mvn_alias :%{artifactId} "org.eclipse.jetty.orbit:com.sun.el" "org.glassfish.web:javax.el"

# missing (unneeded) dep org.glassfish:legal
%pom_remove_plugin :maven-remote-resources-plugin
EOF

%build
scl enable %{scl_maven} %{scl} - <<"EOF"
%mvn_build
EOF

%install
scl enable %{scl_maven} %{scl} - <<"EOF"
%mvn_install
EOF

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Wed Apr 01 2015 Mat Booth <mat.booth@redhat.com> - 3.0.0-6
- Resolves: rhbz#1208232 - rebuild to fix erroneous dep on maven30 collection

* Mon Jan 12 2015 Mat Booth <mat.booth@redhat.com> - 3.0.0-5
- Related: rhbz#1175105 - rebuilt

* Fri Jan 09 2015 Mat Booth <mat.booth@redhat.com> - 3.0.0-4.1
- Related: rhbz#1175105 - Import into DTS 3.1

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
