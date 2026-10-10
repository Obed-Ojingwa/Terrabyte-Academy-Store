import { FormEvent, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';

type IconName =
  | 'search'
  | 'heart'
  | 'cart'
  | 'phone'
  | 'arrow'
  | 'eye'
  | 'star'
  | 'check'
  | 'shipping'
  | 'secure'
  | 'return'
  | 'support'
  | 'menu'
  | 'close'
  | 'instagram'
  | 'facebook'
  | 'linkedin'
  | 'whatsapp';

const iconShapes: Record<IconName, string[]> = {
  search: ['M21 21l-4.35-4.35', 'M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z'],
  heart: ['M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8z'],
  cart: ['M3 3h2l2.2 11.2a2 2 0 0 0 2 1.6h8.9a2 2 0 0 0 1.9-1.4L22 8H6', 'M10 21a1 1 0 1 0 0-2 1 1 0 0 0 0 2z', 'M18 21a1 1 0 1 0 0-2 1 1 0 0 0 0 2z'],
  phone: ['M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7l.5 3.2a2 2 0 0 1-.6 1.7L7.7 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 1.7-.6l3.2.5a2 2 0 0 1 1.7 2.4z'],
  arrow: ['M5 12h14', 'm12 5 7 7-7 7'],
  eye: ['M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z', 'M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z'],
  star: ['m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3z'],
  check: ['m5 12 4 4L19 6'],
  shipping: ['M3 7h11v11H3z', 'M14 11h4l3 3v4h-7z', 'M7.5 21a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z', 'M17.5 21a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z'],
  secure: ['M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z', 'm9 12 2 2 4-4'],
  return: ['M3 12a9 9 0 1 0 2.6-6.4L3 8', 'M3 3v5h5', 'M12 7v5l3 2'],
  support: ['M3 11a9 9 0 0 1 18 0', 'M3 11v5a2 2 0 0 0 2 2h2v-7H5a2 2 0 0 0-2 2z', 'M21 11v5a2 2 0 0 1-2 2h-2v-7h2a2 2 0 0 1 2 2z', 'M12 21h3'],
  menu: ['M4 6h16', 'M4 12h16', 'M4 18h16'],
  close: ['M18 6 6 18', 'm6 6 12 12'],
  instagram: ['M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5z', 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z', 'M17.5 6.5h.01'],
  facebook: ['M15 3h-3a5 5 0 0 0-5 5v3H4v4h3v6h4v-6h3l1-4h-4V8a1 1 0 0 1 1-1h3z'],
  linkedin: ['M4 9v11', 'M4 4v.01', 'M9 20v-7a4 4 0 0 1 8 0v7', 'M9 12v8'],
  whatsapp: ['M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20l1.1-5.2A8.4 8.4 0 1 1 21 11.5z', 'M9 9a6 6 0 0 0 6 6l1-1-2-2-1 1a4 4 0 0 1-2-2l1-1-2-2-1 1z'],
};

function Icon({ name, size = 18, className = '' }: { name: IconName; size?: number; className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {iconShapes[name].map((shape) => <path d={shape} key={shape} />)}
    </svg>
  );
}

type ProductStyle = 'camera' | 'drone' | 'receiver';

function ProductArt({ type, hero = false }: { type: ProductStyle; hero?: boolean }) {
  if (type === 'drone') {
    return (
      <svg className={hero ? 'product-art product-art--hero' : 'product-art'} viewBox="0 0 360 210" role="img" aria-label="Survey drone">
        <defs>
          <linearGradient id="drone-body" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#f9fbfd" /><stop offset="1" stopColor="#9aa8b7" /></linearGradient>
          <filter id="drone-shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="9" stdDeviation="7" floodOpacity=".22" /></filter>
        </defs>
        <g filter="url(#drone-shadow)" stroke="#273445" strokeWidth="8" strokeLinecap="round">
          <path d="M165 93 67 51M195 93l98-42M163 112l-93 48M197 112l93 48" />
          <path d="M31 43h65M264 43h65M37 168h63M260 168h63" strokeWidth="4" />
          <path d="M143 91q37-26 74 0l12 31q-49 25-98 0z" fill="url(#drone-body)" strokeWidth="3" />
          <path d="M166 119h28v28h-28z" fill="#50667a" strokeWidth="3" />
          <circle cx="180" cy="151" r="7" fill="#172b40" strokeWidth="2" />
        </g>
        <circle cx="180" cy="105" r="4" fill="#ff6b38" />
      </svg>
    );
  }

  if (type === 'receiver') {
    return (
      <svg className={hero ? 'product-art product-art--hero' : 'product-art'} viewBox="0 0 360 210" role="img" aria-label="Surveying GNSS receiver">
        <defs>
          <linearGradient id="receiver-shell" x1="0" x2="0.9" y1="0" y2="1"><stop stopColor="#fff" /><stop offset=".58" stopColor="#dfe5e9" /><stop offset="1" stopColor="#aebbc4" /></linearGradient>
          <linearGradient id="receiver-face" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#293a46" /><stop offset="1" stopColor="#0c171e" /></linearGradient>
          <filter id="receiver-shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="10" stdDeviation="8" floodOpacity=".28" /></filter>
        </defs>
        <g filter="url(#receiver-shadow)">
          <path d="M72 111q5-41 39-49l29-27q40-12 80 0l29 27q34 8 39 49l-9 44q-5 19-27 19H108q-22 0-27-19z" fill="url(#receiver-shell)" />
          <path d="m88 107 14-32q5-10 17-10h128q12 0 17 10l14 32z" fill="#f7fafb" />
          <path d="M77 111h206v11H77z" fill="#ef5b36" />
          <rect x="111" y="122" width="138" height="41" rx="9" fill="url(#receiver-face)" />
          <rect x="129" y="131" width="102" height="23" rx="4" fill="#15242a" />
          <circle cx="146" cy="142" r="4" fill="#ff4138" /><circle cx="168" cy="142" r="4" fill="#ff813a" />
          <circle cx="190" cy="142" r="4" fill="#00d7ba" /><circle cx="212" cy="142" r="4" fill="#72e8a2" />
          <path d="M96 159q11-5 20 2l3 10h-16q-8 0-7-12zm168 2q11-7 20-2l-1 12h-16z" fill="#ed5b35" />
          <path d="M112 78h28l-4 13h-29zm108 0h28l5 13h-29z" fill="#dce3e7" />
        </g>
      </svg>
    );
  }

  return (
    <svg className={hero ? 'product-art product-art--hero' : 'product-art'} viewBox="0 0 360 210" role="img" aria-label="Professional thermal camera">
      <defs>
        <linearGradient id="camera-shell" x1="0" x2="0.8" y1="0" y2="1"><stop stopColor="#30383d" /><stop offset=".48" stopColor="#111719" /><stop offset="1" stopColor="#454c50" /></linearGradient>
        <radialGradient id="camera-lens"><stop stopColor="#172e43" /><stop offset=".2" stopColor="#93aeb4" /><stop offset=".26" stopColor="#0b1723" /><stop offset=".56" stopColor="#253f55" /><stop offset=".64" stopColor="#070b10" /><stop offset=".8" stopColor="#53626a" /><stop offset="1" stopColor="#101619" /></radialGradient>
        <filter id="camera-shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="7" floodOpacity=".25" /></filter>
      </defs>
      <g filter="url(#camera-shadow)">
        <path d="M71 76q7-16 23-16h171q19 0 25 19l11 45q4 18-13 25H74q-18-7-14-25z" fill="url(#camera-shell)" />
        <rect x="145" y="43" width="34" height="27" rx="3" fill="#141a1d" />
        <rect x="157" y="34" width="12" height="11" fill="#252c30" />
        <path d="M80 83 54 88q-10 4-10 13v25q0 8 10 11l30 4zm198 0 23 6q10 3 10 12v24q0 8-10 11l-28 5z" fill="#5f686d" />
        <circle cx="128" cy="112" r="46" fill="url(#camera-lens)" stroke="#aab4b8" strokeWidth="4" />
        <circle cx="128" cy="112" r="27" fill="none" stroke="#87969b" strokeWidth="2" />
        <circle cx="128" cy="112" r="15" fill="#142938" stroke="#69818c" strokeWidth="2" />
        <circle cx="229" cy="116" r="24" fill="url(#camera-lens)" stroke="#aab4b8" strokeWidth="4" />
        <circle cx="229" cy="116" r="7" fill="#a5dc96" />
        <path d="M191 78h30" stroke="#7d898f" strokeWidth="5" strokeLinecap="round" />
        <circle cx="258" cy="79" r="5" fill="#e75b51" />
      </g>
    </svg>
  );
}

type Product = {
  id: string;
  name: string;
  detail: string;
  category: string;
  price: string;
  oldPrice?: string;
  reviews: number;
  art: ProductStyle;
};

const products: Product[] = [
  { id: 'thermal-camera', name: 'DJI Zenmuse H30T', detail: 'Thermal camera', category: 'Surveying Equipment', price: '₦2,500,000', reviews: 10, art: 'camera' },
  { id: 'survey-drone', name: 'DJI Matrice 350 RTK', detail: 'Enterprise survey drone', category: 'Drone', price: '₦8,750,000', reviews: 18, art: 'drone', oldPrice: '₦9,200,000' },
  { id: 'gnss-receiver', name: 'Hi-Target V200', detail: 'GNSS receiver', category: 'Surveying Equipment', price: '₦3,850,000', reviews: 24, art: 'receiver', oldPrice: '₦4,100,000' },
];

const categories = [
  { label: 'Geo Kits & Wears', count: '120 Products', art: 'camera' as ProductStyle },
  { label: 'Surveying Equipment', count: '200 Products', art: 'receiver' as ProductStyle },
  { label: 'Drone', count: '200 Products', art: 'drone' as ProductStyle },
  { label: 'Software & License', count: '200 Products', art: 'receiver' as ProductStyle },
  { label: 'Digital maps', count: '200 Products', art: 'receiver' as ProductStyle },
  { label: 'Others', count: '200 Products', art: 'receiver' as ProductStyle },
];

const industries = [
  { title: 'Oil & Gas', detail: '124 Products', icon: '◈', className: 'industry--oil' },
  { title: 'Agriculture', detail: '124 Products', icon: '♧', className: 'industry--agriculture' },
  { title: 'Construction', detail: '124 Products', icon: '⌂', className: 'industry--construction' },
  { title: 'Mining', detail: '124 Products', icon: '◇', className: 'industry--mining' },
  { title: 'Telecommunications', detail: '124 Products', icon: '⌁', className: 'industry--telecom' },
];

const benefits: { icon: IconName; title: string; detail: string }[] = [
  { icon: 'shipping', title: 'Free Shipping', detail: 'On orders over ₦100,000' },
  { icon: 'secure', title: 'Secure Payments', detail: 'Multiple payment options' },
  { icon: 'return', title: 'Easy Returns', detail: '7-day return policy' },
  { icon: 'support', title: '24/7 Support', detail: "We're here to help" },
];

function ProductCard({ product, onAddToCart }: { product: Product; onAddToCart: (product: Product) => void }) {
  const [saved, setSaved] = useState(false);
  return (
    <article className="product-card">
      <div className="product-card__visual">
        {product.oldPrice && <span className="sale-badge">Sale</span>}
        <button
          className={`favorite-button${saved ? ' is-saved' : ''}`}
          aria-label={saved ? `Remove ${product.name} from wishlist` : `Add ${product.name} to wishlist`}
          aria-pressed={saved}
          onClick={() => setSaved(!saved)}
        >
          <Icon name="heart" size={18} />
        </button>
        <ProductArt type={product.art} />
      </div>
      <div className="product-card__details">
        <div className="product-views"><Icon name="eye" size={13} /> <span>124</span></div>
        <h3>{product.name}<br />{product.detail}</h3>
        <p className="product-description">Precision tools for work that matters.</p>
        <div className="product-rating" aria-label={`Rated 4.8 out of 5 by ${product.reviews} reviewers`}>
          <span className="product-rating__stars" aria-hidden="true">★★★★<span>★</span></span>
          <Icon name="star" size={12} />
          <span>{product.reviews} Reviews</span>
        </div>
        <div className="product-price">
          <strong>{product.price}</strong>
          {product.oldPrice && <del>{product.oldPrice}</del>}
        </div>
        <button className="button button--primary product-add" onClick={() => onAddToCart(product)}>
          Add to Cart
        </button>
      </div>
    </article>
  );
}

function SectionHeading({ eyebrow, title, link, href }: { eyebrow: string; title: string; link: string; href: string }) {
  return (
    <div className="section-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      <a className="text-link" href={href}>{link}<Icon name="arrow" size={16} /></a>
    </div>
  );
}

function SellerIllustration() {
  return (
    <svg className="seller-illustration" viewBox="0 0 360 310" role="img" aria-label="Seller working with a laptop">
      <ellipse cx="190" cy="284" rx="123" ry="14" fill="#0b1b37" opacity=".25" />
      <path d="M156 105q-3-47 40-53 43 1 43 53l-12 46-58-3z" fill="#142439" />
      <path d="M172 67q16-21 42-8l18 20-29 12-34-9z" fill="#101a28" />
      <path d="M180 111q18-17 43-4l16 70-28 47-55-42 10-58z" fill="#1471c8" />
      <path d="M173 126 140 151l-42 51 15 11 54-39 25-37zm62 2 34 41-11 20-37-35z" fill="#1262aa" />
      <path d="m104 198 14 7-11 16-17-9z" fill="#754b37" />
      <path d="M185 76q4-20 28-17 15 5 14 24l-9 27q-8 14-22 2l-13-20z" fill="#8a563d" />
      <path d="M203 100q9 7 19-2l-2 22q-8 9-19 1z" fill="#714832" />
      <path d="m148 209 76 2 31 57H128z" fill="#273a51" />
      <path d="m110 226 133 2 27 47-167-3z" fill="#c4d2dc" />
      <path d="m118 229 122 2 19 36-141-2z" fill="#172d46" />
      <path d="M94 272h184q7 0 9 6l-5 5H87l2-7q1-4 5-4z" fill="#dbe4e9" />
      <path d="M190 112h15" stroke="#e6b097" strokeWidth="2" />
    </svg>
  );
}

function HomePage() {
  const [searchInput, setSearchInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('');
  const [cartCount, setCartCount] = useState(0);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [subscribed, setSubscribed] = useState(false);

  const visibleProducts = useMemo(() => products.filter((product) => {
    const matchesSearch = `${product.name} ${product.detail} ${product.category}`.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !activeCategory || product.category === activeCategory || activeCategory === 'Geo Kits & Wears' || activeCategory === 'Others';
    return matchesSearch && matchesCategory;
  }), [activeCategory, searchQuery]);

  const handleSearch = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSearchQuery(searchInput.trim());
    setActiveCategory('');
    document.getElementById('popular')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubscribe = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubscribed(true);
  };

  const addToCart = (_product: Product) => setCartCount((count) => count + 1);

  const renderProductRow = (items: Product[], emptyText: string) => (
    <div className="product-grid">
      {items.length > 0
        ? items.map((product) => <ProductCard key={product.id} product={product} onAddToCart={addToCart} />)
        : <p className="empty-products">{emptyText}</p>}
    </div>
  );

  return (
    <div className="storefront">
      <header className="storefront-header">
        <div className="storefront-topbar">
          <Link className="store-logo" to="/" aria-label="Terrabyte Global home">
            <span className="store-logo__mark"><span /></span>
            <span className="store-logo__text"><strong>TERRABYTE</strong><small>GLOBAL LIMITED</small></span>
          </Link>

          <form className="store-search" onSubmit={handleSearch} role="search">
            <span className="store-search__category">☰</span>
            <input
              aria-label="Search products and brands"
              placeholder="Search for products, brands and more"
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
            />
            <button aria-label="Search" type="submit"><Icon name="search" size={16} /></button>
          </form>

          <a className="store-phone" href="tel:+2348151562640"><Icon name="phone" size={15} /><span>+234 816 156 2640</span></a>
          <a className="header-icon" href="#popular" aria-label="Wishlist"><Icon name="heart" size={19} /></a>
          <a className="header-icon header-cart" href="#popular" aria-label={`Shopping cart, ${cartCount} items`}>
            <Icon name="cart" size={20} />{cartCount > 0 && <span>{cartCount}</span>}
          </a>
          <div className="store-auth">
            <Link className="button button--light" to="/orders">Log in</Link>
            <Link className="button button--primary" to="/inventory">Signup</Link>
          </div>
          <button className="mobile-menu-button" aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'} aria-expanded={mobileMenuOpen} onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            <Icon name={mobileMenuOpen ? 'close' : 'menu'} size={21} />
          </button>
        </div>
        <nav className={`storefront-nav${mobileMenuOpen ? ' is-open' : ''}`} aria-label="Main navigation">
          <div className="storefront-nav__links">
            <a href="#categories"><span className="nav-categories-icon">☷</span> Categories</a>
            <a href="#industries">Training</a>
            <a href="#seller">Services</a>
            <a href="#footer">FAQ</a>
            <a href="#promotions">Blogs</a>
            <a href="#footer">Contact</a>
          </div>
          <div className="storefront-nav__region">
            <button type="button" aria-label="Language and country">🇳🇬 EN <span>⌄</span></button>
            <button type="button" aria-label="Currency">₦ Naira <span>⌄</span></button>
          </div>
        </nav>
      </header>

      <main>
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero__copy">
            <p className="hero__kicker">TERRABYTE · PRECISION TECHNOLOGY</p>
            <h1 id="hero-title">Mars GNSS Receiver</h1>
            <p>A high-precision surveying receiver with laser-assisted mapping and tilt compensation for capturing hard-to-reach spatial coordinates.</p>
            <div className="hero__actions">
              <a className="button button--primary" href="#categories">Shop Now <Icon name="arrow" size={15} /></a>
              <a className="button button--outline" href="#categories">Explore Categories</a>
            </div>
            <div className="hero__pagination"><span className="is-active" /><span /><span /></div>
          </div>
          <div className="hero__art">
            <div className="hero__glow" />
            <div className="hero__terrain" />
            <ProductArt type="receiver" hero />
            <span className="hero__art-label">MARS GNSS · FIELD READY</span>
          </div>
        </section>

        <div className="storefront-content">
          <section className="store-section category-section" id="categories">
            <SectionHeading eyebrow="SHOP BY CATEGORY" title="Explore Our Categories" link="View All Categories" href="#categories" />
            <div className="category-grid">
              {categories.map((category) => (
                <button
                  className={`category-card${activeCategory === category.label ? ' is-active' : ''}`}
                  key={category.label}
                  onClick={() => {
                    setActiveCategory(activeCategory === category.label ? '' : category.label);
                    setSearchQuery('');
                    setSearchInput('');
                  }}
                  aria-pressed={activeCategory === category.label}
                >
                  <span className="category-card__image"><ProductArt type={category.art} /></span>
                  <strong>{category.label}</strong>
                  <small>{category.count}</small>
                </button>
              ))}
            </div>
          </section>

          <section className="store-section products-section" id="popular">
            <SectionHeading eyebrow="FEATURED PRODUCTS" title="Popular Picks" link="View All Products" href="#popular" />
            {(searchQuery || activeCategory) && (
              <div className="filter-notice">
                Showing {searchQuery ? `results for “${searchQuery}”` : activeCategory}
                <button type="button" onClick={() => { setSearchQuery(''); setSearchInput(''); setActiveCategory(''); }}>Clear filter</button>
              </div>
            )}
            {renderProductRow(visibleProducts, 'No products match this selection yet. Try another category or search.')}
          </section>

          <section className="store-section products-section" id="top-rated">
            <SectionHeading eyebrow="BEST SELLERS" title="Top Rated Products" link="View All Products" href="#top-rated" />
            {renderProductRow(visibleProducts.slice().reverse(), 'No top-rated products match this selection.')}
          </section>

          <section className="store-section industries-section" id="industries">
            <SectionHeading eyebrow="SHOP BY INDUSTRY" title="Solutions for Every Industry" link="" href="#industries" />
            <div className="industry-grid">
              {industries.map((industry) => (
                <a className={`industry-card ${industry.className}`} key={industry.title} href="#popular">
                  <span className="industry-card__symbol" aria-hidden="true">{industry.icon}</span>
                  <strong>{industry.title}</strong>
                  <small>{industry.detail}</small>
                </a>
              ))}
            </div>
          </section>

          <section className="store-section products-section" id="promotions">
            <SectionHeading eyebrow="ONGOING DEALS" title="Deals and Promotions" link="View All Deals" href="#promotions" />
            {renderProductRow(visibleProducts, 'No deals match this selection yet.')}
          </section>

          <section className="seller-banner" id="seller">
            <div className="seller-banner__copy">
              <p className="eyebrow">SELL WITH TERRABYTE</p>
              <h2>Become a Seller</h2>
              <p>Turn your network into opportunity. Join our seller program and earn commissions by promoting Terrabyte products.</p>
              <ul>
                <li><Icon name="check" size={15} /> Easy Registration</li>
                <li><Icon name="check" size={15} /> Upload Products</li>
                <li><Icon name="check" size={15} /> Share &amp; Promote</li>
                <li><Icon name="check" size={15} /> Earn Commission</li>
              </ul>
              <Link className="button button--white" to="/inventory">Learn More <Icon name="arrow" size={15} /></Link>
            </div>
            <SellerIllustration />
          </section>

          <section className="benefits-strip" aria-label="Shopping benefits">
            {benefits.map((benefit) => (
              <div className="benefit" key={benefit.title}>
                <Icon name={benefit.icon} size={27} />
                <span><strong>{benefit.title}</strong><small>{benefit.detail}</small></span>
              </div>
            ))}
          </section>
        </div>
      </main>

      <footer className="storefront-footer" id="footer">
        <div className="newsletter">
          <div>
            <strong>Stay in the loop</strong>
            <p>Get the latest products, offers and updates straight to your inbox.</p>
          </div>
          <form className="newsletter-form" onSubmit={handleSubscribe}>
            <label className="sr-only" htmlFor="newsletter-email">Your email address</label>
            <input id="newsletter-email" type="email" placeholder="Enter your email address" required disabled={subscribed} />
            <button type="submit" disabled={subscribed}>{subscribed ? 'Subscribed' : 'Subscribe'}</button>
            {subscribed && <span className="newsletter-success" role="status">Thanks for subscribing!</span>}
          </form>
          <div className="footer-socials" aria-label="Social media">
            <a href="https://instagram.com" aria-label="Instagram"><Icon name="instagram" size={17} /></a>
            <a href="https://facebook.com" aria-label="Facebook"><Icon name="facebook" size={17} /></a>
            <a href="https://linkedin.com" aria-label="LinkedIn"><Icon name="linkedin" size={17} /></a>
            <a href="https://whatsapp.com" aria-label="WhatsApp"><Icon name="whatsapp" size={17} /></a>
          </div>
        </div>
        <div className="footer-main">
          <div className="footer-brand">
            <Link className="store-logo store-logo--footer" to="/">
              <span className="store-logo__mark"><span /></span>
              <span className="store-logo__text"><strong>TERRABYTE</strong><small>GLOBAL LIMITED</small></span>
            </Link>
            <p>Stephen Avenue, Mission House, 1st Floor, Bomi Street,<br />Oshodi, Lagos, Nigeria</p>
            <a href="tel:+2348161562640">+234 816 156 2640</a>
            <a href="mailto:info@terrabyteglobal.com">info@terrabyteglobal.com</a>
          </div>
          <div className="footer-column">
            <strong>Shop by Category</strong>
            {categories.map((category) => <a href="#categories" key={category.label}>{category.label}</a>)}
          </div>
          <div className="footer-column">
            <strong>Quick Links</strong>
            <a href="#footer">About Us</a><a href="#seller">Services</a><a href="#industries">Training</a><Link to="/inventory">Store</Link><Link to="/orders">Blog</Link><Link to="/inventory">Become a Seller</Link>
          </div>
          <div className="footer-column">
            <strong>Help &amp; Support</strong>
            <a href="#footer">FAQ</a><a href="#footer">Shipping Information</a><a href="#footer">Returns &amp; Refunds</a><Link to="/orders">Track Order</Link><a href="mailto:info@terrabyteglobal.com">Contact Us</a>
          </div>
          <div className="footer-column">
            <strong>Policies</strong>
            <a href="#footer">Terms &amp; Condition</a><a href="#footer">Privacy Policy</a><a href="#footer">Returns &amp; Refunds Policy</a><a href="#footer">Shipping Policy</a><a href="#footer">Warranty Policy</a><a href="#footer">Cookie Policy</a>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© {new Date().getFullYear()} <span>Terrabyte Global Ltd.</span> All rights reserved.</p>
          <div className="payment-methods" aria-label="Accepted payment methods"><span>PayPal</span><span>VISA</span><span>●●</span><span>▤</span></div>
        </div>
      </footer>
    </div>
  );
}

export { HomePage };
