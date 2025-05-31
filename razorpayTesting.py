from flask import Flask, render_template, request, jsonify
import razorpay

app = Flask(__name__)

# Replace these with your Razorpay Test Credentials
RAZORPAY_KEY_ID = 'rzp_test_c4YZ6VsAIXU43p'
RAZORPAY_KEY_SECRET = 'B7uiTIWTY91jb8xXaXSgHkqA'

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/')
def index():
    return render_template('pay.html', razorpay_key=RAZORPAY_KEY_ID)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        amount = int(data.get('amount', 0)) * 100  # Convert to paise

        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": '1'
        })

        return jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    signature = request.form.get('razorpay_signature')

    # Here you can verify the signature (optional in test phase)
    if payment_id and order_id:
        return "✅ Payment successful!"
    else:
        return "❌ Payment verification failed", 400

if __name__ == '__main__':
    app.run(debug=True)
