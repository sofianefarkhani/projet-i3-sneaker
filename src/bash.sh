cat ../output.txt | while  read ligne ; do
   
  cp /run/user/1000/gvfs/sftp:host=access886997315.webspace-data.io,user=u106097170-projetia/resources/$ligne /mnt/424cf323-70f0-406a-ae71-29e3da370aec/Temp
  
done