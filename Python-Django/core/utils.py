from amazon_pay.client import AmazonPayClient
from server import settings


def AmazonConfirmationBackend():
    pretty_confirm = None
    pretty_authorize = None

    client = AmazonPayClient(
        mws_access_key=settings.MWS_ACCESS,
        mws_secret_key=settings.MWS_SECRET,
        merchant_id=settings.MERCHANT_ID,
        sandboz=True,
        region='na',
        currency_code='USD',
        log_enabled=True,
        log_file_name='log.txt',
        log_level='DEBUG'
    )

    print(client)

