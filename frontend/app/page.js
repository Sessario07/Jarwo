import React from 'react';
import './landing.css';

export default async function LandingPage() {
  let highlightedItem = null;
  try {
    const resHighlighted = await fetch("http://backend:8000/api/items/highlighted", {
      cache: "no-store"
    });
    const data = await resHighlighted.json();
    if (!data.error) highlightedItem = data;
  } catch (_) {}

  let normalItems = [];
  try {
    const resItems = await fetch("http://backend:8000/api/items", {
      cache: "no-store"
    });
    const itemsResponse = await resItems.json();
    const rawList = itemsResponse.data || [];
    normalItems = rawList.map(item => ({
      id: item.item_id,
      name: item.item_name,
      price: item.item_customer_price,
      image: item.item_link
    }));
  } catch (_) {}

  return (
    <div className="landing-container">
      <nav className="navbar">
        <div className="navbar-brand">Jar<span>wo</span></div>
        <ul className="navbar-links">
          <li><a href="#">Beranda</a></li>
          <li><a href="#">Produk</a></li>
          <li><a href="#">Tentang Kami</a></li>
        </ul>
        <button className="navbar-cta">Hubungi Kami</button>
      </nav>

      {highlightedItem ? (
        <section className="hero-section">
          <div className="hero-content">
            <div className="badge">✦ Produk Unggulan</div>
            <h1 className="hero-title">{highlightedItem.title}</h1>
            <p className="hero-subtitle">{highlightedItem.subtitle}</p>
            <div className="hero-actions">
              <span className="hero-price">Rp {Number(highlightedItem.price).toLocaleString('id-ID')}</span>
              <button className="primary-btn">Beli Sekarang →</button>
            </div>
          </div>
          <div className="hero-image-wrapper">
            <div className="hero-image-blob"></div>
            <img src={highlightedItem.image} alt={highlightedItem.title} className="hero-image" />
          </div>
        </section>
      ) : (
        <section className="hero-section">
          <div className="hero-content">
            <div className="badge">✦ Selamat Datang</div>
            <h1 className="hero-title">Temukan produk terbaik <em>untuk kamu</em></h1>
            <p className="hero-subtitle">Belanja mudah, cepat, dan terpercaya. Pilih dari koleksi terkurasi kami.</p>
            <div className="hero-actions">
              <button className="primary-btn">Lihat Koleksi →</button>
            </div>
          </div>
        </section>
      )}

      <section className="products-section">
        <div className="section-header">
          <h2 className="section-title">Koleksi Kami</h2>
          <p className="section-subtitle">{normalItems.length} produk tersedia</p>
        </div>

        {normalItems.length > 0 ? (
          <div className="products-grid">
            {normalItems.map(item => (
              <div key={item.id} className="product-card">
                <div className="product-image-container">
                  <img src={item.image} alt={item.name} />
                </div>
                <div className="product-info">
                  <h3 className="product-name">{item.name}</h3>
                  <div className="product-footer">
                    <span className="product-price">Rp {Number(item.price).toLocaleString('id-ID')}</span>
                    <button className="add-btn" title="Tambah ke keranjang">+</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>Belum ada produk tersedia. Jalankan seeder untuk mengisi database.</p>
          </div>
        )}
      </section>

    </div>
  );
}