import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pyelethos", 
	version="0.0.1.7",
	author="Cedarville University",
	author_email="techhelp@cedarville.edu",
	description="Library for interacting with Ellucian Ethos",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/cedarville-university/py-ethos",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
