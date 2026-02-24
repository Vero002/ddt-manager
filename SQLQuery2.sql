USE DDTManager;
GO

INSERT INTO Cantieri (Nome, Indirizzo, Citta)
VALUES 
('Cantiere Milano Centro', 'Via Roma 10', 'Milano'),
('Cantiere Bergamo Nord', 'Via Verdi 5', 'Bergamo');

INSERT INTO Veicoli (Targa, Descrizione)
VALUES
('AB123CD', 'Iveco Daily'),
('EF456GH', 'Mercedes Actros');

INSERT INTO DDT (NumeroDDT, DataDDT, CantiereId, VeicoloId, Materiale, Quantita, Note)
VALUES
('DDT001', '2026-02-24', 1, 1, 'Sabbia', 10, 'Consegna mattina'),
('DDT002', '2026-02-24', 2, 2, 'Cemento', 25, 'Urgente'),
('DDT003', '2026-02-25', 1, 2, 'Ghiaia', 15, 'Secondo viaggio');