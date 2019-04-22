Write-Output " In Location :: $PSScriptRoot "
$url = "http://repo.noicldhcl.com/appdata/postInstall/sccmclient.zip"
$output = "c:\temp\sccmclient.zip"
$unzipPath = "c:\temp\sccmclient"

$start_time = Get-Date

#Invoke-WebRequest -Uri $url -OutFile $output
#Write-Output "Time taken: $((Get-Date).Subtract($start_time).Seconds) second(s)"

$wc = New-Object System.Net.WebClient
$wc.DownloadFile($url, $output)
#(New-Object System.Net.WebClient).DownloadFile($url, $output)

Write-Output "Time taken: $((Get-Date).Subtract($start_time).Milliseconds ) millsecond(s)"

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($output,$unzipPath)

Write-Output "SCCM Client Files Unzipped"
$start_time = Get-Date

c:\temp\sccmclient\Client\ccmsetup.exe /mp:sccm smsmp=sccm smssitecode=PR1 /Source:c:\temp\sccmclient\Client

Write-Output "Time taken To Execute CCMSetup : $((Get-Date).Subtract($start_time).Milliseconds ) millsecond(s)"
