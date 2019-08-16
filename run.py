#!/usr/bin/env python
# -*- coding: utf-8 -*-
__DATE__ = '10.07.2018'
__AUTHOR__ = 'cemonatk'

from linkshorten import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
