from flask import Flask, render_template, request, redirect, url_for
import time
import paypalrestsdk
app = Flask(__name__)



paypalrestsdk.configure({
    "mode": "sandbox",  
    "client_id": "Afdnr0GkdNT8RMkHf8BXNuvsJ24YDDu672jNBTQ51GVOlyOlaHY2HdJj_S4nfqdDVhTt9ZE5O-DbFGxd",
    "client_secret": "EMARiYFXlHlGJte4SBkhMVaHfFfAE4VAIe1MJKj_MGdQJgU4JHQfW3uoEGjlQxLOId4Wst3vX56QYkAG",
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    amount = request.form['amount']
    print(amount.isnumeric())
    if(amount.isnumeric()==True):
            print("reached")
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": url_for('success', _external=True),  # Success URL
                    "cancel_url": url_for('index', _external=True)  # Cancel URL
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": "Sample Item",
                            "sku": "item",
                            "price": amount,
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": amount,
                        "currency": "USD"
                    },
                    "description": "Sample payment"
                }]
             })
            if payment.create():
                return redirect(payment.links[1].href)  # Redirect to PayPal for payment
            else:
                return "Error creating payment: %s" % payment.error
    else:
        return "Amount should only  contain numeric value"
        


@app.route('/success')
def success():
    # Handle the successful payment confirmation here
    return "Payment Successful!"

if __name__ == '__main__':
    app.run(debug=True)
