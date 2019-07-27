from distutils.core import setup



setup(
  include_package_data = True,
  name = 'emotapal',
  packages = ['emotapal'],   
  version = '0.8',      
  license='gpl-3.0',        
  description = 'Match colors and words',   
  author = 'Josh Ashkinaze',                   
  author_email = 'josh.ashkinaze@gmail.com',   
  url = 'https://github.com/josh-ashkinaze/emotapal',  
  download_url = 'https://github.com/josh-ashkinaze/emotapal/archive/v_08.tar.gz',    
  keywords = ['colors', 'emotions', 'psychology', 'image processing'],  
  install_requires=[           
      "requests", "scikit-learn", "seaborn",
      "matplotlib", "colorthief", "google_images_download", "afinn"
      ],

  package_data={'emotapal': ['clf.pkl']},

  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
)



