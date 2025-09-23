CREATE TABLE boutique_ventes (
    id SERIAL PRIMARY KEY,
    date_achat DATE NOT NULL,
    ville VARCHAR(30) NOT NULL,
    produit VARCHAR(50) NOT NULL,
    prix DECIMAL(6,2) NOT NULL,
    client_type VARCHAR(20) NOT NULL
);

INSERT INTO boutique_ventes (date_achat, ville, produit, prix, client_type) VALUES
('2024-01-10', 'Paris', 'Smartphone', 699.99, 'particulier'),
('2024-01-15', 'Lyon', 'Tablette', 399.50, 'entreprise'), 
('2024-01-20', 'Paris', 'Casque', 79.90, 'particulier'),
('2024-02-01', 'Marseille', 'Smartphone', 699.99, 'entreprise'),
('2024-02-05', 'Lyon', 'Écran', 259.00, 'particulier'),
('2024-02-10', 'Paris', 'Clavier', 89.90, 'entreprise'),
('2024-02-15', 'Marseille', 'Souris', 45.50, 'particulier'),
('2024-03-01', 'Lyon', 'Smartphone', 699.99, 'particulier'),
('2024-03-05', 'Paris', 'Webcam', 129.00, 'entreprise'),
('2024-03-10', 'Marseille', 'Tablette', 399.50, 'particulier'),
('2024-03-15', 'Lyon', 'Casque', 79.90, 'entreprise'),
('2024-03-20', 'Paris', 'Écran', 259.00, 'particulier');
