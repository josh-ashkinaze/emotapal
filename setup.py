from distutils.core import setup
setup(
  name = 'emotapal',
  packages = ['emotapal'],   
  version = '0.1',      
  license='gpl-3.0',        
  description = 'Match colors and words',   
  author = 'Josh Ashkinaze',                   
  author_email = 'josh.ashkinaze@gmail.com',   
  url = 'https://github.com/josh-ashkinaze/emotapal',   
  download_url = 'https://github.com/josh-ashkinaze/emotapal/archive/v_01.tar.gz',    
  keywords = ['colors', 'emotions', 'psychology', 'image processing'],   # Keywords that define your package best
  install_requires=[           
      "requests", "scikit-learn", "seaborn",
      "matplotlib", "colorthief", "google_images_download", "afinn"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
)



requires = [
    "requests", "scikit-learn", "seaborn",
    "matplotlib", "colorthief", "google_images_download", "afinn"
]