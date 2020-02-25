import setuptools

setuptools.setup(
    name='flaskr',
    version='1.0.0',
    packages=setuptools.find_packages(),     # automatically add all packages/modules imported by flaskr
    include_package_data=True,     # include files specified by MANIFEST.in
    zip_safe=False,  # don't allow for setup directly from zip file (maybe?)
    install_requires=['flask', ],    # dependencies pip will install together with flaskr
)
