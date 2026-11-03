# TRIADE M5-b — client de tunnel en forme absolue https (etape 1).
# Modele EXACT de terrain_m4.ps1 (terrain.17, D96) : « le client qui parle
# la forme absolue https:// n'existe dans AUCUN outil standard » — le
# superviseur posait un petit script TCP qui ecrit la requete a la main et
# recopie la reponse. Meme geste, parametre par l'hote et la sortie.
# La version NAVIGATEUR du flux viendra avec la revision R3 (m5/I/README).
param(
  [string]$Hote = "autorite.test",
  [string]$Sortie = "page.txt",
  [int]$Port = 25000
)
try {
  $Client = New-Object Net.Sockets.TcpClient('127.0.0.1', $Port)
  $Client.ReceiveTimeout = 30000
  $Flux = $Client.GetStream()
  $Octets = [Text.Encoding]::ASCII.GetBytes("GET https://$Hote/ HTTP/1.1`r`nHost: $Hote`r`n`r`n")
  $Flux.Write($Octets, 0, $Octets.Length)
  $Tampon = New-Object byte[] 65536
  $Fichier = [IO.File]::Create($Sortie)
  while (($Lu = $Flux.Read($Tampon, 0, 65536)) -gt 0) {
    $Fichier.Write($Tampon, 0, $Lu)
  }
  $Fichier.Close()
  $Client.Close()
  exit 0
} catch {
  exit 1
}
