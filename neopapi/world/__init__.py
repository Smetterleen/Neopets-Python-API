from neopapi.core.browse import register_page

register_page('explore.phtml',
              ['island/index.phtml', 'pirates/index.phtml', 'desert/index.phtml',
               'halloween/index.phtml', 'faerieland/index.phtml', 'medieval/brightvale.phtml',
               'medieval/index.phtml', 'worlds/index_kikolake.phtml', 'objects.phtml', 
               'worlds/index_roo.phtml', 'prehistoric/index.phtml', 'winter/index.phtml',
               'altador/index.phtml', 'shenkuu/index.phtml', 'tropical/index.phtml',
               'water/index.phtml', 'magma/index.phtml', 'space/index.phtml', 'moon/index.phtml'],
              True)