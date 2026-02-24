SELECT 
    c.Nome AS Cantiere,
    v.Targa,
    COUNT(d.Id) AS NumeroDDT,
    SUM(d.Quantita) AS TotaleQuantita
FROM DDT d
JOIN Cantieri c ON d.CantiereId = c.Id
JOIN Veicoli v ON d.VeicoloId = v.Id
GROUP BY c.Nome, v.Targa
ORDER BY c.Nome;