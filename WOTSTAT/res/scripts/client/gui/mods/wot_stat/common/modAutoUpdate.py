import BigWorld
import json
import os
import shutil

from asyncResponse import get_async
from helpers import getShortClientVersion
from ..utils import print_log
from .exceptionSending import with_exception_sending


def num_game_version():
  return getShortClientVersion().split('v.')[1].strip()


@with_exception_sending
def update_game_version(full_mod_name):
  gameVersion = num_game_version()
  currentMod = os.path.join(os.path.abspath('./mods/'), gameVersion, full_mod_name)

  def b(x, y):
    return '.'.join(
      [str(int(c) + 1 if i == y else 0) if i >= y else c for i, c in enumerate(x.split('.'))])

  v = [b(gameVersion, i) for i in range(len(gameVersion.split('.')))]

  absPath = os.path.abspath('./mods/')
  for i in range(len(v)):
    p = os.path.join(absPath, v[i])
    if not os.path.exists(p):
      os.mkdir(p)
    filePath = os.path.join(p, full_mod_name)
    if not os.path.exists(filePath):
      shutil.copyfile(currentMod, filePath)


GH_headers = {'X-GitHub-Api-Version': '2022-11-28',
              'Accept': 'application/vnd.github+json'}


@with_exception_sending
def update_mod_version(url, mod_name, current_version, on_start_update=None, on_updated=None, on_success_check=None):
  latest_version = ''

  def end_load_mod(res):
    global latest_version

    gameVersion = num_game_version()
    newMod = os.path.join(os.path.abspath(
      './mods/'), gameVersion, mod_name + '_' + latest_version + '.wotmod')
    if not os.path.exists(newMod):
      with open(newMod, "wb") as f:
        f.write(res)

    if on_updated:
      on_updated(latest_version)

  def end_load_info(res):
    global latest_version

    data = json.loads(res)
    latest_version = data['tag_name']
    print_log('detect latest version: ' + latest_version)
    if current_version == latest_version:
      if on_success_check: on_success_check()
      return

    assets = data['assets']
    asset = filter(lambda x: ('name' in x) and (x['name'] == 'mod.wotStat_' + latest_version + '.wotmod'), assets)
    if not len(asset) > 0: return

    firstAsset = asset[0]
    if 'browser_download_url' not in firstAsset: return

    downloadUrl = firstAsset['browser_download_url']
    print_log('Start download new version from: ' + downloadUrl)

    if on_start_update:
      on_start_update(latest_version)
    get_async(downloadUrl, None, end_load_mod)

  get_async(url, None, end_load_info, GH_headers)
