from easydict import EasyDict as edict
__APP_CONFIG                           = edict()
# Import this as from appconfig import appcfg

appcfg                           = __APP_CONFIG
    
__APP_CONFIG.DETECT                         = edict()
__APP_CONFIG.DETECT.PROCESSED_IMAGE_OUT     = '.output'
__APP_CONFIG.DETECT.VIDEO_IN     = './input/India - 8698.mp4'
__APP_CONFIG.DETECT.CORE_PACKAGES = '../compvision/utils'
__APP_CONFIG.DETECT.KNIFE = True
__APP_CONFIG.DETECT.SMOKE = True
__APP_CONFIG.DETECT.FIRE = True
__APP_CONFIG.DETECT.GUN = True
__APP_CONFIG.DETECT.INPUTVIDEO_SOURCE='C:\MP\Camera2.py'
__APP_CONFIG.DETECT.SEND_SMS = False
__APP_CONFIG.DETECT.SMS_FROM_NO = '+16315055650'
__APP_CONFIG.DETECT.SMS_TO_NO = '+919980905999'

#Place your TWILIO KEYS HERE
__APP_CONFIG.DETECT.TWILIO_ACCT_ID='AC44361a591a1c28a3cd1e8db09a4fc5c3'
__APP_CONFIG.DETECT.TWILIO_ATUH_TOKEN='342f0ea16bb3858d59bfa37e75ded807'