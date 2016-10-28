from setuptools import setup

setup(
    name='xmlrpcssl',
    version='0.1',
    author='Jonatan Dellagostin',
    author_email='jdellagostin@gmail.com',
    url='https://github.com/jonDel/xmlrpcssl',
    packages=['xmlrpcssl'],
    license='LICENSE',
    description='xmlrpc server with basic authentication and secured with ssl',
    classifiers=[
     'Development Status :: 3 - Alpha',
     'License :: OSI Approved :: MIT License',
     'Programming Language :: Python :: 2.7',
     'Topic :: Text Processing :: Linguistic',
    ],
    keywords='ssl secure https xmlrpc rpc xml ldap',
    long_description=open('README.md').read(),
    install_requires=[
    ],
    extras_require={
     'ldap':  ['python-ldap>=2.4'],
    },
    include_package_data=True,
    zip_safe=False,
)
