-- LuxCompare AI Database Schema

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS regional_prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    country VARCHAR(100) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vat_rules (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) UNIQUE NOT NULL,
    vat_rate NUMERIC(5, 4) NOT NULL,
    refund_rate NUMERIC(5, 4) NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS exchange_rates (
    id SERIAL PRIMARY KEY,
    currency VARCHAR(10) UNIQUE NOT NULL,
    sgd_rate NUMERIC(10, 6) NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_name ON products(product_name);
CREATE INDEX idx_regional_prices_product ON regional_prices(product_id);
CREATE INDEX idx_regional_prices_country ON regional_prices(country);

-- ============================================================
-- SEED DATA
-- ============================================================

-- VAT Rules
INSERT INTO vat_rules (country, vat_rate, refund_rate, notes) VALUES
('France',    0.20, 0.12, 'Detaxe refund ~12% of retail (VAT included)'),
('Italy',     0.22, 0.13, 'Tax refund ~13% of retail (VAT included)'),
('Japan',     0.10, 0.10, 'Full consumption tax refund for tourists'),
('Singapore', 0.09, 0.00, 'No VAT refund for residents');

-- Exchange Rates (approximate, as of mid-2025)
INSERT INTO exchange_rates (currency, sgd_rate) VALUES
('EUR', 1.46),
('JPY', 0.0092),
('SGD', 1.00),
('USD', 1.35);

-- Products
INSERT INTO products (brand, product_name, category, description) VALUES
('Chanel',      'Classic Flap Medium',          'Handbag',    'Iconic quilted leather flap bag with gold or silver hardware'),
('Chanel',      'Classic Flap Small',           'Handbag',    'Compact version of the iconic Classic Flap'),
('Chanel',      'Boy Bag Medium',               'Handbag',    'Edgy structured bag with chain strap'),
('Louis Vuitton','Neverfull MM',                'Handbag',    'Spacious tote in signature Monogram canvas'),
('Louis Vuitton','Speedy Bandoulière 25',        'Handbag',    'Classic doctor-bag silhouette with strap'),
('Louis Vuitton','Capucines MM',                'Handbag',    'Refined structured tote in Taurillon leather'),
('Dior',        'Lady Dior Medium',             'Handbag',    'Structured cannage-stitched bag, signature of the house'),
('Dior',        'Book Tote Large',              'Handbag',    'Oversized embroidered canvas tote'),
('Dior',        'Saddle Bag',                   'Handbag',    'Curved silhouette in Dior Oblique canvas'),
('Hermès',      'Birkin 25',                    'Handbag',    'Coveted structured tote in Togo leather'),
('Hermès',      'Kelly 28',                     'Handbag',    'Structured trapezoid bag with iconic lock'),
('Hermès',      'Constance 24',                 'Handbag',    'Sleek flap bag with H-buckle closure'),
('Chanel',      'Gabrielle Hobo Bag',           'Handbag',    'Casual yet luxurious hobo with mixed chains'),
('Louis Vuitton','Twist MM',                    'Handbag',    'Structured flap bag with LV twist lock'),
('Dior',        'Miss Dior Mini Bag',           'Handbag',    'Petite quilted bag with CD signature');

-- Regional Prices (EUR for France/Italy, JPY for Japan, SGD for Singapore)
-- Chanel Classic Flap Medium
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(1, 'France',    'EUR', 10300),
(1, 'Italy',     'EUR', 10300),
(1, 'Japan',     'JPY', 1694000),
(1, 'Singapore', 'SGD', 15500);

-- Chanel Classic Flap Small
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(2, 'France',    'EUR', 8900),
(2, 'Italy',     'EUR', 8900),
(2, 'Japan',     'JPY', 1463000),
(2, 'Singapore', 'SGD', 13400);

-- Chanel Boy Bag Medium
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(3, 'France',    'EUR', 9400),
(3, 'Italy',     'EUR', 9400),
(3, 'Japan',     'JPY', 1540000),
(3, 'Singapore', 'SGD', 14200);

-- LV Neverfull MM
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(4, 'France',    'EUR', 1630),
(4, 'Italy',     'EUR', 1630),
(4, 'Japan',     'JPY', 269500),
(4, 'Singapore', 'SGD', 2630);

-- LV Speedy Bandoulière 25
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(5, 'France',    'EUR', 1520),
(5, 'Italy',     'EUR', 1520),
(5, 'Japan',     'JPY', 251000),
(5, 'Singapore', 'SGD', 2450);

-- LV Capucines MM
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(6, 'France',    'EUR', 5550),
(6, 'Italy',     'EUR', 5550),
(6, 'Japan',     'JPY', 912000),
(6, 'Singapore', 'SGD', 8500);

-- Dior Lady Dior Medium
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(7, 'France',    'EUR', 5600),
(7, 'Italy',     'EUR', 5600),
(7, 'Japan',     'JPY', 913000),
(7, 'Singapore', 'SGD', 8600);

-- Dior Book Tote Large
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(8, 'France',    'EUR', 3100),
(8, 'Italy',     'EUR', 3100),
(8, 'Japan',     'JPY', 506000),
(8, 'Singapore', 'SGD', 4700);

-- Dior Saddle Bag
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(9, 'France',    'EUR', 3600),
(9, 'Italy',     'EUR', 3600),
(9, 'Japan',     'JPY', 588000),
(9, 'Singapore', 'SGD', 5500);

-- Hermès Birkin 25
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(10, 'France',    'EUR', 9600),
(10, 'Italy',     'EUR', 9800),
(10, 'Japan',     'JPY', 1540000),
(10, 'Singapore', 'SGD', 16000);

-- Hermès Kelly 28
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(11, 'France',    'EUR', 10200),
(11, 'Italy',     'EUR', 10400),
(11, 'Japan',     'JPY', 1650000),
(11, 'Singapore', 'SGD', 17000);

-- Hermès Constance 24
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(12, 'France',    'EUR', 8700),
(12, 'Italy',     'EUR', 8900),
(12, 'Japan',     'JPY', 1400000),
(12, 'Singapore', 'SGD', 14500);

-- Chanel Gabrielle Hobo
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(13, 'France',    'EUR', 4550),
(13, 'Italy',     'EUR', 4550),
(13, 'Japan',     'JPY', 745000),
(13, 'Singapore', 'SGD', 6900);

-- LV Twist MM
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(14, 'France',    'EUR', 4800),
(14, 'Italy',     'EUR', 4800),
(14, 'Japan',     'JPY', 786000),
(14, 'Singapore', 'SGD', 7300);

-- Dior Miss Dior Mini
INSERT INTO regional_prices (product_id, country, currency, price) VALUES
(15, 'France',    'EUR', 3200),
(15, 'Italy',     'EUR', 3200),
(15, 'Japan',     'JPY', 522000),
(15, 'Singapore', 'SGD', 4900);
