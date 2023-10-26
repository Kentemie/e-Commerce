const stripe = Stripe("pk_test_51O3IqsKByHITeWBfhCYeW5TCpt11K2toSynUIEEITxxVv7UK0vaayIGDKU3LlbR2ckM20mA1263E766P9b2kA8Wy00iRRGZ3Q1");

const element = document.getElementById("submit");
const client_secret = element.getAttribute("data-secret");

const elements = stripe.elements();

const style = {
    base: {
        color: "#fff",
        lineHeight: "2.4",
        fontSize: "16px"
    }
};

const card = elements.create("card", {style: style});
card.mount("#card-element");

card.on("change", function(event) {
    const displayError = document.getElementById("cart-errors");
    
    if (event.error) {
        displayError.textContent = event.error.message;
        $("#card-errors").addClass("alert alert-info");
    }
    else {
        displayError.textContent = '';
        $("#card-errors").removeClass("alert alert-info");
    }
});

function stripePayment(data) {

    const first_name = data.first_name;
    const last_name = data.first_name;

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add/",
        data: {
            order_key: client_secret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
            address_data: data.address_data,
            payment_method: data.payment_method
        },
        success: function(json) {

            stripe.confirmCardPayment(client_secret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            line1: data.address_data.address_line_1,
                            line2: data.address_data.address_line_2
                        },
                        name: first_name + last_name,
                    }
                }
            }).then(function(result) {
                if (result.error) {
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === "succeeded") {
                        // There's a risk of the customer closing the window before callback
                        // execution. Set up a webhook or plugin to listen for the
                        // payment_intent.succeeded event that handles any business critical
                        // post-payment actions.
                        window.location.replace("http://127.0.0.1:8000/payment/order_placed/");
                    }
                }
            });

        },
        error: function(xhr, errmsg, err) {
            console.log(xhr, errmsg, err);
        },
    });

}