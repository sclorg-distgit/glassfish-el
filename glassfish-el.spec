%{?scl:%scl_package glassfish-el}
%{!?scl:%global pkg_name %{name}}

%global namedreltag -b08
%global namedversion %{version}%{?namedreltag}

Name:          %{?scl_prefix}glassfish-el
Version:       3.0.1
Release:       0.4.b08.1%{?dist}
Summary:       J2EE Expression Language Implementation
License:       CDDL or GPLv2 with exceptions
URL:           http://uel.java.net
# svn export https://svn.java.net/svn/uel~svn/tags/javax.el-3.0.1-b08/ glassfish-el-3.0.1-b08
# rm -r glassfish-el-3.0.1-b08/fonts
# rm -r glassfish-el-3.0.1-b08/parent-pom
# rm -r glassfish-el-3.0.1-b08/repo
# rm -r glassfish-el-3.0.1-b08/spec
# rm -r glassfish-el-3.0.1-b08/uel
# rm -r glassfish-el-3.0.1-b08/www
# tar cJf glassfish-el-3.0.1-b08.tar.xz glassfish-el-3.0.1-b08
Source0:       %{pkg_name}-%{namedversion}-clean.tar.xz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: %{?scl_prefix}maven-local
BuildRequires: %{?scl_prefix}mvn(junit:junit)
BuildRequires: %{?scl_prefix}mvn(net.java:jvnet-parent:pom:)
BuildRequires: %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: %{?scl_prefix}mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires: %{?scl_prefix}mvn(org.apache.maven.surefire:surefire-junit47)
BuildRequires: %{?scl_prefix}mvn(org.codehaus.mojo:javacc-maven-plugin)
BuildRequires: %{?scl_prefix}mvn(org.glassfish:legal)

BuildArch:     noarch

%description
This project provides an implementation of the Expression Language (EL).
The main goals are:
 * Improves current implementation: bug fixes and performance improvements
 * Provides API for use by other tools, such as Netbeans

%package api
Summary:       Expression Language 3.0 API
License:       (CDDL or GPLv2 with exceptions) and ASL 2.0

%description api
Expression Language 3.0 API.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{namedversion}

cp -p %{SOURCE1} .

%pom_remove_plugin -r :findbugs-maven-plugin
%pom_remove_plugin -r :findbugs-maven-plugin api
%pom_remove_plugin -r :glassfish-copyright-maven-plugin

# Useless tasks
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin -r :maven-release-plugin api
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-source-plugin api

# Fix javadoc task
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals"
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals" api
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:configuration/pom:sourcepath"
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions/pom:execution/pom:configuration" "<additionalparam>-Xdoclint:none</additionalparam>"
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions/pom:execution/pom:configuration" "<additionalparam>-Xdoclint:none</additionalparam>" api

# Fix apis version
%pom_xpath_set "pom:project/pom:version" %{namedversion} api
# Add missing build dep
%pom_add_dep javax.el:javax.el-api:'${project.version}'

# Move code without build-helper plugin in the proper folder
%pom_remove_plugin -r :build-helper-maven-plugin
mv impl/src/main src

# Do not use ant
%pom_add_plugin org.codehaus.mojo:javacc-maven-plugin:2.6 . "
<executions>
    <execution>
        <id>jjtree-javacc</id>
        <goals>
            <goal>jjtree-javacc</goal>
        </goals>
        <configuration>
            <sourceDirectory>src/main/java/com/sun/el/parser</sourceDirectory>
            <outputDirectory>src/main/java/com/sun/el/parser</outputDirectory>
        </configuration>
    </execution>
</executions>"

# Fix impl resources path
%pom_xpath_remove "pom:build/pom:resources/pom:resource"
%pom_xpath_inject "pom:build/pom:resources" "
    <resource>
        <directory>src/main/java</directory>
        <includes>
            <include>**/*.properties</include>
            <include>**/*.xml</include>
        </includes>
    </resource>"

# This is a dummy POM added just to ease building in the RPM platforms
cat > pom-parent.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project
  xmlns="http://maven.apache.org/POM/4.0.0"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <modelVersion>4.0.0</modelVersion>
  <groupId>org.glassfish.web</groupId>
  <artifactId>javax.el-root</artifactId>
  <version>%{namedversion}</version>
  <packaging>pom</packaging>
  <name>%{pkg_name} Parent</name>
  <modules>
    <module>api</module>
    <module>pom.xml</module>
  </modules>
</project>
EOF

%mvn_file javax.el:javax.el-api %{pkg_name}-api
%mvn_alias javax.el:javax.el-api "javax.el:el-api" "org.glassfish:javax.el-api"

%mvn_file org.glassfish:javax.el %{pkg_name}
%mvn_alias org.glassfish:javax.el "org.eclipse.jetty.orbit:com.sun.el" "org.glassfish.web:javax.el" "org.glassfish:javax.el-impl"

%mvn_package :javax.el-root __noinstall

%build

%mvn_build -s -- -f pom-parent.xml

%install
%mvn_install

cp -p api/target/classes/META-INF/LICENSE.txt .
cp -p api/src/main/javadoc/doc-files/*-spec-license.html .

%files -f .mfiles-javax.el

%files api -f .mfiles-javax.el-api
%license LICENSE.txt LICENSE-2.0.txt *-spec-license.html

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt LICENSE-2.0.txt

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 3.0.1-0.4.b08.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-0.4.b08
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Mat Booth <mat.booth@redhat.com> - 3.0.1-0.3.b08
- Rebuild

* Wed Oct 12 2016 gil cattaneo <puntogil@libero.it> 3.0.1-0.2.b08
- use default bundle plugin settings

* Mon Oct 03 2016 gil cattaneo <puntogil@libero.it> 3.0.1-0.1.b08
- update to 3.0.1-b08

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
