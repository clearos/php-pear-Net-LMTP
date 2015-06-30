%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_LMTP

Name:           php-pear-Net-LMTP
Version:        1.0.2
Release:        1%{?dist}
Summary:        Provides an implementation of the LMTP protocol
Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Net_LMTP
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(PEAR)
Requires:       php-pear(Net_Socket)


%description
Provides an implementation of the LMTP protocol using PEAR's Net_Socket class.

%prep
%setup -q -c

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}

%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*
rm -rf %{buildroot}%{pear_phpdir}/data
rm -rf %{buildroot}/usr/share/pear-data/Net_LMTP/README
rm -rf %{buildroot}/var/lib/pear

# Install XML package description
%{__mkdir_p} %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
# Sanity check
lst=$(find %{buildroot}%{pear_phpdir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;

%clean
rm -rf %{buildroot}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_phpdir}/Net/*
%{pear_testdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml

%changelog
* Sat Feb 25 2012 ClearFoundation <developer@clearfoundation.com> 1.0.2-1
- Initial build
