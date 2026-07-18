@echo off
:: make the script not send any output (suppresses except errors, which are suppressed >nul)
setlocal enabledelayedexpansion
:: allows variables to update inside loops using !var! instead of %var%. When writing to files, %var% would be interpreted as the actual characters, while !var! would yield the value of the variable
echo list disk > X:\listdisk.txt
:: make a script file that tells diskpart to list all disk information
diskpart /s X:\listdisk.txt > X:\disks.txt
:: run the script file to know how many disks there are. Saves the information to a file.
for /f "tokens=2" %%d in ('type X:\disks.txt ^| find "Disk"') do (
   :: looks for lines with the word Disk. In lines found, saves the second word (token), which is the disk number, then loops through each disk
   set "diskNum=%%d"
   :: puts the disk number in a usable variable
   (
       echo select disk !diskNum!
       :: select the disk in diskpart
       echo list partition
       :: list all its partitions
   ) > X:\listpart.txt
   :: save commands to a file for diskpart to run
   diskpart /s X:\listpart.txt > X:\parts.txt
   :: run the file with diskpart and save the partition information
   for /f "tokens=2" %%p in ('type X:\parts.txt ^| find "Partition"') do (
       :: looks for lines with the word Partition. In lines found, saves the second word (token), which is the partition number, then loops through each partition
       set "pNum=%%p"
       :: puts the partition number in a usable variable
       (
           echo select disk !diskNum!
           :: select the disk
           echo select partition !pNum!
           :: select the partition
           echo detail partition
           :: get partition information to check if it is a recovery partition. The recovery partition should be deleted last so if the process is stopped in the middle it can continue
       ) > X:\detail.txt
       :: save commands to a file for diskpart to run
       diskpart /s X:\detail.txt > X:\part_info.txt
       :: run diskpart and save the information about the partition to a file
       set "isRecovery=false"
       :: initialize a variable for knowing if it is a recovery partition
       for /f "tokens=*" %%a in ('type X:\part_info.txt ^| find /i "Recovery"') do (
           :: looks for the word Recovery in the partition info
           set "isRecovery=true"
           :: sets the variable to true
       )
       if "!isRecovery!"=="false" (
           :: runs if it's not a recovery partition
           (
               echo select disk !diskNum!
               :: select the disk
               echo select partition !pNum!
               :: select the partition
               echo delete partition override
               :: force delete partition
           ) > X:\del_part.txt
           :: save commands to a file for diskpart to run
           diskpart /s X:\del_part.txt >nul
           :: run the file with diskpart
       ) else (
           :: runs if it is a recovery partition
           set "recoveryPart=!pNum!"
           :: store the recovery partition number to be deleted later
       )
   )
   :: end of partition loop
   if defined recoveryPart (
       :: checks if there was a recovery partition
       (
          echo select disk !diskNum!
          :: select the disk
          echo select partition !recoveryPart!
          :: select the recovery partition
          echo delete partition override
          :: force delete the recovery partition
       ) > X:\del_final.txt
       :: save commands to a file for diskpart to run
       diskpart /s X:\del_final.txt >nul
       :: run the file with diskpart
   )
   (
       echo select disk !diskNum!
       :: select the disk
       echo clean all
       :: wipe the disk clean
   ) > X:\wipe_final.txt
   :: save commands to a file for diskpart to run
   diskpart /s X:\wipe_final.txt >nul
   :: run the file with diskpart
)
:: end of disk loop
wpeutil shutdown
:: shut down the system