// 発行可能なAPIキーでStripeオブジェクトのインスタンスを作成します
let checkoutButtons = document.querySelectorAll('.checkout-button');

checkoutButtons.forEach(function (checkoutButton) {
  checkoutButton.addEventListener('click', function () {
    fetch('/payment/create_checkout_session', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-CSRFToken': '{{ csrf_token }}'
      },
      body: JSON.stringify({
        priceId: checkoutButton.value
      })
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (session) {
        const stripe = Stripe(session.publicKey);
        return stripe.redirectToCheckout({ sessionId: session.id });
      })
      .then(function (result) {
        // ブラウザやネットワークが原因でredirectToCheckoutが失敗した場合
        // ローカライズされたエラーメッセージを表示する必要があります
        // error.messageを使用しています
        if (result.error) {
          alert(result.error.message);
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
      });
  });
});
