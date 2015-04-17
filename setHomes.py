import subprocess, os

f = open("Teachers.csv", 'r')

for each in f:
	output = ""
	line = each.strip('\n').replace('"', '').split(',')
	userName = line[0]
	print("Setting homeFolder permissions for: "+userName)
	w = open(userName+"home.ps1", 'w')
	w.write("import-module activedirectory -Force\n")
	w.write("$homeDir=Get-ADUser "+userName+" -properties homedirectory | Select-Object homedirectory\n")
	w.write("$dirSplit=$homeDir -split '='\n")
	w.write("$dir=$dirSplit[1] -split '}'\n")
	w.write("$HomeFolderACL=GET-ACL $dir[0]\n")
	domain = os.path.normpath("ICC.EDU//")
	w.write("$identity='ICC.edu\\"+userName+"'\n")
	w.write("$InheritanceFlags=[System.Security.AccessControl.InheritanceFlags]'ContainerInherit,ObjectInherit'\n")
	w.write("$AccessRule=NEW-OBJECT system.security.AccessControl.FileSystemAccessRule($identity,'FullControl',$InheritanceFlags,'None','Allow')\n")
	w.write("$HomeFolderACL.AddAccessRule($AccessRule)\n")
	w.write("SET-ACL -path $dir[0] -AclObject $HomeFolderACL\n")
	w.close()
	cmd = subprocess.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-ExecutionPolicy", "Unrestricted",". \"./"+userName+"home.ps1\";"],stdout=subprocess.PIPE)
	output = cmd.communicate()
f.close()
