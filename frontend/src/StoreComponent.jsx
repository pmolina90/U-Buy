import React, { useState, useEffect } from 'react';
import axiosInstance from './axiosInstance';
import './StoreComponent.css';

function StoreComponent({ user, handleLogout }) {
    const [products, setProducts] = useState();
    const [filteredProducts, setFilteredProducts] = useState();
    const [cartItems, setCartItems] = useState();
    const [cartId, setCartId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isCartVisible, setIsCartVisible] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

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
                setFilteredProducts(productsResponse.data);
                setCartItems(cartResponse.data.items || []);
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

            const productResponse = await axiosInstance.get(`/products/${productId}/`);
            const productDetails = productResponse.data;

            const cartItemWithDetails = { ...response.data, product: productDetails };

            setCartItems([...cartItems, cartItemWithDetails]);
        } catch (error) {
            console.error('Error adding item to cart:', error);
        }
    };

    const removeItem = (id) => {
        axiosInstance
            .delete(`http://127.0.0.1:8000/api/v1/cart-items/${id}/`)
            .then((response) => {
                const updatedCartItems = cartItems.filter((item) => item.id !== id);
                setCartItems(updatedCartItems);
            })
            .catch((error) => console.error('Error removing item from cart:', error));
    };

    const handleSearch = (event) => {
        const query = event.target.value.toLowerCase();
        setSearchQuery(query);

        if (query === '') {
            setFilteredProducts(products);
        } else {
            setFilteredProducts(
                products.filter(
                    (product) =>
                        (product.title && product.title.toLowerCase().includes(query)) ||
                        (product.name && product.name.toLowerCase().includes(query)) ||
                        (product.category &&
                            product.category.name &&
                            product.category.name.toLowerCase().includes(query)) ||
                        (product.description && product.description.toLowerCase().includes(query))
                )
            );
        }
    };

    const calculateTotal = () => {
        return cartItems.reduce(
            (total, item) => total + item.product.price * item.quantity,
            0
        ).toFixed(2);
    };

    const handleCheckout = () => {
        alert('Checkout process completed!');
        setCartItems([]);
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <header>
                <nav>
                    <h1>Store</h1>
                    <input
                        type="text"
                        placeholder="Search..."
                        value={searchQuery}
                        onChange={handleSearch}
                        className="search-input"
                    />
                    <ul>
                        <li>
                            <p>Welcome, {user.name}!</p>
                        </li>
                        <li>
                            <button className="logout-button" onClick={handleLogout}>
                                Log Out
                            </button>
                        </li>
                        <li>
                            <button
                                className="link-button"
                                onClick={() => setIsCartVisible(!isCartVisible)}
                            >
                                <span className="cart-icon">🛒</span>
                                <span className="cart-count">{cartItems.length}</span>
                            </button>
                        </li>
                    </ul>
                </nav>
            </header>
            <main>
                <div className="products">
                    <h2>Products</h2>
                    {filteredProducts.length === 0 ? (
                        <p>No products available</p>
                    ) : (
                        <ul>
                            {filteredProducts.map((product) => (
                                <li key={product.id} className="product-card">
                                    <div>
                                        {product.images && product.images.length > 0 && (
                                            <img src={product.images[0]} alt={product.title} />
                                        )}
                                        <h3>{product.title}</h3>
                                        <p>{product.description}</p>
                                        <p className="product-price">${product.price}</p>
                                        <button onClick={() => addToCart(product.id)}>
                                            Add to Cart
                                        </button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </main>
            <div className={`cart-panel ${isCartVisible ? 'visible' : ''}`}>
                <button className="close-btn" onClick={() => setIsCartVisible(false)}>
                    X
                </button>
                <h2>Cart</h2>
                {cartItems.length === 0 ? (
                    <p>No items in cart</p>
                ) : (
                    <div>
                        <ul>
                            {cartItems.map((item) => (
                                <li key={item.id} className="cart-item">
                                    <div>
                                        {item.product.images && item.product.images.length > 0 && (
                                            <img
                                                src={item.product.images[0]}
                                                alt={item.product.title}
                                            />
                                        )}
                                        <h3>{item.product.title}</h3>
                                        <p className="product-price">${item.product.price}</p>
                                        <p>Quantity: {item.quantity}</p>
                                        <button onClick={() => removeItem(item.id)}>Remove</button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                        <div className="cart-total">
                            <p>Total: ${calculateTotal()}</p>
                            <button onClick={handleCheckout} className="checkout-button">
                                Checkout
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default StoreComponent;
