import React, { useState, useEffect } from 'react';
import axios from 'axios';
import axiosInstance from './axiosInstance';

function StoreComponent() {
    const [products, setProducts] = useState();
    const [cartItems, setCartItems] = useState();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAccessToken = async () => {
            try {
                const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/api/token/`, {
                    grant_type: 'client_credentials',
                    client_id: process.env.REACT_APP_AUTH0_CLIENT_ID,
                    client_secret: process.env.REACT_APP_AUTH0_CLIENT_SECRET,
                    audience: process.env.REACT_APP_AUTH0_AUDIENCE,
                });
                return response.data.access_token;
            } catch (error) {
                console.error('Error fetching access token:', error.response ? error.response.data : error.message);
                throw error;
            }
        };

        const fetchData = async (token) => {
            try {
                axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                const [productsResponse, cartItemsResponse] = await Promise.all([
                    axiosInstance.get('products/'),
                    axiosInstance.get('cart-items/')
                ]);
                setProducts(productsResponse.data);
                setCartItems(cartItemsResponse.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Error fetching data');
            } finally {
                setLoading(false);
            }
        };

        fetchAccessToken()
            .then(fetchData)
            .catch(error => {
                console.error('Error setting access token:', error);
                setError('Error setting access token');
                setLoading(false);
            });
    }, );

    const addToCart = (product) => {
        axiosInstance.post('cart-items/', { product })
            .then(response => setCartItems(response.data))
            .catch(error => console.error('Error adding item to cart:', error));
    };

    const removeItem = (id) => {
        axiosInstance.delete(`cart-items/${id}/`)
            .then(response => setCartItems(response.data))
            .catch(error => console.error('Error removing item from cart:', error));
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
                {products.length === 0 ? (
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
                {cartItems.length === 0 ? (
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