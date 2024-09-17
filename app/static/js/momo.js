function momoPayment(path) {
    fetch(path).then(res => res.json())
        .then(data => {
            if (data['payUrl']) {
                window.open(data['payUrl'], "_blank");
            }
        });
}
