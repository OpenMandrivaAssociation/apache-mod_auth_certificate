#Module-Specific definitions
%define mod_name mod_auth_certificate
%define mod_conf B56_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	 A client certificate authentication module for apache
Name:		apache-%{mod_name}
Version:	0.3
Release: 	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/modauthcertific/
Source0:	http://sunet.dl.sourceforge.net/project/modauthcertific/mod_auth_certificate/mod_auth_certificate-%{version}/mod_auth_certificate-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires(pre):	apache-mod_ssl >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_ssl >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_certificate is an authentication module for the Apache 2.x server. It
adds the capability to forward usernames returned by mod_ssl to authorization
modules or providers as the are called since >= 2.2.x.

%prep

%setup -q -n %{mod_name}-%{version}
cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

