import io
from setuptools import find_packages, setup

with io.open("VERSION", "r") as fd:
    VERSION = fd.read().rstrip()

requires = [
    "nextgisweb>=4.5.0.dev19",
]

entry_points = {
    'nextgisweb.packages': [
        'nextgisweb_legend = nextgisweb:single_component',
    ],
}

setup(
    name='nextgisweb_legend',
    version=VERSION,
    description="Map legends for NextGIS Web",
    long_description="",
    autor="IT-Thematic",
    author_email="inbox@it-thematic.ru",
    url='https://github.com/it-thematic/nextgisweb_legend',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8,<4",
    install_requires=requires,
    entry_points=entry_points,
)
