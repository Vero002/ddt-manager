USE DDTManager;
GO

-- Tabella Cantieri
CREATE TABLE Cantieri (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(150) NOT NULL,
    Indirizzo NVARCHAR(250),
    Citta NVARCHAR(100),
    Attivo BIT DEFAULT 1
);

-- Tabella Veicoli
CREATE TABLE Veicoli (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Targa NVARCHAR(20) NOT NULL UNIQUE,
    Descrizione NVARCHAR(150),
    Attivo BIT DEFAULT 1
);

-- Tabella DDT
CREATE TABLE DDT (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NumeroDDT NVARCHAR(50) NOT NULL,
    DataDDT DATE NOT NULL,
    CantiereId INT NOT NULL,
    VeicoloId INT NOT NULL,
    Materiale NVARCHAR(250),
    Quantita DECIMAL(10,2),
    Note NVARCHAR(500),

    CONSTRAINT FK_DDT_Cantiere 
        FOREIGN KEY (CantiereId) REFERENCES Cantieri(Id),

    CONSTRAINT FK_DDT_Veicolo 
        FOREIGN KEY (VeicoloId) REFERENCES Veicoli(Id)
);