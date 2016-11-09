from setuptools import setup

setup(
    name='xmlrpcssl',
    version='0.1.3',
    author='Jonatan Dellagostin',
    author_email='jdellagostin@gmail.com',
    url='https://github.com/jonDel/xmlrpcssl',
    packages=['xmlrpcssl'],
    license='GPLv3',
    description='xmlrpc server with basic authentication and secured with ssl',
    classifiers=[
     'Development Status :: 3 - Alpha',
     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
     'Programming Language :: Python :: 2.6',
     'Programming Language :: Python :: 2.7',
     'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
     'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    keywords='ssl secure https xmlrpc rpc xml ldap',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
    extras_require={
     'ldap':  ['python-ldap>=2.4'],
    },
    include_package_data=True,
    zip_safe=False,
)
