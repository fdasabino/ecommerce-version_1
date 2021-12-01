let stripe = Stripe('STRIPE_PUBLISHABLE_KEY');

let elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
let elements = stripe.elements();
let style = {
  base: {
    color: '#000',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    lineHeight: '2',
    fontSize: '14px',
  }
};


let card = elements.create("card", {
  style
});
card.mount("#card-element");

card.on('change', (event) => {
  let displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-danger');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-danger');
  }
});

let form = document.getElementById('payment-form');

form.addEventListener('submit', (ev) => {
  ev.preventDefault();

  let custName = document.getElementById("custName").value;
  let custAdd = document.getElementById("custAdd").value;
  let custAdd2 = document.getElementById("custAdd2").value;
  let postCode = document.getElementById("postCode").value;


  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success(json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card,
          billing_details: {
            address: {
              line1: custAdd,
              line2: custAdd2,
              postal_code: postCode,
            },
            name: custName
          },
        }
      }).then((result) => {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else if (result.paymentIntent.status === 'succeeded') {
          console.log('payment processed')
          // There's a risk of the customer closing the window before callback
          // execution. Set up a webhook or plugin to listen for the
          // payment_intent.succeeded event that handles any business critical
          // post-payment actions.
          window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
        }
      });

    },
    error(xhr, errmsg, err) {},
  });
});