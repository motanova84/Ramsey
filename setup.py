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
    author='José Manuel Mota Burruezo (JMMB Ψ✧)',
    author_email='motanova84@users.noreply.github.com',
    description='Formal verification tool for vibrational Ramsey bounds - QCAL ∞³ Original Manufacture',
    long_description='QCAL ∞³ Sovereign Architecture - Formal verification and implementation of Vibrational Ramsey Theory',
    license='Sovereign Noetic License 1.0',
    url='https://github.com/motanova84/Ramsey',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='ramsey-theory formal-verification qcal sovereign-architecture quantum-coherence',
)
