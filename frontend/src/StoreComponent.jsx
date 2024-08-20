import React, { useState, useEffect } from 'react';
import axiosInstance from './axiosInstance';

function StoreComponent() {
    const [products, setProducts] = useState([]);
    const [cartItems, setCartItems] = useState([]);
    const [cartId, setCartId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [productsResponse, cartResponse] = await Promise.all([
                    axiosInstance.get('products/'),
                    axiosInstance.get('cart/get-or-create/'),
                ]);

                console.log('Products response:', productsResponse.data);
                console.log('Cart response:', cartResponse.data);

                setProducts(productsResponse.data);
                setCartItems(cartResponse.data.items || []);  // Ensure items is always an array
                setCartId(cartResponse.data.id);


            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Error fetching data');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const addToCart = async (productId) => {
        try {
            if (!cartId) {
                console.error('Cart ID is not set');
                return;
            }
    
            const response = await axiosInstance.post('/cart-items/', {
                cart: cartId,
                product: productId,
                quantity: 1,
            });
            console.log('Item added to cart:', response.data);
            setCartItems([...cartItems, response.data]);  // Update cart items state
        } catch (error) {
            console.error('Error adding item to cart:', error);
        }
    };
        

    const removeItem = (id) => {
        axiosInstance.delete(`http://127.0.0.1:8000/api/v1/cart-items/${id}/`)
            .then(response => {
                const updatedCartItems = cartItems.filter(item => item.id !== id);
                setCartItems(updatedCartItems);
            })
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
                                    <button onClick={() => addToCart(product.id)}>Add to Cart</button>
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