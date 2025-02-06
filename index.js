const Razorpay = require("razorpay");

// Initialize Razorpay with environment variables
const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID,
    key_secret: process.env.RAZORPAY_KEY_SECRET,
});

exports.handler = async (event) => {
    const headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
    };
    
    // Handle CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    try {
        const { amount } = JSON.parse(event.body);

        const options = {
            amount: amount, // Amount in paise
            currency: "INR",
            receipt: `receipt_${Date.now()}`
        };

        const order = await razorpay.orders.create(options);

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ order })
        };

    } catch (error) {
        console.error("Error creating order:", error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: "Failed to create Razorpay order" })
        };
    }
};