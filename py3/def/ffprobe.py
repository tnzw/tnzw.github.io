# ffprobe.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ffprobe(i):
  p = subprocess.run(['ffprobe', '-hide_banner', '-loglevel', 'quiet', '-show_streams', '-of', 'json', '-i', i], stdout=subprocess.PIPE, check=True)
  return json.loads(p.stdout)
ffprobe._required_globals = ['json', 'subprocess']
