from distutils.core import setup
setup(
  name = 'himawari8',         
  version = '0.7',      
  packages = ['himawari8'],  
  license='GPL-3.0',        
  description = 'Assists in downloading images of planet earth from the japanese satellite himawari 8',   
  author = 'Raphael Augusto Teixeira Silva',                 
  author_email = 'raphaelaugustoteixeirasilva@gmail.com',      
  url = 'https://github.com/Maharal/Himawari-8',  
  download_url = 'https://github.com/Maharal/Himawari-8/archive/v0.7.tar.gz', 
  keywords = ['earth', 'himawari 8', 'planet', 'photo'],   
  install_requires=[           
          'requests',
          'Pillow',
          'tqdm',
          'setuptools',
          'wheel'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
  ],
)
