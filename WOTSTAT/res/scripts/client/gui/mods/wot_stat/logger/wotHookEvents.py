from Account import Account
from Avatar import PlayerAvatar
from ProjectileMover import ProjectileMover
from Vehicle import Vehicle
from VehicleGunRotator import VehicleGunRotator
from gui.Scaleform.daapi.view.lobby.battle_queue import BattleQueue
from helpers import dependency
from skeletons.connection_mgr import IConnectionManager
from ..common.exceptionSending import SendExceptionEvent
from ..common.hook import g_overrideLib


class WotHookEvents:
  __connectionMgr = dependency.descriptor(IConnectionManager)

  def __init__(self):
    # DI
    self.__connectionMgr.onConnected += self.__onConnected

    self.listeners = {}
    # ------------------INIT------------------#
    self.onConnected = SendExceptionEvent()
    self.Account_onBecomePlayer = SendExceptionEvent()
    self.BattleQueue_populate = SendExceptionEvent()
    self.PlayerAvatar_onEnterWorld = SendExceptionEvent()
    self.PlayerAvatar_updateTargetingInfo = SendExceptionEvent()
    self.PlayerAvatar_onArenaPeriodChange = SendExceptionEvent()
    # -------------------MOVE------------------#
    self.VehicleGunRotator_setShotPosition = SendExceptionEvent()
    self.VehicleGunRotator_updateGunMarker = SendExceptionEvent()
    self.PlayerAvatar_updateGunMarker = SendExceptionEvent()
    # -------------------SHOT------------------#
    self.PlayerAvatar_shoot = SendExceptionEvent()
    self.PlayerAvatar_showTracer = SendExceptionEvent()
    self.PlayerAvatar_showShotResults = SendExceptionEvent()
    self.Vehicle_onHealthChanged = SendExceptionEvent()
    self.PlayerAvatar_showOwnVehicleHitDirection = SendExceptionEvent()
    # -------------------EXPLOSION------------------#
    self.PlayerAvatar_explodeProjectile = SendExceptionEvent()
    self.Vehicle_showDamageFromShot = SendExceptionEvent()
    # -------------------PROJECTILE-------------------#
    self.ProjectileMover_killProjectile = SendExceptionEvent()
    # -------------------HELP-------------------#
    self.PlayerAvatar_enableServerAim = SendExceptionEvent()

  def __onConnected(self):
    self.onConnected()


wotHookEvents = WotHookEvents()


# ------------------INIT------------------#

@g_overrideLib.registerEvent(Account, 'onBecomePlayer')
def queuePopulate(self, *a, **k):
  wotHookEvents.Account_onBecomePlayer(self, *a, **k)


@g_overrideLib.registerEvent(BattleQueue, '_populate')
def queuePopulate(self, *a, **k):
  wotHookEvents.BattleQueue_populate(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'onEnterWorld')
def onEnterWorld(self, *a, **k):
  wotHookEvents.PlayerAvatar_onEnterWorld(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'updateTargetingInfo')
def updateTargetingInfo(self, *a, **k):
  wotHookEvents.PlayerAvatar_updateTargetingInfo(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, '_PlayerAvatar__onArenaPeriodChange')
def onArenaPeriodChange(self, *a, **k):
  wotHookEvents.PlayerAvatar_onArenaPeriodChange(self, *a, **k)


# -------------------MOVE------------------#

@g_overrideLib.registerEvent(VehicleGunRotator, 'setShotPosition')
def setShotPosition(self, *a, **k):
  wotHookEvents.VehicleGunRotator_setShotPosition(self, *a, **k)


@g_overrideLib.registerEvent(VehicleGunRotator, '_VehicleGunRotator__updateGunMarker')
def updateGunMarker(self, *a, **k):
  wotHookEvents.VehicleGunRotator_updateGunMarker(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'updateGunMarker')
def PlayerAvatar_updateGunMarker(self, *a, **k):
  wotHookEvents.PlayerAvatar_updateGunMarker(self, *a, **k)


# -------------------SHOT------------------#

@g_overrideLib.registerEvent(PlayerAvatar, 'shoot', prepend=True)
def shoot(self, *a, **k):
  wotHookEvents.PlayerAvatar_shoot(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'showTracer')
def showTracer(self, *a, **k):
  wotHookEvents.PlayerAvatar_showTracer(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'showShotResults')
def showShotResults(self, *a, **k):
  wotHookEvents.PlayerAvatar_showShotResults(self, *a, **k)


@g_overrideLib.registerEvent(Vehicle, 'onHealthChanged')
def onHealthChanged(self, *a, **k):
  wotHookEvents.Vehicle_onHealthChanged(self, *a, **k)


@g_overrideLib.registerEvent(PlayerAvatar, 'showOwnVehicleHitDirection')
def showOwnVehicleHitDirection(self, *a, **k):
  wotHookEvents.PlayerAvatar_showOwnVehicleHitDirection(self, *a, **k)


# -------------------EXPLOSION------------------#

@g_overrideLib.registerEvent(PlayerAvatar, 'explodeProjectile')
def explodeProjectile(self, *a, **k):
  wotHookEvents.PlayerAvatar_explodeProjectile(self, *a, **k)


@g_overrideLib.registerEvent(Vehicle, 'showDamageFromShot')
def showDamageFromShot(self, *a, **k):
  wotHookEvents.Vehicle_showDamageFromShot(self, *a, **k)


# -------------------PROJECTILE-------------------#

@g_overrideLib.registerEvent(ProjectileMover, '_ProjectileMover__killProjectile')
def killProjectile(self, *a, **k):
  wotHookEvents.ProjectileMover_killProjectile(self, *a, **k)


# -------------------HELP-------------------#

@g_overrideLib.registerEvent(PlayerAvatar, 'enableServerAim')
def enableServerAim(self, *a, **k):
  wotHookEvents.PlayerAvatar_enableServerAim(self, *a, **k)
