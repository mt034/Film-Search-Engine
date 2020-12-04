Add-Type -AssemblyName PresentationCore,PresentationFramework
         

function file_search(){
Add-Type -AssemblyName System.Windows.Forms
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
[void]$FolderBrowser.ShowDialog()
$PATH = $FolderBrowser.SelectedPath
return $PATH}

function no_dvd(){
$msgBody = "No CD detected!"
$msgTitle = "Empty CD Drive"
$msgButton = 'OKCancel'
$msgImage = 'Warning'
$Result = [System.Windows.MessageBox]::Show($msgBody,$msgTitle,$msgButton,$msgImage)
}

$PATH = ""
if((Get-WMIObject -Class Win32_CDROMDrive -Property *).MediaLoaded)
	{
	#Get the Removable Disk Relative Path 
	$Disk = Get-WmiObject -Class Win32_logicaldisk -Filter "DriveType = '5'"
	$PATH = $Disk.GetRelationships() | Select-Object -Property __RELPATH
	Write-Output $PATH
	} 
# Error: no CD was detected
else{
	no_dvd
	$PATH = file_search
	Write-Output $PATH
}

#use regex to get the correct VOB Files from the disk
$CertificateFileRegEx = '\bVTS\w*.VOB'
$VOB_Files = Get-ChildItem -Path $PATH | Where-Object -FilterScript {$_.Name -match $CertificateFileRegEx}

Write-Output $VOB_Files

#set up the concat files
$concat_VOB_Call = 'concat:'
foreach($file in $VOB_Files){$concat_VOB_Call = "$concat_VOB_Call$file|"}

Write-Output $concat_VOB_Call

#combine files
.\ffmpeg -i $concat -f dvd -c copy output.VOB

#convert Vobs to srts
.\SE3518\SubtitleEdit.exe /convert $PATH\*.VOB srt 

