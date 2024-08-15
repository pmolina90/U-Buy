import React, { useState, useEffect } from 'react';
import axiosInstance from './axiosInstance';

function StoreComponent() {
    const [products, setProducts] = useState();
    const [cartItems, setCartItems] = useState();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState();  

    // Fetch products from the API
    useEffect(() => {
        axiosInstance.get('products/')
            .then(response => {
                setProducts(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching products', error);
                setError('Error fetching products');
                setLoading(false);
            });    
    }, );

    // Fetch cart items
    useEffect(() => {
        axiosInstance.get('cart-items/')
            .then(response => setCartItems(response.data))
            .catch(error => console.error('Error fetching cart items', error));
    }, );

    // Add item to cart
    const addToCart = (product) => {
        axiosInstance.post('cart-items/', { product })
            .then(response => setCartItems(response.data))
            .catch(error => console.error('Error adding item to cart', error));
    };

    // Remove item from cart
    const removeItem = (id) => {
        axiosInstance.delete(`cart-items/${id}/`)
            .then(response => setCartItems(response.data))
            .catch(error => console.error('Error removing item from cart', error));
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }   

    return (
        <div>
            <h1>Store</h1>
            <div>
                <h2>Products</h2>
                {products && products.length === 0 ? (
                    <p>No products available</p>
                ) : (
                    <ul>
                        {products.map(product => (
                            <li key={product.id}>
                                <div>
                                    {product.images && product.images.length > 0 && (
                                        <img
                                            src={product.images[0]}
                                            alt={product.title}
                                            style={{ width: '100px', height: '100px' }}
                                        />
                                    )}
                                    <h2>{product.title}</h2>
                                    <p>{product.description}</p>
                                    <p>{product.price}</p>
                                    <button onClick={() => addToCart(product)}>Add to Cart</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            <div>
                <h2>Cart</h2>
                {cartItems && cartItems.length === 0 ? (
                    <p>No items in cart</p>
                ) : (
                    <ul>
                        {cartItems.map(item => (
                            <li key={item.id}>
                                <div>
                                    {item.product.images && item.product.images.length > 0 && (
                                        <img
                                            src={item.product.images[0]}
                                            alt={item.product.title}
                                            style={{ width: '100px', height: '100px' }}
                                        />
                                    )}
                                    <h2>{item.product.title}</h2>
                                    <p>{item.product.description}</p>
                                    <p>${item.product.price}</p>
                                    <button onClick={() => removeItem(item.id)}>Remove</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}

export default StoreComponent;