import time
import requests
from hashlib import md5
from urllib.parse import urlencode

from Wsign import Gorgon,Argus,Ladon


# ===================== SIGN =====================
def sign(params, payload=None, cookie=None, sec_device_id="", aid=1233,
         license_id=1611921764, sdk_version_str="v10.01.17-ov-android_V27",
         sdk_version=100117, platform=0, unix=None):

    if unix is None:
        unix = int(time.time())

    x_ss_stub = md5(payload.encode()).hexdigest().upper() if payload else None

    return (
        Gorgon(params, unix, payload, cookie).get_value()
        | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(
                params,
                x_ss_stub,
                unix,
                platform=platform,
                aid=aid,
                license_id=license_id,
                sec_device_id=sec_device_id,
                sdk_version=sdk_version_str,
                sdk_version_int=sdk_version,
            ),
            "x-ss-stub": x_ss_stub
        }
    )


# ===================== PARAMS (QUERY) =====================
def base_params():
    return {
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": str(int(time.time() * 1000)),
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "430104",
        "version_name": "43.1.4",
        "manifest_version_code": "2024301040",
        "update_version_code": "2024301040",
        "ab_version": "43.1.4",
        "resolution": "900*1600",
        "dpi": "320",
        "device_type": "SM-S9260",
        "device_brand": "Samsung",
        "language": "en",
        "os_api": "32",
        "os_version": "12",
        "ac": "wifi",
        "is_pad": "1",
        "current_region": "DZ",
        "app_type": "normal",
        "sys_region": "US",
        "last_install_time": "1767362248",
        "mcc_mnc": "31001",
        "timezone_name": "Africa/Lagos",
        "carrier_region_v2": "302",
        "residence": "DZ",
        "app_language": "en",
        "carrier_region": "US",
        "timezone_offset": "3600",
        "host_abi": "arm64-v8a",
        "locale": "en",
        "content_language": "en,fr,ar,",
        "ac2": "wifi5g",
        "uoo": "0",
        "op_region": "DZ",
        "build_number": "43.1.4",
        "region": "US",
        "ts": str(int(time.time())),
        "iid": iid,
        "device_id": did,
    }


# ===================== PAYLOAD (BODY) =====================
def payload_data():
    return {
        "user_id": target_uid,
        "sec_user_id": target_secuid,
        "type": "1",
        "channel_id": "0",
        "from": "20",
        "from_pre": "13",
        "rec_type": "1-1",
        "item_id": item_id,
        "enter_from": "homepage_hot",
        "action_time": str(int(time.time() * 1000)),
        "is_network_available": "true",
    }


# ===================== SESSION =====================
iid = "7590763061897594632"
did = "7590755553484883512"

target_uid = "7094313498864288773"
target_secuid = "MS4wLjABAAAA..."

item_id = "7580812327113608455"

cookie = "PUT_VALID_COOKIE_HERE"


# ===================== REQUEST =====================
url = "https://api31-normal-alisg.tiktokv.com/aweme/v1/commit/follow/user/"

params = urlencode(base_params())
payload = urlencode(payload_data())

sig = sign(params, payload, cookie=cookie)

headers = {
    "host": "api31-normal-alisg.tiktokv.com",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "user-agent": "com.zhiliaoapp.musically/2024301040 (Linux; U; Android 12; en; SM-S9260; Build/V417IR;tt-ok/3.12.13.21)",
    "x-ss-req-ticket": str(int(time.time() * 1000)),
    "x-tt-dm-status": "login=1;ct=1;rt=1",
    "x-tt-store-region": "dz",
    "x-tt-store-region-src": "uid",
    "sdk-version": "2",
    "passport-sdk-version": "1",
    "x-vc-bdturing-sdk-version": "2.3.17.i18n",
    "tt-ticket-guard-version": "3",

    "x-gorgon": sig["x-gorgon"],
    "x-khronos": sig["x-khronos"],
    "x-argus": sig["x-argus"],
    "x-ladon": sig["x-ladon"],
    "x-ss-stub": sig["x-ss-stub"],

    "cookie": cookie,
}

resp = requests.post(url, params=params, data=payload, headers=headers)
print(resp.status_code)
print(resp.text)
