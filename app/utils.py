import requests
from flask import url_for
import pprint
import json
import hashlib
from functools import wraps
from base64 import b64encode
from uuid import uuid4
from flask_login import current_user
from werkzeug.exceptions import Unauthorized, Forbidden
from json import dumps
import hmac


def require_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def authorize(*args, **kwargs):
            if not current_user.is_authenticated:
                raise Unauthorized()
            if current_user.user_role not in roles:
                raise Forbidden()

            return f(*args, **kwargs)
        return authorize
    return wrapper


def momo_request_payment(amount, extra_data, payment_id, order_info):
    headers = {"Content-Type": "application/json"}
    url = "https://test-payment.momo.vn/v2/gateway/api/create"

    extra_data = b64encode(bytes(dumps(extra_data), 'utf-8'))
    ipn_url = "https://momo.vn"
    redirect_url = url_for('momo_payment_check', payment_id=payment_id, _external=True)
    request_id = "RQ_" + str(uuid4())
    access_key = "F8BBA842ECF85"
    secret_key = "K951B6PE1waDMi640xX08PD3vg6EkVlz"

    raw_data = {
            "amount": str(amount),
            "extraData": extra_data.decode('utf-8'),
            "ipnUrl": ipn_url,
            "orderId": request_id,
            "orderInfo": order_info,
            "partnerCode": "MOMO",
            "redirectUrl": redirect_url,
            "requestId": request_id,
            "requestType": "captureWallet"
    }

    request_data = raw_data

    message = "accessKey=" + access_key
    for k, v in raw_data.items():
        message = message + "&" + k + "=" + str(v)
    print(message)

    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    request_data["signature"] = signature
    request_data["lang"] = "vi"
    request_data["accessKey"] = access_key

    response = requests.post(url, headers=headers, data=json.dumps(request_data))
    return response.json()
