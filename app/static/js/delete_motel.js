function deleteMotel(path) {
    if (confirm('Xác nhận xóa nhà trọ này ?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`${path}`, {
            method: 'DELETE',
            headers: {
                'X-CSRF-Token': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Xóa nhà trọ thành công');
                location.reload();
            }
            else {
                alert('Có lỗi xảy ra')
            }
        })
        .catch(error => {
            console.log('Error: ', error);
            alert('Lỗi xảy ra khi đang thực hiện xóa');
        });
    }
}
