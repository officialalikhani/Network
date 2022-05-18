
Write-Host "--------------------------------------<<  Network Automation  >>--------------------------------"   -ForegroundColor Green 
Write-Host "Enter number : "  -BackgroundColor Green  -ForegroundColor Black 
$Number = Read-Host ">>"
if ($Number -eq  1)
    { 
        $y = Read-Host "How many Host you have"
        for($x=1 ;$x -le $y;$x++)
            {
            $VMHost = Read-Host "ip"           
            $Name = Read-Host "VM name"
            $DataStore = Read-Host "datastore "
            $OVF = "#yourovfFile.ovf"
            $Credential = Get-Credential
            Connect-VIServer -Server $VMHost -Credential $Credential
            $a = Read-Host "How many VMs"
            Write-Host "PowerON => y or n" -BackgroundColor Green  -ForegroundColor Black 
            $b = Read-Host ">>"
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
                for ($i=1;$i -le $a;$i++) 
                    {
                        Import-VApp -Name "$Name-$i" -Datastore $DataStore -VMHost $VMHost -Source  $OVF -DiskStorageFormat Thin 
                        if ($b -eq "y" )
                            {Start-VM "$Name-*"}
                    }
            }
            Write-host "VMs Created and Run..........!" -BackgroundColor Green  -ForegroundColor Black 

    }
elseif($Number -eq 2)
{
    $y = Read-Host "How many Host you have"
        for($x=1 ;$x -le $y;$x++)
            {
            $VMHost = Read-Host "ip"
            $Name = Read-Host "VM name"
            $DataStore = Read-Host "datastore "
            $Credential = Get-Credential
            Connect-VIServer -Server $VMHost -Credential $Credential
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            $a = Read-Host "How many VMs"
            Write-Host "PowerON => y or n" -BackgroundColor Green  -ForegroundColor Black 
            $b = Read-Host ">>"
            for ($i=1;$i -le $a; $i++)
                {
                    New-VM -Name "$Name-$i" -VMHost $VMHost -Datastore $DataStore  -NumCpu 2 -MemoryMB '2048' -DiskMB '40960'  -GuestId "windows7Server64Guest"  -CD  
                    if ($b -eq "y" )
                            {Start-VM "$Name-*" }
        
                }
            }
        Write-host "VMs Created and Run..........!" -BackgroundColor Green  -ForegroundColor Black 
} 
elseif($Number -eq 3) 
{
            $VMHost = Read-Host "ip"
            $Name = Read-Host "VM name"
            $DataStore = Read-Host "datastore "
            $Credential = Get-Credential
            Connect-VIServer -Server $VMHost -Credential $Credential
            $Temp = Read-Host "Template "
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            $a = Read-Host "How many VMs"
            Write-Host "PowerON => y or n" -BackgroundColor Green  -ForegroundColor Black 
            $b = Read-Host ">>"
            $esxi = Read-Host "Which esxi ip"
            for ($i=1;$i -le $a;$i++)
            {
                New-VM -Name "$Name-$i" -VMHost $esxi -Datastore 'datastore1' -Template $Temp 
                if ($b -eq "y" )
                {Start-VM "$Name-*"}
            }
            Write-host "VMs Created and Run..........!" -BackgroundColor Green  -ForegroundColor Black 
}  
elseif ($Number -eq 4)
{
            $VMHost = Read-Host "ip"
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            $Credential = Get-Credential
            Connect-VIServer -Server $VMHost -Credential $Credential
            Get-VM
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            Write-Output "1 : Start  VM "
            Write-Output "2 : stop  VM "
            Write-Host " * ==> means All VMs "  -BackgroundColor Green  -ForegroundColor Black 
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            $power = Read-Host "select number"
            if ($power -eq 1)
            {
            $Name = Read-Host "Name of VM"
            Start-VM -VM $Name
            } 
            elseif ($power -eq 2)
            {
            $Name = Read-Host "Name of VM"
            Stop-VM -VM $Name
            }
}
elseif ($Number -eq 5)
{
            $VMHost = Read-Host "ip"
            Write-Host "--------------------------------------------------------------"   -ForegroundColor Green
            $Credential = Get-Credential
            Connect-VIServer -Server $VMHost -Credential $Credential
            Get-VM 
            Write-Output "-------------------------<  Delete  VM >--------------------------------"
            Write-Host  " * => means All VMs " -BackgroundColor Green  -ForegroundColor Black 
            Write-Output  
            $Name = Read-Host "Name of VM"
            Remove-VM -VM $Name -DeletePermanently
}




            
