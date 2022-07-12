from setuptools import setup


with open("README.md") as f:
    readme = f.read()

setup(
    name="vpype-concave-hull",
    version="0.1.0",
    description="Find the concave hull of a point set",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Daniele D'Orazio",
    url="https://github.com/d-dorazio/vpype-concave-hull",
    packages=["vpype_concave_hull"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Plugins",
    ],
    setup_requires=["wheel"],
    install_requires=[
        "click",
        "vpype[all]>=1.10,<2.0",
        "numpy",
        "scipy",
        "shapely>=1.8.0",
    ],
    entry_points="""
            [vpype.plugins]
            concave_hull=vpype_concave_hull.vpype_concave_hull:concave_hull
        """,
)
