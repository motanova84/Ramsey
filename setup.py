from setuptools import setup, find_packages

setup(
    name='ai-ramsey-formal',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'z3-solver>=4.12.0',
        'numpy>=1.24.0',
    ],
    entry_points={
        'console_scripts': [
            'ai-ramsey-formal=ai_ramsey_formal.cli:cli',
        ],
    },
    author='José Manuel Mota Burruezo',
    description='Formal verification tool for vibrational Ramsey bounds',
    python_requires='>=3.8',
)
