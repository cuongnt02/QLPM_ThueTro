document.getElementById('bookingForm').addEventListener('submit', function(e) {
    e.preventDefault();

    fetch(this.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: new URLSearchParams(new FormData(this)).toString()
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Xử lý thành công
            window.location.href = data.url; // Ví dụ, chuyển hướng đến URL trả về
        } else {
            // Xử lý lỗi
            alert('Đã xảy ra lỗi: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Lỗi khi gửi yêu cầu:', error);
    });
});
