if product:
        return render_template('product.html', product=product, user=current_user)
    else:
        return 'Sản phẩm không tồn tại.'