from django.shortcuts import render
import json 

# Create your views here.
def index(request):
    return render(request,  template_name="base.html")

def cart(request):
    if request.method == 'POST':
        request.session['merchant_id'] = request.POST.get('merchant-id')
        request.session['mws_access_key'] = request.POST.get('mws-access-key')
        request.session['mws_secret_key'] = request.POST.get('mws-secret-key')
        request.session['client_id'] = request.POST.get('client-id')
        request.session['order_reference_id'] = 'S01-9969307-1083016'
    return render(request, 'cart.html')

def confirm(request):
    if request.method == 'POST':
        from amazon_pay.client import AmazonPayClient

        client = AmazonPayClient(
            mws_access_key=request.session['mws_access_key'],
            mws_secret_key=request.session['mws_secret_key'],
            merchant_id=request.session['merchant_id'],
            sandbox=True,
            region='na',
            currency_code='USD',
            log_enabled=True,
            log_file_name="log.txt",
            log_level="DEBUG"
        )

        print(request.session)

        response = client.confirm_order_reference(
            amazon_order_reference_id=request.session['order_reference_id']
        )

        pretty_confirm = json.dumps(
            json.loads(
            response.to_json()),
            indent=4
        )

        if response.success:
           response = client.authorize(
            amazon_order_reference_id=request.session['order_reference_id'],
            authorization_reference_id=rand(),
            authorization_amount='19.95',
            transaction_timeout=0,
            capture_now=False)
        
        pretty_authorize = json.dumps(
            json.loads(
                response.to_json()
            ), indent=4
        )

        return render(request, 'confirm.html', {'confirm':pretty_confirm, 'authorize':pretty_authorize})

def set(request):
    request.session['access_token'] = request.GET.get('access_token')
    return render(request, 'set.html')

def get_details():
    if request.method == 'POST':
        from amazon_pay.client import AmazonPayClient

        client = AmazonPayClient(
            mws_access_key=request.session['mws_access_key'],
            mws_secret_key=request.session['mws_secret_key'],
            merchant_id=request.session['merchant_id'],
            sandbox=True,
            region='na',
            currency_code='USD',
            log_enabled=True,
            log_file_name="log.txt",
            log_level="DEBUG")

        order_reference_id = request.POST.get('orderReferenceId')
        request.session['order_reference_id'] = order_reference_id
        
        print(request.session['order_reference_id'])

        response = client.set_order_reference_details(
            amazon_order_reference_id=order_reference_id,
            order_total='19.95')

        if response.success:
            response = client.get_order_reference_details(
                amazon_order_reference_id=order_reference_id,
                address_consent_token=request.session['access_token'])

        pretty = json.dumps(
            json.loads(
                response.to_json()),
            indent=4)

        return pretty


def rand():
    return random.randint(0, 9999) + random.randint(0, 9999)
        